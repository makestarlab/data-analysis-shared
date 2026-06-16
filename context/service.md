# Makestar 서비스 도메인 지식

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
| NRU | 신규 가입자. `tb_auth_log WHERE log_type = 0` |
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
- **B2B**: 기업/도매 구매
- **market_type** 기준으로 GMV 분리. 앨범버디/기타는 별도 집계

## 이벤트 구조

- 하나의 아티스트(`artist_id`)가 여러 이벤트(`event_id`)를 가짐
- `event_type`: 앨범 유형 구분 (정규, 미니, 싱글 등)
- `event_order`: 아티스트 기준 n번째 이벤트
- `sales_start_at`: 오픈일 (이탈 원인 분석 시 후속 이벤트 유무 체크 기준)

## 이탈 원인 분류

1. **이벤트 공급 부재**: 이탈 후 동일 아티스트 후속 이벤트 없음
2. **플랫폼 리마케팅 실패**: 후속 이벤트 있음에도 미복귀
