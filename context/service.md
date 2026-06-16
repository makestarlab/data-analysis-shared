# Makestar 서비스 도메인 지식

## BQ 데이터 업데이트 주기

| 테이블 종류 | 주기 | 비고 |
|---|---|---|
| `pg_mystarroom_public.*`, `pg_oms_public.*`, `pg_pocadb_public.*` 등 원본 CDC 테이블 | **10분** | Datastream CDC |
| `datamart.*` | 미확정 | 별도 배치 |
| `pocaalbum_production` | 수동 | Google Sheets 연동 |

---

## 서비스 개요

Makestar는 K-POP 아티스트 기반 크라우드펀딩·커머스 플랫폼.

| 서비스 | 설명 |
|---|---|
| 메이크스타 커머스 | 아티스트 공식 굿즈/앨범 판매 (B2C/B2B) |
| SPM (크라우드펀딩) | 아티스트 프로젝트 펀딩 |
| AlbumBuddy | 앨범 공동구매 플랫폼 |
| PocaDB | 포토카드 데이터베이스 |

---

## 핵심 KPI

| KPI | 정의 |
|---|---|
| GMV | 총결제액. `SUM(total_revenue)` WHERE `market_type IN ('B2C','B2B')` |
| PU | 결제 유저 수. `COUNT(DISTINCT user_id)` |
| ARPPU | GMV / PU |
| MAU | 월간 활성 유저. `COUNT(DISTINCT user_pseudo_id)` from `customer_analysis_visit` |
| PUR | 구매전환율. PU / MAU |
| DAU/WAU | `datamart.dau`, `datamart.wau` |
| NRU | 신규 가입자. `tb_auth_user WHERE is_certified = true` 기준 |
| Stickiness | DAU / MAU |
| Churn | 미구매 기간 기준 (기준값 미확정) |

---

## 유저 ID 연결 구조

시스템마다 유저를 식별하는 ID가 다르다. 분석 목적에 따라 아래를 참조.

### 핵심 ID 대응표

| ID | 타입 | 위치 | 설명 |
|---|---|---|---|
| `tb_auth_user.id` | INTEGER | pg_mystarroom_public | **메이크스타 커머스 유저 PK** |
| `total_orders.user_id` | STRING | datamart | = `CAST(tb_auth_user.id AS STRING)` |
| `tb_commerce_order.user_id` | INTEGER | pg_mystarroom_public | = `tb_auth_user.id` |
| `customer_analysis_visit.user_id` | STRING | datamart | = `CAST(tb_auth_user.id AS STRING)` (로그인 세션만 존재) |
| `customer_analysis_visit.user_pseudo_id` | STRING | datamart | GA 익명 ID. 비로그인 포함. MAU 집계 기준 |
| `customer_analysis_visit.paying_user_id` | STRING | datamart | 해당 세션에서 결제한 경우만 값 존재 |
| `tb_auth_user.user_idx` | INTEGER | pg_mystarroom_public | = `production.user.idx` (SPM 레거시 ID) |
| `production.user.idx` | INTEGER | production | SPM 크라우드펀딩 유저 PK |

### 시스템 간 조인 방법

```sql
-- 커머스 주문 ↔ 유저 정보
total_orders.user_id = CAST(tb_auth_user.id AS STRING)

-- 커머스 ↔ SPM 크라우드펀딩
tb_auth_user.user_idx = production.user.idx
-- 또는 이메일 기준: tb_auth_user.email = production.user.email

-- GA 세션 ↔ 결제 유저
customer_analysis_visit.user_id = total_orders.user_id  -- 로그인 세션만 가능
```

### 주의사항

- `customer_analysis_visit`에서 `user_id`는 로그인 세션의 ~47%만 존재. 비로그인 포함 전체 트래픽은 `user_pseudo_id` 사용
- `paying_user_id`는 해당 세션에 결제가 있을 때만 존재 (~12%)
- `tb_auth_user.id`와 `tb_auth_user.user_idx`는 **다른 값**. 혼용 주의
- `production.user.idx`는 SPM 전용. 커머스 전용 유저는 `user_idx`가 NULL

---

## 판매 채널 구조

- **B2C**: 일반 소비자 직접 구매
- **B2B**: 기업/도매 구매 (`user_order_number` 'B' 접두사)
- **market_type** 기준으로 GMV 분리. 앨범버디/기타는 별도 집계

---

## 이벤트 생명주기

메이크스타 매출의 대부분은 **이벤트 단위**로 발생. 이벤트 오픈 시 매출이 단기 집중되는 패턴.

```
오픈(sales_start_at) → 판매(sales_end_at) → 발매(album_release_date) → 배송(issue_date + 10h)
```

