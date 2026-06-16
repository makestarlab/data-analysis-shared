# 공통 SQL 패턴

## 구매대행 탐지

### 신규 구매대행 후보 탐지 (distinct_ip >= 30, 목록 미등록)

```sql
SELECT
  a.user_id,
  b.email,
  COUNT(DISTINCT a.ip_name)   AS distinct_ip,
  COUNT(DISTINCT a.order_no)  AS order_cnt,
  ROUND(SUM(a.total_revenue)) AS total_gmv
FROM `makestar-dw.datamart.total_orders` a
JOIN `makestar-dw.pg_mystarroom_public.tb_auth_user` b ON a.user_id = CAST(b.id AS STRING)
WHERE a.pay_date >= '2022-01-01'
  AND a.market_type = 'B2C'
  AND a.user_id NOT IN (
    -- 현재 알려진 구매대행 목록 (service.md 참조)
    '1876860','812307','1736734','621230','1302313','1902098','859600','969308',
    '1027784','1581799','797962','802866','1492647','781240','885795','1264675',
    '1001311','2116643','1659287','700815','1540460','1890901','1511280','1006060',
    '1606082','1552669','1913216','1138597','1284854','1504890','12526','944286',
    '945344','2046425','1545878','1600974','886898','1539934','1533310','911936',
    '1069252','971976','1658602','948579','1071325','1995221','1933087','636546',
    '1509180','1257147','2032775','1323619','1958765','864765','1994769','209076',
    '1608153','1312465','1355103','1248833','1506290','965150','1011224','1260938',
    '625886','939836','1870283','1347032','1939835','1973097','2022335','1335644',
    '1975403','646210','1542033','910047','1995697','882978','1252380','2159123',
    '867147','942107','1329252','71764','1845002','999056','809695','1604186',
    '1506617','1006091','870982','1895495','1052115','1313023','1254035','1063330',
    '2050980','1550897','1660416','1620875','946338','1482920','1253405','1502990',
    '91909','1738982','2114301','1005028','1513305','1874153','1267050','1354020',
    '1062950','905126','1071819','1935908','1073305','1247698','898061','943715',
    '1673444','1334025','1982712','1290379','1503928','1502504','2159410'
  )
GROUP BY a.user_id, b.email
HAVING COUNT(DISTINCT a.ip_name) >= 30
ORDER BY distinct_ip DESC, total_gmv DESC
```

### 확인된 구매대행의 이메일 도메인으로 동일 도메인 유저 검색

```sql
-- :target_email 자리에 확인된 구매대행 이메일 입력
-- 예: 'shipkorea.kpop@gmail.com' → gmail.com은 너무 넓으므로 비즈니스 도메인에만 유효

WITH target_domain AS (
  SELECT REGEXP_EXTRACT(:target_email, r'@(.+)') AS domain
),
domain_users AS (
  SELECT
    CAST(b.id AS STRING) AS user_id,
    b.email,
    COUNT(DISTINCT a.ip_name)   AS distinct_ip,
    COUNT(DISTINCT a.order_no)  AS order_cnt,
    ROUND(SUM(a.total_revenue)) AS total_gmv
  FROM `makestar-dw.pg_mystarroom_public.tb_auth_user` b
  LEFT JOIN `makestar-dw.datamart.total_orders` a ON CAST(b.id AS STRING) = a.user_id
    AND a.market_type = 'B2C'
  WHERE REGEXP_EXTRACT(b.email, r'@(.+)') = (SELECT domain FROM target_domain)
    AND REGEXP_EXTRACT(b.email, r'@(.+)') NOT IN ('gmail.com','naver.com','daum.net','hanmail.net','icloud.com','hotmail.com','yahoo.com','outlook.com','kakao.com')
  GROUP BY b.id, b.email
)
SELECT * FROM domain_users
WHERE order_cnt > 0
ORDER BY total_gmv DESC
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
