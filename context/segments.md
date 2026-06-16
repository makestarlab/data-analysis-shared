# 유저 세그먼트 & 이탈 기준

## 유저 세그먼트 (B2C 누적 결제금액 기준)

| 그룹 | 범위 | Tier |
|---|---|---|
| Light | 0 ~ 20만원 미만 | Tier 1–2 |
| Middle | 20만원 ~ 100만원 미만 | Tier 3–4 |
| Whale | 100만원 이상 | Tier 5–7 |

### Tier 상세

| Tier | 범위 |
|---|---|
| Tier 1 | 0 ~ 5만원 미만 |
| Tier 2 | 5만원 ~ 20만원 미만 |
| Tier 3 | 20만원 ~ 50만원 미만 |
| Tier 4 | 50만원 ~ 100만원 미만 |
| Tier 5 | 100만원 ~ 300만원 미만 |
| Tier 6 | 300만원 ~ 1000만원 미만 |
| Tier 7 | 1000만원 이상 |

### 세그먼트 분류 SQL CTE

```sql
WITH user_segment AS (
  SELECT
    user_id,
    SUM(total_revenue)                                                    AS ltv,
    MAX(DATE(pay_date, 'Asia/Seoul'))                                     AS last_pay_date,
    ARRAY_AGG(event_id IGNORE NULLS ORDER BY pay_date DESC LIMIT 1)[SAFE_OFFSET(0)] AS last_event_id,
    CASE
      WHEN SUM(total_revenue) < 200000   THEN 'Light'
      WHEN SUM(total_revenue) < 1000000  THEN 'Middle'
      ELSE 'Whale'
    END AS segment
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C','B2B')
  GROUP BY user_id
)
```

---

## 이탈 기준

- **CHURN_DAYS = 90**: 마지막 구매 후 90일 이상 미구매 = 이탈
- 이탈 여부: `DATE_DIFF(CURRENT_DATE(), last_pay_date, DAY) >= 90`

### 복귀율 측정 주의사항

현재 이탈 중인 유저 풀로 복귀율 계산 시 **항상 0%** 가 나옴.
복귀한 유저는 이탈 풀에서 이미 제외되기 때문.

**올바른 방법**: 과거 시점 기준으로 이탈자 정의
```sql
-- 1년 전 기준 이탈자 중 이후 복귀한 비율
WHERE last_pay_date < DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
  AND DATE_DIFF(DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY), last_pay_date, DAY) >= 90
```

---

## 분석 기준일

- `ANALYSIS_START = '2025-01-01'`
- 타임존: 모든 날짜 연산에 `'Asia/Seoul'` 적용
