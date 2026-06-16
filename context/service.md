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

## 유저 행동 특성

### 일반 B2C 유저
- **한 유저 = 한 아티스트** 구매가 평균적인 패턴
- 특정 아티스트의 팬이 그 아티스트 이벤트만 반복 구매
- 아티스트 이벤트가 없으면 구매가 끊김 → 이탈 분석 시 핵심 변수

### 구매대행 유저

일반 팬 유저와 **완전히 다른 구매 패턴**. 분석 시 반드시 제외.

**식별 기준:**
- 여러 아티스트(IP) 구매
- 배송지가 물류센터 주소
- 대량 반복 구매

**현재 알려진 구매대행 user_id 목록:**
```
'1876860', '812307', '1736734', '621230', '1302313', '1902098', '859600', '969308',
'1027784', '1581799', '797962', '802866', '1492647', '781240', '885795', '1264675',
'1001311', '2116643', '1659287', '700815', '1540460', '1890901', '1511280', '1006060',
'1606082', '1552669', '1913216', '1138597', '1284854', '1504890', '12526', '944286',
'945344', '2046425', '1545878', '1600974', '886898', '1539934', '1533310', '911936',
'1069252', '971976', '1658602', '948579', '1071325', '1995221', '1933087', '636546',
'1509180', '1257147', '2032775', '1323619', '1958765', '864765', '1994769', '209076',
'1608153', '1312465', '1355103', '1248833', '1506290', '965150', '1011224', '1260938',
'625886', '939836', '1870283', '1347032', '1939835', '1973097', '2022335', '1335644',
'1975403', '646210', '1542033', '910047', '1995697', '882978', '1252380', '2159123',
'867147', '942107', '1329252', '71764', '1845002', '999056', '809695', '1604186',
'1506617', '1006091', '870982', '1895495', '1052115', '1313023', '1254035', '1063330',
'2050980', '1550897', '1660416', '1620875', '946338', '1482920', '1253405', '1502990',
'91909', '1738982', '2114301', '1005028', '1513305', '1874153', '1267050', '1354020',
'1062950', '905126', '1071819', '1935908', '1073305', '1247698', '898061', '943715',
'1673444', '1334025', '1982712', '1290379', '1503928', '1502504', '2159410'
```

**분석 시 제외 패턴:**
```sql
WHERE user_id NOT IN (
  '1876860', '812307', '1736734', '621230', '1302313', '1902098', '859600', '969308',
  '1027784', '1581799', '797962', '802866', '1492647', '781240', '885795', '1264675',
  '1001311', '2116643', '1659287', '700815', '1540460', '1890901', '1511280', '1006060',
  '1606082', '1552669', '1913216', '1138597', '1284854', '1504890', '12526', '944286',
  '945344', '2046425', '1545878', '1600974', '886898', '1539934', '1533310', '911936',
  '1069252', '971976', '1658602', '948579', '1071325', '1995221', '1933087', '636546',
  '1509180', '1257147', '2032775', '1323619', '1958765', '864765', '1994769', '209076',
  '1608153', '1312465', '1355103', '1248833', '1506290', '965150', '1011224', '1260938',
  '625886', '939836', '1870283', '1347032', '1939835', '1973097', '2022335', '1335644',
  '1975403', '646210', '1542033', '910047', '1995697', '882978', '1252380', '2159123',
  '867147', '942107', '1329252', '71764', '1845002', '999056', '809695', '1604186',
  '1506617', '1006091', '870982', '1895495', '1052115', '1313023', '1254035', '1063330',
  '2050980', '1550897', '1660416', '1620875', '946338', '1482920', '1253405', '1502990',
  '91909', '1738982', '2114301', '1005028', '1513305', '1874153', '1267050', '1354020',
  '1062950', '905126', '1071819', '1935908', '1073305', '1247698', '898061', '943715',
  '1673444', '1334025', '1982712', '1290379', '1503928', '1502504', '2159410'
)
```

> 이 목록은 수동 관리 중. 신규 구매대행 발견 시 추가 필요.

