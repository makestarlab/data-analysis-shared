# KPI 쿼리 모음

KPI 트리 전체 지표 쿼리. BigQuery(`makestar-dw`) 기준.
⚠️ = 데이터 미확보(Pending), 🔲 = 집계 미구현

---

## 매출 (GMV)

### 월별 GMV / PU / ARPPU

```sql
SELECT
  FORMAT_DATE('%Y-%m', DATE(pay_date, 'Asia/Seoul'))             AS month,
  SUM(total_revenue)                                             AS gmv,
  COUNT(DISTINCT user_id)                                        AS pu,
  SAFE_DIVIDE(SUM(total_revenue), COUNT(DISTINCT user_id))       AS arppu
FROM `makestar-dw.datamart.total_orders`
WHERE market_type IN ('B2C', 'B2B')
  AND DATE(pay_date, 'Asia/Seoul') >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```

### 주별 GMV / PU / ARPPU

```sql
SELECT
  DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), WEEK(MONDAY))         AS pay_week,
  SUM(total_revenue)                                             AS gmv,
  COUNT(DISTINCT user_id)                                        AS pu,
  SAFE_DIVIDE(SUM(total_revenue), COUNT(DISTINCT user_id))       AS arppu
FROM `makestar-dw.datamart.total_orders`
WHERE market_type IN ('B2C', 'B2B')
  AND DATE(pay_date, 'Asia/Seoul') >= DATE_ADD(
        DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -20 WEEK)
  AND DATE(pay_date, 'Asia/Seoul') < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
GROUP BY 1
ORDER BY 1
```

---

## 매출 분해 — 대분류 (market_type)

### 주별 대분류별 GMV

```sql
SELECT
  DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), WEEK(MONDAY))         AS pay_week,
  market_type,
  SUM(total_revenue)                                             AS gmv,
  COUNT(DISTINCT user_id)                                        AS pu
FROM `makestar-dw.datamart.total_orders`
WHERE DATE(pay_date, 'Asia/Seoul') >= DATE_ADD(
        DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -20 WEEK)
  AND DATE(pay_date, 'Asia/Seoul') < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
GROUP BY 1, 2
ORDER BY 1, 2
```

### 대분류별 주간 증감 (지난주 vs 그전주 vs 52주 평균)

```sql
WITH weekly AS (
  SELECT
    DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), WEEK(MONDAY))       AS pay_week,
    market_type,
    SUM(total_revenue)                                           AS gmv
  FROM `makestar-dw.datamart.total_orders`
  WHERE DATE(pay_date, 'Asia/Seoul') >= DATE_ADD(
          DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -52 WEEK)
    AND DATE(pay_date, 'Asia/Seoul') < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
  GROUP BY 1, 2
),
last_week  AS (SELECT DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -1 WEEK) AS wk),
prev_week  AS (SELECT DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -2 WEEK) AS wk),
summary AS (
  SELECT
    market_type,
    SUM(IF(pay_week = (SELECT wk FROM last_week), gmv, 0))       AS last_week_gmv,
    SUM(IF(pay_week = (SELECT wk FROM prev_week), gmv, 0))       AS prev_week_gmv,
    SUM(gmv) / 52                                                AS avg_weekly_gmv
  FROM weekly
  GROUP BY 1
),
grand_total AS (
  SELECT '총계' AS market_type,
    SUM(IF(pay_week = (SELECT wk FROM last_week), gmv, 0))       AS last_week_gmv,
    SUM(IF(pay_week = (SELECT wk FROM prev_week), gmv, 0))       AS prev_week_gmv,
    SUM(gmv) / 52                                                AS avg_weekly_gmv
  FROM weekly
)
SELECT
  market_type                                                    AS `대분류`,
  ROUND(last_week_gmv)                                          AS `지난주 GMV`,
  ROUND(prev_week_gmv)                                          AS `그전주 GMV`,
  CONCAT(CAST(ROUND(SAFE_DIVIDE(last_week_gmv - prev_week_gmv, prev_week_gmv) * 100) AS INT64), '%')
                                                                 AS `전주 대비`,
  ROUND(avg_weekly_gmv)                                         AS `주평균_52주`
FROM (SELECT * FROM grand_total UNION ALL SELECT * FROM summary)
ORDER BY CASE market_type WHEN '총계' THEN 0 WHEN 'B2C' THEN 1 WHEN 'B2B' THEN 2 ELSE 3 END
```

---

## 매출 분해 — B2C 사업별 (biz_type)

