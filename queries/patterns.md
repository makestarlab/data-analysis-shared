# 공통 SQL 패턴

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

```sql
SELECT
  DATE(created_at, 'Asia/Seoul') AS date,
  COUNT(*) AS nru
FROM `makestar-dw.pg_mystarroom_public.tb_auth_log`
WHERE log_type = 0
  AND DATE(created_at, 'Asia/Seoul') >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```
