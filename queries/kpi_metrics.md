# KPI 미집계 쿼리

현행 대시보드에 없는 KPI 쿼리 모음.
모든 쿼리는 BigQuery(`makestar-dw`) 기준.

---

## 1. Stickiness (DAU / MAU)

```sql
WITH monthly_dau AS (
  SELECT
    DATE_TRUNC(date, MONTH) AS month,
    AVG(SUM(dau)) OVER(PARTITION BY DATE_TRUNC(date, MONTH)) AS avg_dau
  FROM `makestar-dw.datamart.dau`
  WHERE date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 12 MONTH), MONTH)
    AND date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), MONTH)
  GROUP BY date
),
monthly_dau_agg AS (
  SELECT month, AVG(avg_dau) AS avg_dau
  FROM monthly_dau
  GROUP BY month
),
monthly_mau AS (
  SELECT
    DATE_TRUNC(report_date, MONTH) AS month,
    COUNT(DISTINCT user_pseudo_id) AS mau
  FROM `makestar-dw.datamart.customer_analysis_visit`
  WHERE report_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 12 MONTH), MONTH)
    AND report_date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), MONTH)
  GROUP BY 1
)
SELECT
  d.month,
  ROUND(d.avg_dau)                                      AS avg_dau,
  m.mau,
  ROUND(SAFE_DIVIDE(d.avg_dau, m.mau) * 100, 1)         AS stickiness_pct
FROM monthly_dau_agg d
JOIN monthly_mau m USING (month)
ORDER BY 1
```

---

## 2. 첫구매 전환율 (주간 NRU 코호트)

가입 주차 기준 코호트별로, 해당 주차 이후 첫 구매 전환율 집계.

```sql
WITH nru AS (
  SELECT
    id AS user_id,
    DATE_TRUNC(DATE(created_at, 'Asia/Seoul'), WEEK(MONDAY)) AS join_week
  FROM `makestar-dw.pg_mystarroom_public.tb_auth_user`
  WHERE is_certified = true
    AND DATE(created_at, 'Asia/Seoul') >= '2025-01-01'
    AND is_withdrawn = false
),
first_purchase AS (
  SELECT
    user_id,
    MIN(DATE(pay_date, 'Asia/Seoul')) AS first_pay_date
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C', 'B2B')
  GROUP BY 1
)
SELECT
  n.join_week,
  COUNT(DISTINCT n.user_id)                                                        AS nru,
  COUNT(DISTINCT f.user_id)                                                        AS converted,
  ROUND(SAFE_DIVIDE(COUNT(DISTINCT f.user_id), COUNT(DISTINCT n.user_id)) * 100, 1) AS conversion_rate_pct
FROM nru n
LEFT JOIN first_purchase f
  ON CAST(n.user_id AS STRING) = f.user_id
  AND f.first_pay_date >= n.join_week
ORDER BY 1
```

---

## 3. 라운드 참여율 (Round-to-Round Retention)

동일 아티스트의 연속 앨범(라운드) 구매 비율.
라운드 = `album_name` 단위, 순서는 최초 구매일 기준.

```sql
WITH user_artist_rounds AS (
  SELECT
    o.user_id,
    e.artist_id,
    e.album_name,
    MIN(DATE(o.pay_date, 'Asia/Seoul')) AS first_pay_in_round
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
    AND e.album_name IS NOT NULL
  GROUP BY 1, 2, 3
),
round_seq AS (
  -- 아티스트별 라운드 순서 (최초 구매일 기준)
  SELECT
    artist_id,
    album_name,
    ROW_NUMBER() OVER(
      PARTITION BY artist_id
      ORDER BY MIN(first_pay_in_round)
    ) AS round_num
  FROM user_artist_rounds
  GROUP BY artist_id, album_name
),
user_rounds AS (
  SELECT uar.user_id, uar.artist_id, rs.round_num
  FROM user_artist_rounds uar
  JOIN round_seq rs USING (artist_id, album_name)
),
consecutive AS (
  SELECT
    r1.round_num                        AS round_n,
    COUNT(DISTINCT r1.user_id)          AS round_n_users,
    COUNT(DISTINCT r2.user_id)          AS returned_next_round
  FROM user_rounds r1
  LEFT JOIN user_rounds r2
    ON  r1.user_id    = r2.user_id
    AND r1.artist_id  = r2.artist_id
    AND r2.round_num  = r1.round_num + 1
  GROUP BY 1
)
SELECT
  round_n,
  round_n_users,
  returned_next_round,
  ROUND(SAFE_DIVIDE(returned_next_round, round_n_users) * 100, 1) AS round_retention_pct
FROM consecutive
WHERE round_n <= 10  -- 10라운드까지만 표시
ORDER BY 1
```

---

## 4. 이탈율

이탈 정의: **후속 이벤트가 오픈됐음에도 미구매**.
단순 미구매 기간(N일)으로 집계하지 않음.