### 주별 B2C 사업별 GMV

```sql
SELECT
  DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), WEEK(MONDAY))         AS pay_week,
  biz_type,
  SUM(total_revenue)                                             AS gmv,
  COUNT(DISTINCT user_id)                                        AS pu,
  SAFE_DIVIDE(SUM(total_revenue), COUNT(DISTINCT user_id))       AS arppu
FROM `makestar-dw.datamart.total_orders`
WHERE market_type = 'B2C'
  AND DATE(pay_date, 'Asia/Seoul') >= DATE_ADD(
        DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -20 WEEK)
  AND DATE(pay_date, 'Asia/Seoul') < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
GROUP BY 1, 2
ORDER BY 1, 2
```

### B2C 사업별 주간 증감

```sql
WITH weekly AS (
  SELECT
    DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), WEEK(MONDAY))       AS pay_week,
    biz_type,
    SUM(total_revenue)                                           AS gmv
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type = 'B2C'
    AND DATE(pay_date, 'Asia/Seoul') >= DATE_ADD(
          DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -52 WEEK)
    AND DATE(pay_date, 'Asia/Seoul') < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
  GROUP BY 1, 2
),
last_week  AS (SELECT DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -1 WEEK) AS wk),
prev_week  AS (SELECT DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -2 WEEK) AS wk),
summary AS (
  SELECT
    biz_type,
    SUM(IF(pay_week = (SELECT wk FROM last_week), gmv, 0))       AS last_week_gmv,
    SUM(IF(pay_week = (SELECT wk FROM prev_week), gmv, 0))       AS prev_week_gmv,
    SUM(gmv) / 52                                                AS avg_weekly_gmv
  FROM weekly
  GROUP BY 1
),
grand_total AS (
  SELECT '총계' AS biz_type,
    SUM(IF(pay_week = (SELECT wk FROM last_week), gmv, 0))       AS last_week_gmv,
    SUM(IF(pay_week = (SELECT wk FROM prev_week), gmv, 0))       AS prev_week_gmv,
    SUM(gmv) / 52                                                AS avg_weekly_gmv
  FROM weekly
)
SELECT
  biz_type                                                       AS `B2C 사업`,
  ROUND(last_week_gmv)                                          AS `지난주 GMV`,
  ROUND(prev_week_gmv)                                          AS `그전주 GMV`,
  CONCAT(CAST(ROUND(SAFE_DIVIDE(last_week_gmv - prev_week_gmv, prev_week_gmv) * 100) AS INT64), '%')
                                                                 AS `전주 대비`,
  ROUND(avg_weekly_gmv)                                         AS `주평균_52주`
FROM (SELECT * FROM grand_total UNION ALL SELECT * FROM summary)
ORDER BY CASE biz_type
  WHEN '총계'       THEN 0 WHEN '한국(이벤트)' THEN 1 WHEN '한국(매장)' THEN 2
  WHEN '중국'       THEN 3 WHEN 'APAC'        THEN 4 WHEN '일본'       THEN 5
  WHEN '미주유럽'   THEN 6 WHEN '쇼핑'         THEN 7 ELSE 8 END
```

---

## PUR (구매전환율)

PUR = PU / MAU. 월별 집계.

```sql
WITH monthly_pu AS (
  SELECT
    DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), MONTH)              AS month,
    COUNT(DISTINCT user_id)                                      AS pu
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C', 'B2B')
    AND DATE(pay_date, 'Asia/Seoul') >= '2025-01-01'
  GROUP BY 1
),
monthly_mau AS (
  SELECT
    DATE_TRUNC(report_date, MONTH)                               AS month,
    COUNT(DISTINCT user_pseudo_id)                               AS mau
  FROM `makestar-dw.datamart.customer_analysis_visit`
  WHERE report_date >= '2025-01-01'
  GROUP BY 1
)
SELECT
  p.month,
  p.pu,
  m.mau,
  ROUND(SAFE_DIVIDE(p.pu, m.mau) * 100, 1)                      AS pur_pct
FROM monthly_pu p
JOIN monthly_mau m USING (month)
ORDER BY 1
```

---

## Growth (신규 유입)

### 주별 NRU (서비스별)