---

## 유저 생애주기

```
가입 → 첫구매 → 반복구매 → 이벤트 공백(휴식) → 이탈 → 복귀
```

### 단계별 정의

| 단계 | 정의 | 분석 기준 |
|---|---|---|
| **가입** | `tb_auth_user.is_certified = true` | `created_at` 기준 |
| **첫구매** | 해당 유저의 첫 번째 결제 완료 | `MIN(DATE(pay_date))` from `total_orders` |
| **반복구매** | 동일 아티스트 이벤트를 앨범 릴리즈 사이클에 맞춰 재구매 | 아티스트별 팬덤 단위 집계 |
| **이벤트 공백(휴식)** | 마지막 구매 아티스트의 후속 이벤트가 아직 열리지 않은 상태. **이탈 아님** | `events_.sales_start_at` 기준으로 후속 이벤트 유무 확인 |
| **이탈** | 후속 이벤트가 열렸음에도 구매하지 않음 | 이벤트 오픈 후 미구매 |
| **복귀** | 이탈 후 재구매. 드물게 다른 아티스트로 전환하는 경우도 있음 | 재구매 발생 시점 |

### 핵심 특수성 — 이탈 판단 기준

> **단순 미구매 기간(N일)으로 이탈을 정의할 수 없음**
>
> 아티스트 앨범 릴리즈 주기가 불규칙하므로, 이벤트 공백 중인 유저를 이탈로 분류하면 오탐.
> 반드시 **"후속 이벤트 오픈 이후에도 미구매"** 를 이탈 조건에 포함해야 함.

```sql
-- 이탈 판단 패턴 (이벤트 오픈 이후 미구매)
-- 1) 유저의 마지막 구매 이벤트 → 아티스트 확인
-- 2) 해당 아티스트의 후속 이벤트 오픈 여부 확인 (events_.sales_start_at)
-- 3) 후속 이벤트 오픈 후에도 구매 없으면 → 이탈

WITH last_purchase AS (
  SELECT user_id, last_event_id, last_pay_date,
    ARRAY_AGG(event_id IGNORE NULLS ORDER BY pay_date DESC LIMIT 1)[SAFE_OFFSET(0)] AS last_event_id
  FROM `makestar-dw.datamart.total_orders`
  WHERE market_type IN ('B2C','B2B')
  GROUP BY user_id, last_event_id, last_pay_date
),
next_event AS (
  SELECT lp.user_id, lp.last_pay_date,
    MIN(e2.sales_start_at) AS next_event_open_at
  FROM last_purchase lp
  JOIN `makestar-dw.datamart.events_` e1 ON lp.last_event_id = e1.event_id
  JOIN `makestar-dw.datamart.events_` e2
    ON e1.artist_id = e2.artist_id
    AND e2.sales_start_at > lp.last_pay_date
  GROUP BY lp.user_id, lp.last_pay_date
)
-- 후속 이벤트가 열렸고, 그 이후에도 구매 없으면 이탈
```

### 아티스트-팬덤 단위 집계

- 대부분의 유저 분석은 **아티스트별 팬덤 단위**로 의미가 있음
- 유저 × 아티스트 조합으로 집계 (전체 유저 단위 집계 시 왜곡 발생)
- `events_.artist_id` 기준으로 팬덤 구분

### 구매력에 따른 행동 차이

| 구매력 | 구매 이벤트 특성 |
|---|---|
| 높음 | 더 많은 판매 차수(`event_order`) 참여, 다양한 이벤트 유형, 더 많은 옵션 구매 (응모 수 극대화) |
| 낮음 | 주요 차수(1차)만 참여, 단일 옵션 구매 |

---

## 이탈 원인 분류

1. **이벤트 공급 부재**: 이탈 후 동일 아티스트 후속 이벤트 없음 → 플랫폼 책임 아님
2. **플랫폼 리마케팅 실패**: 후속 이벤트 열렸음에도 미복귀 → 플랫폼 개입 가능 영역
