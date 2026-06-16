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