```sql
SELECT
  DATE_TRUNC(DATE(created_at, 'Asia/Seoul'), WEEK(MONDAY))       AS join_week,
  CASE
    WHEN created_from IN ('STREAMWITH','POCADB','FANS','KPOPMATE','CALENDOL','JOGIYO')
    THEN 'New Biz'
    ELSE created_from
  END                                                            AS service,
  COUNT(*)                                                       AS nru
FROM `makestar-dw.pg_mystarroom_public.tb_auth_user`
WHERE is_certified = true
  AND DATE(created_at, 'Asia/Seoul') >= '2025-01-01'
  AND DATE(created_at, 'Asia/Seoul') < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
  AND created_from NOT IN ('UNKNOWN', 'VOTE', 'SYSTEM')
GROUP BY 1, 2
ORDER BY 1, 2
```

### 첫구매 전환율 (주간 NRU 코호트)

```sql
WITH nru AS (
  SELECT
    id                                                           AS user_id,
    DATE_TRUNC(DATE(created_at, 'Asia/Seoul'), WEEK(MONDAY))     AS join_week
  FROM `makestar-dw.pg_mystarroom_public.tb_auth_user`
  WHERE is_certified = true
    AND is_withdrawn = false
    AND DATE(created_at, 'Asia/Seoul') >= '2025-01-01'
),
first_purchase AS (
  SELECT
    user_id,
    MIN(DATE(pay_date, 'Asia/Seoul'))                            AS first_pay_date
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C', 'B2B')
  GROUP BY 1
)
SELECT
  n.join_week,
  COUNT(DISTINCT n.user_id)                                      AS nru,
  COUNT(DISTINCT f.user_id)                                      AS converted,
  ROUND(SAFE_DIVIDE(COUNT(DISTINCT f.user_id),
        COUNT(DISTINCT n.user_id)) * 100, 1)                    AS conversion_rate_pct
FROM nru n
LEFT JOIN first_purchase f
  ON  CAST(n.user_id AS STRING) = f.user_id
  AND f.first_pay_date >= n.join_week
ORDER BY 1
```

---

## Engagement (활성도)

### DAU

```sql
SELECT
  date,
  SUM(dau)                                                       AS dau
FROM `makestar-dw.datamart.dau`
WHERE date >= DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 90 DAY)
  AND date < CURRENT_DATE('Asia/Seoul')
GROUP BY 1
ORDER BY 1
```

### WAU

```sql
SELECT
  date,
  SUM(wau)                                                       AS wau
FROM `makestar-dw.datamart.wau`
WHERE date >= DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -53 WEEK)
  AND date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
GROUP BY 1
ORDER BY 1
```

### MAU

```sql
SELECT
  DATE_TRUNC(report_date, MONTH)                                 AS month,
  COUNT(DISTINCT user_pseudo_id)                                 AS mau
FROM `makestar-dw.datamart.customer_analysis_visit`
WHERE report_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 12 MONTH), MONTH)
  AND report_date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), MONTH)
GROUP BY 1
ORDER BY 1
```

### Stickiness (DAU / MAU)

```sql
WITH monthly_dau AS (
  SELECT
    DATE_TRUNC(date, MONTH)                                      AS month,
    AVG(SUM(dau)) OVER(PARTITION BY DATE_TRUNC(date, MONTH))     AS avg_dau
  FROM `makestar-dw.datamart.dau`
  WHERE date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 12 MONTH), MONTH)
    AND date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), MONTH)
  GROUP BY date
),
monthly_dau_agg AS (
  SELECT month, AVG(avg_dau) AS avg_dau FROM monthly_dau GROUP BY 1
),
monthly_mau AS (
  SELECT
    DATE_TRUNC(report_date, MONTH)                               AS month,
    COUNT(DISTINCT user_pseudo_id)                               AS mau
  FROM `makestar-dw.datamart.customer_analysis_visit`
  WHERE report_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 12 MONTH), MONTH)
    AND report_date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), MONTH)
  GROUP BY 1
)
SELECT
  d.month,
  ROUND(d.avg_dau)                                              AS avg_dau,
  m.mau,
  ROUND(SAFE_DIVIDE(d.avg_dau, m.mau) * 100, 1)                AS stickiness_pct
FROM monthly_dau_agg d
JOIN monthly_mau m USING (month)
ORDER BY 1
```

### PDP 방문 Top 5 (주별)

