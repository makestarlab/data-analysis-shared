# 공통 SQL 패턴

## 구매대행 탐지

`shipping_information` JSONB 기반 데이터 드리븐 탐지.
동일 창고주소(base_address)에 개인식별코드(detail_address) 3개 이상 + 아티스트 2개 이상.

```sql
-- Step 1: 창고주소별 고객코드 수 집계
WITH order_shipping AS (
  SELECT
    user_id,
    TRIM(JSON_EXTRACT_SCALAR(shipping_information, '$.information.address'))        AS base_address,
    TRIM(JSON_EXTRACT_SCALAR(shipping_information, '$.information.detail_address')) AS customer_code
  FROM `makestar-dw.pg_mystarroom_public.tb_commerce_order`
  WHERE payment_status = 'CONFIRMED'
    AND user_id IS NOT NULL
    AND shipping_information IS NOT NULL
),
-- 동일 창고주소에 고객코드 3개 이상인 계정
purchasing_candidates AS (
  SELECT user_id
  FROM order_shipping
  WHERE customer_code IS NOT NULL AND TRIM(customer_code) != ''
    AND base_address  IS NOT NULL AND TRIM(base_address)  != ''
  GROUP BY user_id, base_address
  HAVING COUNT(DISTINCT customer_code) >= 3
),
-- 아티스트 2개 이상 구매
multi_artist AS (
  SELECT o.user_id
  FROM `makestar-dw.datamart.total_orders` o
  LEFT JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type = 'B2C'
    AND DATE(o.pay_date) >= '2025-01-01'
    AND e.artist_id IS NOT NULL
  GROUP BY o.user_id
  HAVING COUNT(DISTINCT e.artist_id) >= 2
),
-- 최종 구매대행 유저 목록
purchasing_users AS (
  SELECT DISTINCT CAST(p.user_id AS STRING) AS uid
  FROM purchasing_candidates p
  JOIN multi_artist m ON m.user_id = CAST(p.user_id AS STRING)
)
SELECT uid FROM purchasing_users
```

> `shipping_information` 데이터는 2025-01 이전 구간 신뢰도 낮음 → 기준일 `>= '2025-01-01'` 권장.
> 쿼리 전문 및 상위 유저 목록: `bq-analysis/queries/multi_account/01_purchasing_agent_detection.sql`

---

## 배송대행 탐지

해외 주문자가 한국 창고로 배송받는 패턴 + 키워드/코드/주소공유 필터.

```sql
-- Step 1: 배대지 기본 후보 (해외 주문 → 한국 배송)
WITH fwd_base AS (
  SELECT DISTINCT
    o.user_id,
    o.order_country_code,
    JSON_EXTRACT_SCALAR(c.shipping_information, '$.information.address')        AS addr,
    JSON_EXTRACT_SCALAR(c.shipping_information, '$.information.detail_address') AS detail,
    c.recipient_name
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.pg_mystarroom_public.tb_commerce_order` c ON c.order_number = o.order_no
  WHERE o.order_country_code  != 'KR'     -- 주문자가 해외
    AND o.shipping_country_code = 'KR'    -- 배송지는 한국 (배대지 창고)
    AND o.market_type           = 'B2C'
    AND o.channel_type          = '메이크스타웹'
    AND DATE(o.pay_date)       >= '2025-01-01'
    AND c.payment_status        = 'CONFIRMED'
),
-- Step 2: 동일 주소를 3명+ 공유하는 주소 = 배대지 창고
shared_addresses AS (
  SELECT addr
  FROM fwd_base
  WHERE addr IS NOT NULL
  GROUP BY addr
  HAVING COUNT(DISTINCT user_id) >= 3
),
-- Step 3: 키워드/코드패턴 OR 주소공유 해당 유저만 추출
forwarding_users AS (
  SELECT DISTINCT b.user_id
  FROM fwd_base b
  LEFT JOIN shared_addresses s ON s.addr = b.addr
  WHERE
    -- 배대지 서비스 키워드 (주소·상세주소·수취인명 통합 검색)
    REGEXP_CONTAINS(
      COALESCE(b.addr,'') || ' ' || COALESCE(b.detail,'') || ' ' || COALESCE(b.recipient_name,''),
      r'logistics|forwarding|warehouse|unun|물류|국제|배송대행|창고|글로벌|international|배대지|포워딩|album.?buddy'
    )
    -- 개인식별코드 패턴 (상세주소·수취인명)
    OR REGEXP_CONTAINS(
      COALESCE(b.detail,'') || ' ' || COALESCE(b.recipient_name,''),
      r'#[A-Z0-9]{4,}|[A-Z]{2,}[0-9]{5,}|Suite\s*[A-Z0-9]{3,}|(MZ|EK|DRV|TAI|SJH|MOI|PLT|SGN|KR2ME)-[0-9A-Z]{2,}'
    )
    -- 동일 주소 공유 (3명 이상)
    OR s.addr IS NOT NULL
)
SELECT DISTINCT user_id FROM forwarding_users
```

> 쿼리 전문: `bq-analysis/queries/multi_account/02_forwarding_agent_detection.sql`

---

## 구매대행·배송대행 분리 레이블 CTE

두 유형을 동시에 탐지하고 일반 유저와 구분할 때 사용하는 공통 패턴.

```sql
-- purchasing_users, forwarding_users CTE 위에서 정의된 이후
user_labels AS (
  SELECT
    u.user_id,
    CASE
      WHEN pu.uid IS NOT NULL THEN 'purchasing'  -- 구매대행
      WHEN fu.uid IS NOT NULL THEN 'forwarding'  -- 배송대행
      ELSE 'general'                             -- 일반
    END AS user_type
  FROM (
    SELECT DISTINCT user_id FROM `makestar-dw.datamart.total_orders`
    WHERE market_type = 'B2C' AND channel_type = '메이크스타웹'
      AND DATE(pay_date) >= '2025-01-01'
  ) u
  LEFT JOIN purchasing_users pu ON pu.uid = u.user_id
  LEFT JOIN forwarding_users fu ON fu.uid = u.user_id
)
```

## 월별 GMV / PU

```sql
SELECT
  FORMAT_DATE('%Y-%m', DATE(pay_date, 'Asia/Seoul')) AS month,
  SUM(total_revenue)          AS gmv,
  COUNT(DISTINCT user_id)     AS pu,
  SAFE_DIVIDE(SUM(total_revenue), COUNT(DISTINCT user_id)) AS arppu
