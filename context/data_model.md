# Makestar 데이터 모델 — 엔티티 관계도

분석 중 자주 헷갈리는 ID 체계, 주문-이벤트-SKU 관계, 특전(POB) 구조 정리.

---

## 전체 관계도

```
┌─────────────────────────────────────────────────────────────────┐
│                         유저 (USER)                              │
│  tb_auth_user.id         INTEGER  ← 커머스 유저 PK              │
│  tb_auth_user.user_idx   INTEGER  ← SPM 레거시 ID (다른 값!)    │
│                                                                 │
│  total_orders.user_id    STRING   = CAST(tb_auth_user.id AS STRING)
│  customer_analysis_visit.user_id  = total_orders.user_id       │
│  customer_analysis_visit.user_pseudo_id  ← GA 익명ID (비로그인 포함)
└───────────────────┬─────────────────────────────────────────────┘
                    │ 1:N
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     주문 (ORDER)                                 │
│  total_orders / tb_commerce_order                               │
│                                                                 │
│  order_no     커머스 주문번호 (C25xxx...)                        │
│  user_id      유저                                              │
│  event_id ──────────────────────────────────────────────────┐  │
│  ip_name      비정형 아티스트명 (오타 있음, artist_id 권장)     │  │
│  product_code 상품코드                                         │  │
│  option_code  옵션코드                                         │  │
│  biz_type     이벤트 / 쇼핑 / B2B ...                          │  │
│  market_type  B2C / B2B                                        │  │
│                                                                 │  │
│  event_id IS NULL     → 순수 쇼핑 주문                          │  │
│  event_id IS NOT NULL → POB(특전) 포함 주문                     │  │
└──────────────┬──────────────────────────────────────────────────┘  │
               │ product_code + option_code                          │
               ▼                                                      │
┌──────────────────────────────┐                                      │
│  상품/옵션                    │           event_id                   │
│  vw_commerce_items_v2        │◄─────────────────────────────────────┘
│  ⚠️ Google Sheets 의존       │                    │
│     → 실행 시 권한 에러 발생  │                    ▼
│                              │   ┌──────────────────────────────┐
│  product_event_code          │   │  이벤트 (events_)            │
│    = total_orders.product_code   │  event_id                    │
│  product_option_id           │   │  artist_id ──────────────────┼──┐
│    = total_orders.option_code│   │  album_name                  │  │
│  event_id                    │   │  event_type (MEET&CALL 등)   │  │
│  artist_id                   │   │  event_order (이벤트 회차)   │  │
│  sku_code ──────────┐        │   │  sales_start_at              │  │
└─────────────────────┼────────┘   │  sales_end_at                │  │
                      │            └──────────────────────────────┘  │
                      ▼                                               │
┌─────────────────────────────────────────┐                          │
│  재고 단위 (mst_sku)                     │◄─────────────────────────┘
│                                         │
│  sku_code   예: SKU016001               │
│  sku_name   아티스트|상품코드|SKU설명    │
│  sku_type                               │
│    P = 부모 (랜덤포카 상위 단위)         │
│    C = 자식 (실제 개별 포카) ← 집계 제외 │
│    NULL = 일반 상품                     │
│  virtual_child_sku_count ← 포카 종류 수 │
└──────────────────┬──────────────────────┘
                   │ sku_code
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│              OMS 출고 (oms_order_line_item_sku)                  │
│                                                                 │
│  order_no     OMS 주문번호 (E-xxx, B-xxx, C-xxx)                │
│               ⚠️ 커머스 order_no (C25xxx)와 별개 체계           │
│               직접 JOIN 불가 — sku_code가 유일한 공통 키         │
│  sku_code                                                       │
│  quantity                                                       │
│  product_type NCM_EVENT / NCM_SHOPPING / SHOPPING               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 주문번호 접두사 체계

### 커머스 주문번호 (`total_orders.order_no`)

| 접두사 | market_type | biz_type | 설명 |
|---|---|---|---|
| `C` | B2C | 이벤트/쇼핑/해외 | B2C 커머스 주문 (주력) |
| `P` | B2C | 이벤트/중국/해외 | B2C 구형 또는 특정 채널 |
| `B` | B2B + B2C 혼재 | B2B/이벤트/기타 | B2B 주력, B2C 소수 혼재 |
| `S` | B2C | 쇼핑/일본 | B2C 쇼핑 구형 |
| `M` | B2C | 중국/쇼핑 | 위챗 계열 |
| `E` | B2B | B2B | B2B 이벤트 |
| `8`, `9`, `1` | B2C | 중국/일본 | 오프라인/외부 채널 |

```sql
-- B2C 쇼핑만 필터
WHERE order_no LIKE 'C%' OR order_no LIKE 'S%'