```sql
WITH visitor AS (
  SELECT
    DATE_TRUNC(event_date, WEEK(MONDAY))                         AS pay_week,
    i.product_event_code,
    i.product_event_name,
    COUNT(DISTINCT v.user_pseudo_id)                             AS visitors
  FROM `makestar-dw.datamart.vw_commerce_events_visitor_segment` v
  JOIN (
    SELECT DISTINCT product_event_id, product_event_code, product_event_name
    FROM `makestar-dw.datamart.vw_commerce_items`
  ) i ON REGEXP_EXTRACT(v.page_path, r'/product/(\d+)') = i.product_event_id
  WHERE event_name = 'session_start'
    AND event_date >= DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -12 WEEK)
    AND event_date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
  GROUP BY 1, 2, 3
)
SELECT
  pay_week,
  product_event_name                                             AS pdp,
  visitors
FROM visitor
QUALIFY ROW_NUMBER() OVER(PARTITION BY pay_week ORDER BY visitors DESC) <= 5
ORDER BY 1, visitors DESC
```

---

## Retention (유지)

### 라운드 참여율 (Round-to-Round Retention)

동일 아티스트의 연속 앨범 구매 비율. `album_name` 기준 라운드.

```sql
WITH user_artist_rounds AS (
  SELECT
    o.user_id,
    e.artist_id,
    e.album_name,
    MIN(DATE(o.pay_date, 'Asia/Seoul'))                          AS first_pay_in_round
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
    AND e.album_name IS NOT NULL
  GROUP BY 1, 2, 3
),
round_seq AS (
  SELECT
    artist_id,
    album_name,
    ROW_NUMBER() OVER(
      PARTITION BY artist_id
      ORDER BY MIN(first_pay_in_round)
    )                                                            AS round_num
  FROM user_artist_rounds
  GROUP BY 1, 2
),
user_rounds AS (
  SELECT uar.user_id, uar.artist_id, rs.round_num
  FROM user_artist_rounds uar
  JOIN round_seq rs USING (artist_id, album_name)
),
consecutive AS (
  SELECT
    r1.round_num                                                 AS round_n,
    COUNT(DISTINCT r1.user_id)                                   AS round_n_users,
    COUNT(DISTINCT r2.user_id)                                   AS returned_next_round
  FROM user_rounds r1
  LEFT JOIN user_rounds r2
    ON  r1.user_id   = r2.user_id
    AND r1.artist_id = r2.artist_id
    AND r2.round_num = r1.round_num + 1
  GROUP BY 1
)
SELECT
  round_n,
  round_n_users,
  returned_next_round,
  ROUND(SAFE_DIVIDE(returned_next_round, round_n_users) * 100, 1) AS round_retention_pct
FROM consecutive
WHERE round_n <= 10
ORDER BY 1
```

### 이탈율

이탈 = 후속 이벤트 오픈 후에도 미구매.
단순 미구매 기간(N일)으로 집계하지 않음.

```sql
WITH last_purchase AS (
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
  SELECT
    lp.user_id,
    lp.artist_id,
    lp.last_pay_date,
    MIN(DATE(e2.sales_start_at, 'Asia/Seoul'))                   AS next_event_open_date
  FROM last_purchase lp
  JOIN `makestar-dw.datamart.events_` e2
    ON  e2.artist_id = lp.artist_id
    AND DATE(e2.sales_start_at, 'Asia/Seoul') > lp.last_pay_date
  GROUP BY 1, 2, 3
),
with_return AS (
  SELECT
    wne.user_id,
    wne.artist_id,
    wne.last_pay_date,
    wne.next_event_open_date,
    MAX(DATE(o.pay_date, 'Asia/Seoul'))                          AS return_pay_date
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
  COUNT(DISTINCT user_id)                                                              AS total_users_with_next_event,
  COUNT(DISTINCT CASE WHEN return_pay_date IS NULL THEN user_id END)                  AS churned_users,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN return_pay_date IS NULL THEN user_id END),
    COUNT(DISTINCT user_id)
  ) * 100, 1)                                                                         AS churn_rate_pct
FROM with_return
```

### 복귀율

> ⚠️ 현재 이탈 풀로 측정 시 항상 0% — 반드시 **과거 시점 이탈자** 기준으로 측정.