| 단계 | 컬럼 | 비고 |
|---|---|---|
| 오픈 | `events_.sales_start_at` | 판매 시작. 매출 집중 시점 |
| 판매 종료 | `events_.sales_end_at` | |
| 앨범 발매 | `events_.album_release_date` | 써클차트 집계 기준 |
| 출고 기준 | `mst_sku.issue_date + 10h` | lead_time `발매일시` 계산 기준 |

- 하나의 아티스트(`artist_id`)가 여러 이벤트(`event_id`)를 가짐
- `event_order`: **같은 앨범 내 판매 차수** (아티스트 전체 순번 아님). 동일 앨범을 여러 차수로 재판매 시 1→N 증가. NULL = 구 이벤트
- `event_type`: 이벤트 유형 (MEET&CALL, VIDEOCALL, PHOTOCARD 등 — 코드값 참조)
- 데이터 품질: `event_name`에 "(삭제 필요)" 등 관리용 문자열 포함된 이벤트 존재 → 집계 시 주의

---

## POB (Purchase with Benefit) — 특전 구조

일정 금액 이상 구매 시 이벤트(팬미팅·영상통화 등) **응모권**을 부여하는 구조.

- `total_orders.event_id IS NOT NULL` = POB 포함 주문
- 쇼핑 주문에 POB가 묶여 판매됨 → `lead_time.주문유형`에서 "특전&일반" / "특전" / "일반" 구분이 나오는 이유
- `vw_commerce_order_items.product_event_type = '이벤트'` = POB 라인아이템
- 응모 수를 늘리려는 팬덤 특성상 **동일 유저의 다수 옵션 구매**가 일반적

---

## 앨범 판매량(초동) vs GMV

| 지표 | 컬럼 | 설명 |
|---|---|---|
| GMV | `total_revenue` | 결제액 (KRW) |
| 앨범 판매량 | `order_album_qty` | 실제 앨범 수량. 써클차트 집계 기준 |
| 초동 | — | 발매 첫 주(`first_week_closing_date`) 누적 판매량 |

- `order_album_qty` = `order_qty` × `vw_product_option_info.sales_qty` (`content_sales_base = 'true'`)
- GMV와 앨범 판매량은 별개 지표. 고가 옵션 1개 구매 vs 저가 옵션 다수 구매의 차이

---

## 취소/환불과 GMV 계산

- `total_orders`에 포함되는 결제 상태: `CONFIRMED`, `PARTIAL_CANCELED`
- `PARTIAL_CANCELED` = 일부 취소 후 **잔여 금액만** 집계됨
- `total_orders_waiting` = 결제 진행 중 대기 주문 (GMV 미포함)
- 취소 완료(`CANCELED`) 주문은 `total_orders`에서 제외

```sql
-- 정확한 GMV: total_orders만 사용하면 됨 (이미 필터 적용됨)
SELECT SUM(total_revenue) FROM `makestar-dw.datamart.total_orders`
WHERE market_type IN ('B2C','B2B')

-- 대기 포함 예상 GMV
SELECT SUM(total_revenue) FROM `makestar-dw.datamart.total_orders_waiting`
WHERE market_type IN ('B2C','B2B')
```

---

## 통화/환율 처리

모든 매출은 **KRW 기준**으로 집계.

| 채널 | 원본 통화 | 환율 소스 |
|---|---|---|
| 메이크스타 커머스 | KRW / USD / 기타 | `vw_commerce_exchange_rate` |
| 웨이디엔 | CNY | `vw_commerce_exchange_rate` |
| 위챗 미니프로그램 | CNY | (내부 처리) |
| 대만 오프라인 | TWD | `external.country_exchange_rate_googlefinance` |
| 일본 오프라인 | JPY | `vw_commerce_exchange_rate` |

- `vw_commerce_orders.exchange_rate` = 주문 시점 환율
- 환율 기준일 = `DATE(pay_date, 'Asia/Seoul')`

---

## 아티스트 vs IP 개념

| 컬럼 | 위치 | 설명 |
|---|---|---|
| `ip_name` | `total_orders` | 아티스트명 **문자열** (비정형, 오타 가능) |
| `artist_id` | `events_`, `vw_commerce_items_v2` | 아티스트 **고유 ID** (조인 키로 사용) |
| `artist_name` | `vw_commerce_items_v2` | 정규화된 아티스트명 |

- `ip_name` 기준 집계는 오류 가능성 있음 → `artist_id` 기준 권장
- 그룹 아티스트와 멤버 솔로 이벤트가 혼재 → `artist_id` 레벨로 구분 필요

---

## 이탈 원인 분류

1. **이벤트 공급 부재**: 이탈 후 동일 아티스트 후속 이벤트 없음
2. **플랫폼 리마케팅 실패**: 후속 이벤트 있음에도 미복귀