-- B는 B2B 주력이지만 B2C 소수 혼재 → market_type으로 이중 확인 권장
WHERE order_no LIKE 'B%' AND market_type = 'B2B'
```

### OMS 주문번호 (`oms_order_line_item_sku.order_no`)

| 접두사 | 채널 |
|---|---|
| `E-` | 이벤트 주문 |
| `B-` | B2B 도매 주문 (NCM_SHOPPING에 혼재) |
| `C-` | 쇼핑 B2C 주문 (추정) |
| `S` | 쇼핑 구형 |

> `NCM_SHOPPING` product_type에는 B2B(B- 접두사)와 B2C(C- 접두사)가 혼재.
> 채널 구분 시 반드시 order_no 접두사로 재필터 필요.

---

## 특전(POB) 구조 — 분석 시 반드시 주의

```
팬이 이벤트 상품 구매
  ├── [일반 구성] 앨범 + 랜덤포카
  │     → SKU로 OMS 출고 가능 ✅
  │
  └── [특전 POB] 팬미팅/영상통화 응모권
        → total_orders.event_id IS NOT NULL 로 식별
        → 실물 없음, OMS 출고 대상 아님
        → ⚠️ 단독 판매/배송 불가 (항상 일반 상품에 번들)
```

**분석 영향:**
- 쇼핑 주문 중 `event_id IS NOT NULL` (약 5%) = 특전 응모 목적으로 쇼핑 상품을 산 것
- 순수 쇼핑 수요 측정 시 → `event_id IS NULL` 조건 추가 권장
- POB 포함 쇼핑 주문은 재구매율/LTV 성격이 일반 쇼핑과 다를 수 있음

---

## 핵심 조인 패턴

```sql
-- 1. 커머스 유저 ID 통일
total_orders.user_id = CAST(tb_auth_user.id AS STRING)

-- 2. 이벤트 메타 보강 (룩업)
FROM total_orders t
LEFT JOIN events_ e ON t.event_id = e.event_id
-- → artist_id, event_type, sales_start_at, sales_end_at 획득

-- 3. ip_name 대신 artist_id 기준 권장
-- ip_name은 오타/표기 차이 있음
-- events_ 경유해서 artist_id 사용

-- 4. 쇼핑 상품 SKU 조인 (new_commerce_db 주문만 유효)
FROM total_orders o
LEFT JOIN vw_commerce_items_v2 i
       ON o.event_id    = i.event_id
      AND o.option_code = i.product_option_id
-- ⚠️ vw_commerce_items_v2: Google Sheets 의존 → 권한 에러 발생 가능
```

---

## 분석별 주의사항

| 분석 목적 | 주의사항 |
|---|---|
| 팬덤/유저 행동 | 구매대행(~356명), 배송대행(~14,000명) 반드시 제외 |
| GMV 집계 | 구매대행·배송대행 포함 (실제 매출) |
| 이탈 분석 | 단순 미구매 기간이 아닌 "후속 이벤트 오픈 후 미구매"로 정의 |
| 쇼핑 수요 분석 | `event_id IS NULL` 로 순수 쇼핑만 필터 권장 |
| SKU 분석 | `sku_type = 'C'` (자식 포카) 제외, `virtual_child_sku_count` 사용 |
| B2C/B2B 구분 | `market_type` 컬럼 또는 `order_no` 접두사 사용 |
| OMS ↔ 커머스 연결 | 직접 JOIN 불가 — `sku_code`가 유일한 공통 키 |