```sql
DECLARE snapshot_date DATE DEFAULT DATE_SUB(CURRENT_DATE('Asia/Seoul'), INTERVAL 365 DAY);

WITH last_purchase_as_of AS (
  SELECT
    o.user_id,
    e.artist_id,
    MAX(DATE(o.pay_date, 'Asia/Seoul'))                                                AS last_pay_date
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
    AND DATE(o.pay_date, 'Asia/Seoul') <= snapshot_date
  GROUP BY 1, 2
),
churned_as_of AS (
  -- snapshot_date 시점에 후속 이벤트가 열렸으나 미구매
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
  COUNT(DISTINCT CONCAT(c.user_id, '_', c.artist_id))           AS churned_user_artist_pairs,
  COUNT(DISTINCT CONCAT(r.user_id, '_', r.artist_id))           AS returned_pairs,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CONCAT(r.user_id, '_', r.artist_id)),
    COUNT(DISTINCT CONCAT(c.user_id, '_', c.artist_id))
  ) * 100, 1)                                                   AS return_rate_pct
FROM churned_as_of c
LEFT JOIN returned r USING (user_id, artist_id)
```

---

## 아티스트별 매출

### 아티스트 × 라운드별 GMV / PU / ARPPU / 판매량

```sql
WITH artist_round_sales AS (
  SELECT
    e.artist_id,
    e.album_name,
    MIN(DATE(e.sales_start_at, 'Asia/Seoul'))                    AS round_open_date,
    SUM(o.total_revenue)                                         AS gmv,
    SUM(o.order_album_qty)                                       AS album_qty,
    COUNT(DISTINCT o.user_id)                                    AS pu,
    SAFE_DIVIDE(SUM(o.total_revenue), COUNT(DISTINCT o.user_id)) AS arppu
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
    AND e.album_name IS NOT NULL
  GROUP BY 1, 2
),
round_seq AS (
  SELECT
    artist_id,
    album_name,
    ROW_NUMBER() OVER(
      PARTITION BY artist_id ORDER BY MIN(round_open_date)
    )                                                            AS round_num
  FROM artist_round_sales
  GROUP BY 1, 2
),
artist_name AS (
  -- artist_id → artist_name 정규화 (vw_commerce_items_v2 기준)
  SELECT DISTINCT artist_id, artist_name
  FROM `makestar-dw.datamart.vw_commerce_items_v2`
  WHERE artist_id IS NOT NULL AND artist_name IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY artist_name) = 1
)
SELECT
  ars.artist_id,
  an.artist_name,
  rs.round_num,
  ars.album_name                                                 AS round_name,
  ars.round_open_date,
  ROUND(ars.gmv)                                                AS gmv,
  ars.pu,
  ROUND(ars.arppu)                                              AS arppu,
  ROUND(ars.album_qty)                                          AS album_qty
FROM artist_round_sales ars
JOIN round_seq rs USING (artist_id, album_name)
LEFT JOIN artist_name an USING (artist_id)
ORDER BY ars.gmv DESC, rs.round_num
```

---

### 아티스트별 라운드 간 증감 (N vs N-1)

```sql
WITH artist_round_sales AS (
  SELECT
    e.artist_id,
    e.album_name,
    MIN(DATE(e.sales_start_at, 'Asia/Seoul'))                    AS round_open_date,
    SUM(o.total_revenue)                                         AS gmv,
    SUM(o.order_album_qty)                                       AS album_qty,
    COUNT(DISTINCT o.user_id)                                    AS pu,
    SAFE_DIVIDE(SUM(o.total_revenue), COUNT(DISTINCT o.user_id)) AS arppu
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
    AND e.album_name IS NOT NULL
  GROUP BY 1, 2
),
round_seq AS (
  SELECT
    artist_id, album_name,
    ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY MIN(round_open_date)) AS round_num
  FROM artist_round_sales
  GROUP BY 1, 2
),
artist_name AS (
  SELECT DISTINCT artist_id, artist_name
  FROM `makestar-dw.datamart.vw_commerce_items_v2`
  WHERE artist_id IS NOT NULL AND artist_name IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY artist_name) = 1
),
base AS (
  SELECT
    ars.artist_id,
    an.artist_name,
    rs.round_num,
    ars.album_name                                               AS round_name,
    ars.round_open_date,
    ars.gmv,
    ars.pu,
    ars.arppu,
    ars.album_qty
  FROM artist_round_sales ars
  JOIN round_seq rs USING (artist_id, album_name)
  LEFT JOIN artist_name an USING (artist_id)
)
SELECT
  artist_id,
  artist_name,
  round_num,
  round_name,
  round_open_date,
  ROUND(gmv)                                                    AS gmv,
  ROUND(LAG(gmv) OVER(PARTITION BY artist_id ORDER BY round_num)) AS prev_gmv,
  CONCAT(CAST(ROUND(SAFE_DIVIDE(
    gmv - LAG(gmv) OVER(PARTITION BY artist_id ORDER BY round_num),
    LAG(gmv) OVER(PARTITION BY artist_id ORDER BY round_num)
  ) * 100) AS INT64), '%')                                      AS gmv_growth,
  pu,
  LAG(pu) OVER(PARTITION BY artist_id ORDER BY round_num)       AS prev_pu,
  CONCAT(CAST(ROUND(SAFE_DIVIDE(
    pu - LAG(pu) OVER(PARTITION BY artist_id ORDER BY round_num),
    LAG(pu) OVER(PARTITION BY artist_id ORDER BY round_num)
  ) * 100) AS INT64), '%')                                      AS pu_growth,
  ROUND(arppu)                                                  AS arppu,
  ROUND(album_qty)                                              AS album_qty
FROM base
ORDER BY gmv DESC, round_num
```

