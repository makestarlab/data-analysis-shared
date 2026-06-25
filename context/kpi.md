# Makestar KPI 현황

Weekly Review 대시보드(Redash #58) 기준 현행 KPI 정의.

---

## 매출 (GMV)

### 대분류별 매출 (`market_type`)

| market_type | 설명 |
|---|---|
| B2C | 일반 소비자 직접 구매 |
| B2B | 기업/도매 구매 |
| 포카앨범제작 | 포카앨범 제작 매출 |
| 앨범버디 | AlbumBuddy 플랫폼 |

```sql
-- 주별 대분류별 매출 (Redash #970)
SELECT
    DATE_TRUNC(pay_date, WEEK(MONDAY)) AS pay_week,
    market_type,
    SUM(total_revenue) AS total_revenue
FROM datamart.total_orders
WHERE DATE(pay_date) >= DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -20 WEEK)
  AND DATE(pay_date) < DATE(CURRENT_DATE('Asia/Seoul'))
GROUP BY ALL
ORDER BY pay_week
```

### B2C 사업별 매출 (`biz_type`)

| biz_type | 채널 |
|---|---|
| 한국(이벤트) | 국내 이벤트 리워드 |
| 한국(매장) | 오프라인 메이크스타샵 |
| 중국 | 위챗미니프로그램 + 웨이디엔 + 오프라인 |
| APAC | 아시아태평양 |
| 일본 | 일본 온/오프라인 |
| 미주유럽 | 미주·유럽 |
| 쇼핑 | 국내 쇼핑 B2C |

```sql
-- 주별 B2C 사업별 매출 (Redash #985)
SELECT
    DATE_TRUNC(pay_date, WEEK(MONDAY)) AS pay_week,
    biz_type,
    SUM(total_revenue) AS total_revenue
FROM datamart.total_orders
WHERE DATE(pay_date) >= DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -20 WEEK)
  AND DATE(pay_date) < DATE(CURRENT_DATE('Asia/Seoul'))
  AND market_type = 'B2C'
GROUP BY ALL
ORDER BY pay_week
```

### 주간 매출 증감 요약 테이블

지난주 / 그 전주 / 52주 평균을 나란히 비교.

```sql
-- 대분류별 증감 (Redash #1492)
-- B2C 사업별 증감 (Redash #1493)
-- 공통 구조:
SELECT
    대분류,
    지난주_매출,
    그전주_매출,
    전주_대비_증가율,   -- SAFE_DIVIDE 기반
    주평균_매출_최근1년  -- SUM / 52
```

---

## 유저 활동

### WAU (주간 활성 유저)

```sql
-- Redash #114
SELECT date, SUM(wau) AS wau
FROM datamart.wau
WHERE date >= DATE_ADD(DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY)), INTERVAL -53 WEEK)
  AND date < DATE_TRUNC(CURRENT_DATE('Asia/Seoul'), WEEK(MONDAY))
GROUP BY date
ORDER BY date
```

### NRU (신규 가입자, 서비스별)

`tb_auth_log.log_type = 0` 기준. 서비스별 분류:

| 가입서비스 | 설명 |
|---|---|
| MAKESTAR | 메이크스타 커머스 |
| POCAALBUM | 포카앨범 |
| New Biz | STREAMWITH / POCADB / FANS / KPOPMATE / CALENDOL / JOGIYO 통합 |

> 집계 제외: UNKNOWN, MA, VOTE, ADMIN

```sql
-- Redash #569 (PostgreSQL — pg_mystarroom 데이터소스)
SELECT
    DATE_TRUNC('week', created_at AT TIME ZONE 'Asia/Seoul') AS 가입일,
    CASE WHEN service_name IN ('STREAMWITH','POCADB','FANS','KPOPMATE','CALENDOL','JOGIYO')
         THEN 'New Biz' ELSE service_name END AS 가입서비스,
    COUNT(id) AS 가입자수
FROM tb_auth_log
WHERE log_type = 0
  AND service_name NOT IN ('UNKNOWN','MA','VOTE','ADMIN')
GROUP BY 1, 2
```

---

## 상품/이벤트 성과

### PDP 방문 Top 5

상품 상세 페이지(PDP) 주간 방문자 기준 상위 5개 상품.

- 소스: `datamart.vw_commerce_events_visitor_segment`
- 기준: `event_name = 'session_start'`, `user_pseudo_id` 기준 유니크
- 파라미터: 기간(start/end), 단위(일별/주별/월별)

```sql
-- Redash #921 (핵심 구조)
SELECT time_interval, product_event_name, COUNT(DISTINCT user_pseudo_id) AS visitors
FROM datamart.vw_commerce_events_visitor_segment v
JOIN datamart.vw_commerce_items i
  ON REGEXP_EXTRACT(v.page_path, r'/product/(\d+)') = i.product_event_id
WHERE event_name = 'session_start'
GROUP BY ALL
QUALIFY ROW_NUMBER() OVER(PARTITION BY time_interval ORDER BY visitors DESC) <= 5
```

### 지난주 종료 이벤트

```sql
-- Redash #121
SELECT event_name, 오픈일, 종료일, 리워드매출, 판매량(order_album_qty)
FROM datamart.total_orders JOIN datamart.events_
WHERE biz_type IN ('한국(이벤트)', '한국(매장)')
  AND sales_end_at BETWEEN 지난주월요일 AND 지난주일요일
ORDER BY 리워드매출 DESC
```

---

## 해외 커머스

### 지역별 매출 추이

집계 기준: 주별/월별/분기별/반기별 선택 가능.

| 지역 | biz_type |
|---|---|
| 중국 | 중국 |
| APAC | APAC |
| 일본 | 일본 |
| 미주·유럽 | 미주유럽 |

```sql
-- Redash #1491
-- 집계기준(주별/월별/분기별/반기별) 파라미터, 기간필터 파라미터
SELECT biz_type, params_period, revenue,
    SAFE_DIVIDE(revenue, SUM(revenue) OVER(PARTITION BY params_period)) AS 매출비중
FROM datamart.total_orders
WHERE biz_type IN ('중국','APAC','일본','미주유럽')
```

---

## Redash 쿼리 인덱스

| 쿼리ID | 쿼리명 | 데이터소스 |
|---|---|---|
| #114 | Weekly Active Users (WAU) | BigQuery |
| #121 | 지난주 종료 이벤트 | BigQuery |
| #569 | Weekly 통합회원 가입서비스별 가입자 수 | PostgreSQL |
| #921 | PDP 방문 Top 5 | BigQuery |
| #970 | Weekly 대분류별 매출액 | BigQuery |
| #985 | Weekly B2C 사업별 매출액 | BigQuery |
| #1491 | [해외커머스유닛] 주별 지역별 매출 추이 | BigQuery |
| #1492 | 주별 대분류별 매출액 증감 | BigQuery |
| #1493 | 주별 B2C 사업별 매출액 증감 | BigQuery |