FROM `makestar-dw.datamart.total_orders`
WHERE market_type IN ('B2C','B2B')
  AND DATE(pay_date, 'Asia/Seoul') >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```

---

## 유저 세그먼트 분류 CTE

```sql
WITH user_segment AS (
  SELECT
    user_id,
    SUM(total_revenue) AS ltv,
    MAX(DATE(pay_date, 'Asia/Seoul')) AS last_pay_date,
    ARRAY_AGG(event_id IGNORE NULLS ORDER BY pay_date DESC LIMIT 1)[SAFE_OFFSET(0)] AS last_event_id,
    CASE
      WHEN SUM(total_revenue) < 200000  THEN 'Light'
      WHEN SUM(total_revenue) < 1000000 THEN 'Middle'
      ELSE 'Whale'
    END AS segment
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C','B2B')
  GROUP BY user_id
)
```

---

## 이탈 유저 식별

```sql
WITH churned AS (
  SELECT
    user_id,
    segment,
    last_pay_date,
    last_event_id
  FROM user_segment
  WHERE DATE_DIFF(CURRENT_DATE(), last_pay_date, DAY) >= 90
)
```

---

## 이탈 후 후속 이벤트 유무 (이탈 원인 분류)

```sql
WITH churn_with_event AS (
  SELECT
    c.*,
    e.artist_id,
    e.sales_end_at AS last_event_end,
    (
      SELECT COUNT(*)
      FROM `makestar-dw.datamart.events_` e2
      WHERE e2.artist_id = e.artist_id
        AND e2.sales_start_at > e.sales_end_at
        AND e2.sales_start_at <= DATE_ADD(c.last_pay_date, INTERVAL 365 DAY)
        AND e2.event_type = e.event_type
    ) AS same_type_cnt,
    (
      SELECT COUNT(*)
      FROM `makestar-dw.datamart.events_` e2
      WHERE e2.artist_id = e.artist_id
        AND e2.sales_start_at > e.sales_end_at
        AND e2.sales_start_at <= DATE_ADD(c.last_pay_date, INTERVAL 365 DAY)
    ) AS any_type_cnt
  FROM churned c
  LEFT JOIN `makestar-dw.datamart.events_` e ON e.event_id = c.last_event_id
)
```

---

## MAU (월별)

```sql
SELECT
  FORMAT_DATE('%Y-%m', report_date) AS month,
  COUNT(DISTINCT user_pseudo_id) AS mau
FROM `makestar-dw.datamart.customer_analysis_visit`
WHERE report_date >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```

---

## NRU (신규 가입자, 일별)

`is_certified = true` 기준. `tb_auth_log.log_type = 0` 아님.

```sql
SELECT
  DATE(created_at, 'Asia/Seoul') AS date,
  COUNT(*) AS nru
FROM `makestar-dw.pg_mystarroom_public.tb_auth_user`
WHERE is_certified = true
  AND DATE(created_at, 'Asia/Seoul') >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```