---

### 특정 아티스트 라운드별 상세 (아티스트 지정)

```sql
DECLARE target_artist_id STRING DEFAULT 'A001';  -- artist_id로 교체

WITH event_sales AS (
  SELECT
    e.event_id,
    e.event_name,
    e.album_name,
    e.event_order,
    e.event_type,
    DATE(e.sales_start_at, 'Asia/Seoul')                         AS open_date,
    DATE(e.sales_end_at, 'Asia/Seoul')                           AS close_date,
    SUM(o.total_revenue)                                         AS gmv,
    SUM(o.order_album_qty)                                       AS album_qty,
    COUNT(DISTINCT o.user_id)                                    AS pu,
    SAFE_DIVIDE(SUM(o.total_revenue), COUNT(DISTINCT o.user_id)) AS arppu
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id = target_artist_id
  GROUP BY 1, 2, 3, 4, 5, 6, 7
),
round_seq AS (
  SELECT DISTINCT album_name,
    ROW_NUMBER() OVER(ORDER BY MIN(open_date)) AS round_num
  FROM event_sales
  GROUP BY album_name
)
SELECT
  rs.round_num,
  es.album_name                                                  AS round_name,
  es.event_order,
  es.event_type,
  es.event_name,
  es.open_date,
  es.close_date,
  ROUND(es.gmv)                                                 AS gmv,
  es.pu,
  ROUND(es.arppu)                                               AS arppu,
  ROUND(es.album_qty)                                           AS album_qty
FROM event_sales es
JOIN round_seq rs USING (album_name)
ORDER BY rs.round_num, es.event_order
```

---

## 이벤트 타입별 매출

### 월별 이벤트 타입별 GMV

```sql
SELECT
  DATE_TRUNC(DATE(o.pay_date, 'Asia/Seoul'), MONTH)              AS month,
  e.event_type,
  SUM(o.total_revenue)                                           AS gmv,
  COUNT(DISTINCT o.user_id)                                      AS pu,
  COUNT(DISTINCT o.event_id)                                     AS event_count,
  SAFE_DIVIDE(SUM(o.total_revenue), COUNT(DISTINCT o.event_id))  AS gmv_per_event,
  SAFE_DIVIDE(SUM(o.total_revenue), COUNT(DISTINCT o.user_id))   AS arppu
FROM `makestar-dw.datamart.total_orders` o
JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
WHERE o.market_type IN ('B2C', 'B2B')
  AND e.event_type IS NOT NULL
  AND DATE(o.pay_date, 'Asia/Seoul') >= '2025-01-01'
GROUP BY 1, 2
ORDER BY 1, 3 DESC
```

### 아티스트 × 이벤트 타입별 GMV

```sql
WITH artist_name AS (
  SELECT DISTINCT artist_id, artist_name
  FROM `makestar-dw.datamart.vw_commerce_items_v2`
  WHERE artist_id IS NOT NULL AND artist_name IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY artist_name) = 1
)
SELECT
  e.artist_id,
  an.artist_name,
  e.event_type,
  SUM(o.total_revenue)                                           AS gmv,
  COUNT(DISTINCT o.order_no)                                     AS order_count,
  COUNT(DISTINCT o.user_id)                                      AS pu,
  SAFE_DIVIDE(SUM(o.total_revenue), COUNT(DISTINCT o.user_id))   AS arppu,
  SUM(o.order_album_qty)                                         AS album_qty
FROM `makestar-dw.datamart.total_orders` o
JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
LEFT JOIN artist_name an USING (artist_id)
WHERE o.market_type IN ('B2C', 'B2B')
  AND e.artist_id IS NOT NULL
  AND e.event_type IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY 4 DESC
```