```sql
WITH last_purchase AS (
  -- 유저 × 아티스트별 마지막 구매
  SELECT
    o.user_id,
    e.artist_id,
    MAX(DATE(o.pay_date, 'Asia/Seoul'))                                                AS last_pay_date,
    ARRAY_AGG(o.event_id IGNORE NULLS ORDER BY o.pay_date DESC LIMIT 1)[SAFE_OFFSET(0)] AS last_event_id
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
  GROUP BY 1, 2
),
with_next_event AS (
  -- 후속 이벤트 오픈 여부 확인
  SELECT
    lp.user_id,
    lp.artist_id,
    lp.last_pay_date,
    MIN(DATE(e2.sales_start_at, 'Asia/Seoul')) AS next_event_open_date
  FROM last_purchase lp
  JOIN `makestar-dw.datamart.events_` e2
    ON  e2.artist_id = lp.artist_id
    AND DATE(e2.sales_start_at, 'Asia/Seoul') > lp.last_pay_date
  GROUP BY 1, 2, 3
),
with_return AS (
  -- 후속 이벤트 오픈 이후 재구매 여부
  SELECT
    wne.user_id,
    wne.artist_id,
    wne.last_pay_date,
    wne.next_event_open_date,
    MAX(DATE(o.pay_date, 'Asia/Seoul')) AS return_pay_date
  FROM with_next_event wne
  LEFT JOIN `makestar-dw.datamart.total_orders` o
    ON  o.user_id = wne.user_id
    AND DATE(o.pay_date, 'Asia/Seoul') > wne.next_event_open_date
  LEFT JOIN `makestar-dw.datamart.events_` e
    ON  o.event_id = e.event_id
    AND e.artist_id = wne.artist_id
  GROUP BY 1, 2, 3, 4
)
SELECT
  COUNT(DISTINCT user_id)                                                                          AS total_users_with_next_event,
  COUNT(DISTINCT CASE WHEN return_pay_date IS NULL THEN user_id END)                              AS churned_users,
  ROUND(
    SAFE_DIVIDE(
      COUNT(DISTINCT CASE WHEN return_pay_date IS NULL THEN user_id END),
      COUNT(DISTINCT user_id)
    ) * 100, 1
  )                                                                                                AS churn_rate_pct
FROM with_return
```

---

## 5. 복귀율

> ⚠️ 현재 이탈 풀로 측정 시 항상 0%가 나옴.
> 반드시 **과거 시점 이탈자** 기준으로 측정해야 의미 있는 수치 산출.

기준: 1년 전 시점에 이탈 상태였던 유저 중 그 이후 복귀한 비율.

```sql
DECLARE snapshot_date DATE DEFAULT DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 365 DAY);

WITH last_purchase_as_of AS (
  -- snapshot_date 기준 유저 × 아티스트별 마지막 구매
  SELECT
    o.user_id,
    e.artist_id,
    MAX(DATE(o.pay_date, 'Asia/Seoul'))                                                AS last_pay_date,
    ARRAY_AGG(o.event_id IGNORE NULLS ORDER BY o.pay_date DESC LIMIT 1)[SAFE_OFFSET(0)] AS last_event_id
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
    AND DATE(o.pay_date, 'Asia/Seoul') <= snapshot_date
  GROUP BY 1, 2
),
churned_as_of AS (
  -- snapshot_date 시점에 이미 후속 이벤트가 오픈됐으나 미구매 = 이탈
  SELECT lp.user_id, lp.artist_id, lp.last_pay_date
  FROM last_purchase_as_of lp
  WHERE EXISTS (
    SELECT 1
    FROM `makestar-dw.datamart.events_` e2
    WHERE e2.artist_id = lp.artist_id
      AND DATE(e2.sales_start_at, 'Asia/Seoul') > lp.last_pay_date
      AND DATE(e2.sales_start_at, 'Asia/Seoul') <= snapshot_date
  )
),
returned AS (
  -- snapshot_date 이후 재구매 여부
  SELECT DISTINCT c.user_id, c.artist_id
  FROM churned_as_of c
  JOIN `makestar-dw.datamart.total_orders` o
    ON  o.user_id = c.user_id
    AND DATE(o.pay_date, 'Asia/Seoul') > snapshot_date
  JOIN `makestar-dw.datamart.events_` e
    ON  o.event_id = e.event_id
    AND e.artist_id = c.artist_id
  WHERE o.market_type IN ('B2C', 'B2B')
)
SELECT
  COUNT(DISTINCT CONCAT(c.user_id, '_', c.artist_id))          AS churned_user_artist_pairs,
  COUNT(DISTINCT CONCAT(r.user_id, '_', r.artist_id))          AS returned_pairs,
  ROUND(
    SAFE_DIVIDE(
      COUNT(DISTINCT CONCAT(r.user_id, '_', r.artist_id)),
      COUNT(DISTINCT CONCAT(c.user_id, '_', c.artist_id))
    ) * 100, 1
  )                                                              AS return_rate_pct
FROM churned_as_of c
LEFT JOIN returned r USING (user_id, artist_id)
```
