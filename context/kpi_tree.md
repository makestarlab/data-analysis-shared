# Makestar KPI Tree

## Main KPI

| KPI | 정의 | 상태 |
|---|---|---|
| GMV | `SUM(total_revenue)` WHERE `market_type IN ('B2C','B2B')` | ✅ 운영 중 |
| 공헌이익 | GMV - 앨범원가 | ⚠️ Pending (앨범원가 데이터 미확보) |

---

## Supporting Metrics

### 매출 분해

```
GMV = PU × ARPPU
       │        └── 주문당 평균 금액 × 구매 빈도
       └── MAU × PUR (구매전환율)
```

| 지표 | 정의 | 데이터 소스 | 상태 |
|---|---|---|---|
| PU | `COUNT(DISTINCT user_id)` | `datamart.total_orders` | ✅ |
| ARPPU | GMV / PU | `datamart.total_orders` | ✅ |
| PUR | PU / MAU | `total_orders` + `customer_analysis_visit` | ✅ |
| 세그먼트 믹스 | Light / Middle / Whale 비중 변화 | `datamart.total_orders` | ✅ |

**세그먼트 기준 (LTV 누적)**

| 세그먼트 | 기준 |
|---|---|
| Light | LTV < 200,000원 |
| Middle | 200,000원 ≤ LTV < 1,000,000원 |
| Whale | LTV ≥ 1,000,000원 |

---

### Growth (신규 유입)

| 지표 | 정의 | 데이터 소스 | 상태 |
|---|---|---|---|
| NRU | 주간 신규 인증 가입자 (`is_certified = true`) | `pg_mystarroom_public.tb_auth_user` | ✅ |
| ↳ MAKESTAR | NRU 중 MAKESTAR 가입 | `tb_auth_log.service_name` | ✅ |
| ↳ POCAALBUM | NRU 중 POCAALBUM 가입 | `tb_auth_log.service_name` | ✅ |
| ↳ New Biz | NRU 중 STREAMWITH / POCADB / FANS / KPOPMATE / CALENDOL / JOGIYO | `tb_auth_log.service_name` | ✅ |
| 첫구매 전환율 | NRU → 첫 결제 비율 | `tb_auth_user` + `total_orders` | 🔲 미집계 |

---

### Engagement (활성도)

| 지표 | 정의 | 데이터 소스 | 상태 |
|---|---|---|---|
| DAU | 일간 활성 유저 | `datamart.dau` | ✅ |
| WAU | 주간 활성 유저 | `datamart.wau` | ✅ |
| MAU | 월간 활성 유저 (`COUNT(DISTINCT user_pseudo_id)`) | `datamart.customer_analysis_visit` | ✅ |
| Stickiness | DAU / MAU | `datamart.dau` + `customer_analysis_visit` | 🔲 미집계 |
| PDP 방문 Top 5 | 상품 상세 페이지 주간 방문자 상위 5개 상품 | `datamart.vw_commerce_events_visitor_segment` | ✅ |

---

### Retention (유지)

Makestar는 아티스트 이벤트 주기 기반이므로 **단순 미구매 기간이 아닌 이벤트 기준**으로 이탈 판단.

> 이탈 정의: 마지막 구매 아티스트의 후속 이벤트가 오픈된 이후에도 미구매

| 지표 | 정의 | 데이터 소스 | 상태 |
|---|---|---|---|
| 라운드 참여율 | 동일 아티스트 재구매 비율 (album_name 기준) | `total_orders` + `events_` | 🔲 미집계 |
| 이탈율 | 후속 이벤트 오픈 후 미구매 유저 비율 | `total_orders` + `events_` | 🔲 미집계 |
| 복귀율 | 이탈 후 재구매 비율 (과거 시점 기준 측정) | `total_orders` + `events_` | 🔲 미집계 |

**세그먼트별 Retention 추적**

| 세그먼트 | 우선순위 | 이유 |
|---|---|---|
| Whale | 높음 | 이탈 1명 = 매출 충격 큼 |
| Middle | 중간 | Whale 전환 가능 풀 |
| Light | 낮음 | 이벤트 부재 이탈이 대부분 |

---

### 공헌이익 분해 ⚠️ Pending

앨범원가 데이터 확보 후 구성 예정.

```
공헌이익 = GMV - 앨범원가
공헌이익률 = 공헌이익 / GMV
```

---

## 전체 구조 요약

```
GMV (Main)
├── PU × ARPPU
│     ├── PU = MAU × PUR
│     └── ARPPU = 주문당금액 × 빈도 × 세그먼트믹스
│
├── Growth
│     ├── NRU (MAKESTAR / POCAALBUM / New Biz)
│     └── 첫구매 전환율 🔲
│
├── Engagement
│     ├── DAU
│     ├── WAU
│     ├── MAU
│     ├── Stickiness (DAU/MAU) 🔲
│     └── PDP 방문 Top 5
│
└── Retention
      ├── 라운드 참여율 🔲
      ├── 이탈율 🔲
      └── 복귀율 🔲

공헌이익 (Main) ⚠️ Pending
└── GMV - 앨범원가
```

✅ = 집계 중  🔲 = 미집계  ⚠️ = 데이터 미확보