---

## 주문/유저 단위 지표

### 주문당 단가 (AOV)

```sql
SELECT
  DATE_TRUNC(DATE(pay_date, 'Asia/Seoul'), MONTH)                AS month,
  COUNT(DISTINCT order_no)                                       AS order_count,
  ROUND(SAFE_DIVIDE(SUM(total_revenue),
        COUNT(DISTINCT order_no)))                               AS aov,
  ROUND(SAFE_DIVIDE(SUM(product_revenue),
        COUNT(DISTINCT order_no)))                               AS product_aov,
  ROUND(SAFE_DIVIDE(SUM(shipping_revenue),
        COUNT(DISTINCT order_no)))                               AS shipping_aov
FROM `makestar-dw.datamart.total_orders`
WHERE market_type IN ('B2C', 'B2B')
  AND DATE(pay_date, 'Asia/Seoul') >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```

### 유저당 최대 · 평균 · 분위 매출

```sql
WITH user_revenue AS (
  SELECT
    user_id,
    SUM(total_revenue)    AS ltv,
    COUNT(DISTINCT order_no) AS order_count
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C', 'B2B')
  GROUP BY 1
)
SELECT
  COUNT(*)                                                       AS total_users,
  ROUND(MAX(ltv))                                               AS max_user_revenue,
  ROUND(AVG(ltv))                                               AS avg_user_revenue,
  ROUND(APPROX_QUANTILES(ltv, 100)[OFFSET(50)])                 AS median_user_revenue,
  ROUND(APPROX_QUANTILES(ltv, 100)[OFFSET(75)])                 AS p75_user_revenue,
  ROUND(APPROX_QUANTILES(ltv, 100)[OFFSET(90)])                 AS p90_user_revenue,
  ROUND(APPROX_QUANTILES(ltv, 100)[OFFSET(99)])                 AS p99_user_revenue,
  ROUND(AVG(order_count), 1)                                    AS avg_orders_per_user
FROM user_revenue
```

### 아티스트별 유저당 최대 · 평균 매출

```sql
WITH artist_name AS (
  SELECT DISTINCT artist_id, artist_name
  FROM `makestar-dw.datamart.vw_commerce_items_v2`
  WHERE artist_id IS NOT NULL AND artist_name IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY artist_name) = 1
),
user_artist_revenue AS (
  SELECT
    o.user_id,
    e.artist_id,
    SUM(o.total_revenue)     AS revenue,
    COUNT(DISTINCT o.order_no) AS order_count
  FROM `makestar-dw.datamart.total_orders` o
  JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
  WHERE o.market_type IN ('B2C', 'B2B')
    AND e.artist_id IS NOT NULL
  GROUP BY 1, 2
)
SELECT
  uar.artist_id,
  an.artist_name,
  COUNT(DISTINCT uar.user_id)                                    AS pu,
  ROUND(SUM(uar.revenue))                                       AS gmv,
  ROUND(MAX(uar.revenue))                                       AS max_user_revenue,
  ROUND(AVG(uar.revenue))                                       AS avg_user_revenue,
  ROUND(APPROX_QUANTILES(uar.revenue, 100)[OFFSET(50)])         AS median_user_revenue,
  ROUND(AVG(uar.order_count), 1)                                AS avg_orders_per_user
FROM user_artist_revenue uar
LEFT JOIN artist_name an USING (artist_id)
GROUP BY 1, 2
ORDER BY 4 DESC
```

---

## 아티스트 × 이벤트별 상세

### 아티스트 × 이벤트별 전체 지표

```sql
WITH artist_name AS (
  SELECT DISTINCT artist_id, artist_name
  FROM `makestar-dw.datamart.vw_commerce_items_v2`
  WHERE artist_id IS NOT NULL AND artist_name IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY artist_name) = 1
),
round_seq AS (
  SELECT
    artist_id,
    album_name,
    ROW_NUMBER() OVER(
      PARTITION BY artist_id
      ORDER BY MIN(DATE(sales_start_at, 'Asia/Seoul'))
    )                                                            AS round_num
  FROM `makestar-dw.datamart.events_`
  WHERE artist_id IS NOT NULL AND album_name IS NOT NULL
  GROUP BY 1, 2
)
SELECT
  e.artist_id,
  an.artist_name,
  rs.round_num,
  e.album_name                                                   AS round_name,
  e.event_order,
  e.event_type,
  e.event_id,
  e.event_name,
  DATE(e.sales_start_at, 'Asia/Seoul')                           AS open_date,
  DATE(e.sales_end_at, 'Asia/Seoul')                             AS close_date,
  ROUND(SUM(o.total_revenue))                                   AS gmv,
  COUNT(DISTINCT o.order_no)                                     AS order_count,
  ROUND(SAFE_DIVIDE(SUM(o.total_revenue),
        COUNT(DISTINCT o.order_no)))                             AS aov,
  COUNT(DISTINCT o.user_id)                                      AS pu,
  ROUND(SAFE_DIVIDE(SUM(o.total_revenue),
        COUNT(DISTINCT o.user_id)))                              AS arppu,
  ROUND(MAX(SUM(o.total_revenue)) OVER(
    PARTITION BY e.artist_id, o.user_id))                        AS max_user_revenue,
  ROUND(SUM(o.order_album_qty))                                 AS album_qty
FROM `makestar-dw.datamart.total_orders` o
JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
LEFT JOIN artist_name an USING (artist_id)
LEFT JOIN round_seq rs USING (artist_id, album_name)
WHERE o.market_type IN ('B2C', 'B2B')
  AND e.artist_id IS NOT NULL
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
ORDER BY gmv DESC
```

### 특정 아티스트 이벤트별 라운드 비교 (세로)

```sql
DECLARE target_artist_id STRING DEFAULT 'A001';

WITH round_seq AS (
  SELECT album_name,
    ROW_NUMBER() OVER(ORDER BY MIN(DATE(sales_start_at, 'Asia/Seoul'))) AS round_num
  FROM `makestar-dw.datamart.events_`
  WHERE artist_id = target_artist_id AND album_name IS NOT NULL
  GROUP BY 1
)
SELECT
  rs.round_num,
  e.album_name                                                   AS round_name,
  e.event_order,
  e.event_type,
  DATE(e.sales_start_at, 'Asia/Seoul')                           AS open_date,
  ROUND(SUM(o.total_revenue))                                   AS gmv,
  ROUND(LAG(SUM(o.total_revenue)) OVER(
    PARTITION BY e.album_name ORDER BY e.event_order))           AS prev_event_gmv,
  COUNT(DISTINCT o.order_no)                                     AS order_count,
  ROUND(SAFE_DIVIDE(SUM(o.total_revenue),
        COUNT(DISTINCT o.order_no)))                             AS aov,
  COUNT(DISTINCT o.user_id)                                      AS pu,
  ROUND(SAFE_DIVIDE(SUM(o.total_revenue),
        COUNT(DISTINCT o.user_id)))                              AS arppu,
  ROUND(MAX(o.total_revenue))                                   AS max_order_amount,
  ROUND(SUM(o.order_album_qty))                                 AS album_qty
FROM `makestar-dw.datamart.total_orders` o
JOIN `makestar-dw.datamart.events_` e ON o.event_id = e.event_id
JOIN round_seq rs ON rs.album_name = e.album_name
WHERE o.market_type IN ('B2C', 'B2B')
  AND e.artist_id = target_artist_id
GROUP BY 1, 2, 3, 4, 5
ORDER BY rs.round_num, e.event_order
```

---

## 이벤트 성과

### 지난주 종료 이벤트 (리워드매출 · 판매량)

```sql
SELECT
  e.event_id                                                     AS `이벤트ID`,
  e.event_name                                                   AS `이벤트명`,
  DATE(e.sales_start_at, 'Asia/Seoul')                           AS `오픈일`,
  DATE(e.sales_end_at, 'Asia/Seoul')                             AS `종료일`,
  COALESCE(SUM(o.product_revenue), 0)                           AS `리워드매출`,
  COALESCE(SUM(o.order_album_qty), 0)                           AS `판매량`
FROM `makestar-dw.datamart.events_` e
LEFT JOIN `makestar-dw.datamart.total_orders` o ON o.event_id = e.event_id
WHERE DATE(e.sales_end_at, 'Asia/Seoul') BETWEEN
        DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -1 WEEK)
    AND DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -1 DAY)
  AND e.event_name NOT LIKE '%(삭제 필요)%'
GROUP BY 1, 2, 3, 4
ORDER BY 5 DESC
```

---

## ⚠️ Pending

| KPI | 이유 |
|---|---|
| 공헌이익 (GMV - 앨범원가) | 앨범원가 데이터 미확보 |
| 세그먼트 믹스 | 별도 레포에서 작업 중 |
