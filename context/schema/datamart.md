# datamart 스키마

_자동 생성 — `scripts/refresh_schema.py` 실행으로 갱신_


## total_orders — GMV/결제 집계 기준

| 컬럼 | 타입 | 설명 |
|---|---|---|
| market_type | STRING | 매출 대분류(B2C, B2B, 앨범버디, 기타) |
| biz_type | STRING | 매출 분류 |
| channel_type | STRING | 판매채널 |
| data_source | STRING | 데이터 출처 |
| order_no | STRING | 주문번호 |
| order_date | DATETIME | 주문일시 |
| pay_date | DATETIME | 결제일시 |
| product_type | STRING | 상품유형 |
| product_category | STRING | 상품카테고리 |
| parent_product_name | STRING | 대분류명 |
| ms_product_code | STRING | 메이크스타 어드민 상품코드 |
| ms_product_name | STRING | 메이크스타 어드민 상품명 |
| ms_option_code | STRING | 메이크스타 어드민 옵션코드 |
| ms_option_name | STRING | 메이크스타 어드민 옵션명 |
| product_code | STRING | 상품코드 |
| product_name | STRING | 상품명 |
| option_code | STRING | 옵션코드 |
| option_name | STRING | 옵션명 |
| ip_name | STRING | 아티스트명 |
| event_id | STRING | 이벤트 ID |
| product_revenue | FLOAT | 상품결제액 |
| shipping_revenue | FLOAT | 배송비결제액 |
| total_revenue | FLOAT | 총결제액 |
| order_qty | FLOAT | 주문수량 |
| order_album_qty | FLOAT | 주문앨범수량 |
| logis_cd | STRING | 배송사코드 |
| order_country_code | STRING | 주문국가코드 |
| shipping_country_code | STRING | 배송국가코드 |
| user_id | STRING | 유저 ID |

## events_ — 이벤트 메타 (권장)

이벤트 목록입니다. 이벤트의 정보가 필요한 대부분의 경우에 사용됩니다.


| 컬럼 | 타입 | 설명 |
|---|---|---|
| event_idx | INTEGER | 이벤트 IDX |
| event_id | STRING | 이벤트 ID |
| event_name | STRING | 이벤트명 |
| album_name | STRING | 앨범명 |
| album_price | INTEGER | 앨범가 |
| album_release_date | DATE | 발매일 |
| event_order | INTEGER | 이벤트 회차 |
| event_type | STRING | 이벤트 유형 |
| artist_id | STRING | 아티스트 ID |
| sales_start_at | DATETIME | 오픈일 |
| sales_end_at | DATETIME | 종료일 |

## events — 이벤트 메타 (구버전, artist_id=INTEGER)

이벤트 목록입니다.


| 컬럼 | 타입 | 설명 |
|---|---|---|
| event_idx | INTEGER | 이벤트 IDX |
| event_id | STRING | 이벤트 ID |
| event_name | STRING | 이벤트명 |
| album_name | STRING | 앨범명 |
| album_price | INTEGER | 앨범가 |
| album_release_date | DATE | 발매일 |
| event_order | INTEGER | 이벤트 회차 |
| event_type | STRING | 이벤트 유형 |
| artist_id | INTEGER | 아티스트 ID |

## customer_analysis_visit — GA 기반 방문자 (MAU)

| 컬럼 | 타입 | 설명 |
|---|---|---|
| report_date | DATE |  |
| user_pseudo_id | STRING |  |
| user_id | STRING |  |
| device_os | STRING |  |
| device_category | STRING |  |
| device_group | STRING |  |
| continent | STRING |  |
| country | STRING |  |
| language_setting | STRING |  |
| is_new | STRING |  |
| source | STRING |  |
| medium | STRING |  |
| campaign | STRING |  |
| ga_session_number | INTEGER |  |
| paying_user_id | STRING |  |
| engagement_minutes | INTEGER |  |
| product_event_code | STRING |  |
| product_event_name | STRING |  |

## dau — 일별 DAU

커머스 일별 DAU 입니다.


| 컬럼 | 타입 | 설명 |
|---|---|---|
| date | DATE [REQUIRED] | 일자 |
| platform | STRING | 플랫폼(WEB, ANDROID, IOS) |
| dau | INTEGER | DAU(일간 방문자) |

## wau — 주별 WAU

| 컬럼 | 타입 | 설명 |
|---|---|---|
| date | DATE [REQUIRED] | 일자(주의 시작 월요일) |
| platform | STRING | 플랫폼(WEB, ANDROID, IOS) |
| wau | INTEGER | WAU(주간 방문자) |

## vw_master_order — 주문 마스터 뷰

| 컬럼 | 타입 | 설명 |
|---|---|---|
| 식별번호 | STRING |  |
| 주문번호 | STRING |  |
| 결제번호 | STRING |  |
| 주문고객명 | STRING |  |
| 이메일주소 | STRING |  |
| 주문일시 | TIMESTAMP |  |
| 휴대폰번호 | STRING |  |
| 주문상태 | STRING |  |
| 상품명 | STRING |  |
| 이벤트 구분 | STRING |  |
| 응모여부 | STRING |  |
| 당첨여부 | STRING |  |
| 당첨일자 | INTEGER |  |
| 통화기준 | STRING |  |
| 결제일시 | TIMESTAMP |  |
| 결제상태 | STRING |  |
| 상품금액 | FLOAT |  |
| 배송비 | FLOAT |  |
| 관부가세 | FLOAT |  |
| 대납수수료 | FLOAT |  |
| 결제수단 | STRING |  |
| 결제수단정보 | STRING |  |
| 수취인명 | STRING |  |
| 배송대상 | STRING |  |
| 배송국가지역 | STRING |  |
| 배송국가코드 | STRING |  |
| 주도 | STRING |  |
| 도시 | STRING |  |
| 주소 | STRING |  |
| 상세주소 | STRING |  |
| 우편번호 | STRING |  |
| 배송사 | STRING |  |
| 응모자성 | STRING |  |
| 응모자이름 | STRING |  |
| 응모자생년월일 | STRING |  |
| 응모메신저 | STRING |  |
| 응모메신저ID | STRING |  |
| 신분증통관번호 | STRING |  |

## vw_master_user — 유저 마스터 뷰

| 컬럼 | 타입 | 설명 |
|---|---|---|
| 유저ID | INTEGER |  |
| 가입계정 | STRING |  |
| 이름 | STRING |  |
| 생년월일 | DATE |  |
| 거주국가 | STRING |  |
| 전화번호 | STRING |  |
| 성별 | STRING |  |
| 회원상태 | STRING |  |
| 활동상태 | STRING |  |
| 가입일 | TIMESTAMP |  |
| 탈퇴여부 | BOOLEAN |  |
| 가입서비스 | STRING |  |
| 배송정보 수신 | STRING |  |
| 마케팅 제공동의 | BOOLEAN |  |

---

## lead_time — 쇼핑/B2B 주문 배송 리드타임

B2B(`user_order_number` 'B' 접두사)·쇼핑('C' 접두사) 주문만 포함.
코드값·기준일시 계산 규칙은 `context/code_values.md` 참조.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| 주문번호 | STRING | tb_commerce_order.user_order_number |
| 주문유형 | STRING | B2B/쇼핑 × 특전(POB) 여부 조합 |
| 결제일시 | DATETIME | |
| 발매일시 | DATETIME | mst_sku.issue_date + 10시간 |
| 기준일시 | DATETIME | greatest(결제일시, 발매일시) + 영업시간 보정 |
| 배송준비일시 | DATETIME | |
| 배송준비 소요일 | FLOAT | 기준일시 → 배송준비일시 |
| 재고할당일시 | DATETIME | |
| 재고할당 소요일 | FLOAT | 배송준비(또는 홀딩 해제) → 재고할당 |
| 배송요청일시 | DATETIME | |
| 배송요청 소요일 | FLOAT | 재고할당 → 배송요청 |
| 총 소요일 | FLOAT | 위 3단계 합계 |
| 비고 | STRING | NULL=정상 / '재고할당 실패로 홀딩' |

---

## pocaalbum_orders — 포카앨범 주문

| 컬럼 | 타입 | 설명 |
|---|---|---|
| order_date | DATE | 주문일자 |
| order_time | TIME | 주문일시 |
| store_name | STRING | 매장명 |
| product_code | STRING | 상품코드 |
| product_name | STRING | 상품명 |
| event_id | STRING | 이벤트 ID |
| artist_name | STRING | 아티스트명 |
| album_name | STRING | 앨범명 |
| album_qty | INTEGER | 앨범 수량 |
| order_qty | INTEGER | 구매 수량 |
| pay_amount | FLOAT | 결제액 |
| currency | STRING | 결제 통화 |

## pocaalbum_production — 포카앨범 제작 현황

Google Sheets 연동 테이블. BQ에서 직접 조회 불가 (Drive 권한 별도 필요).

| 컬럼 | 타입 | 설명 |
|---|---|---|
| release_date | DATE | 발매일 |
| category | STRING | 카테고리 |
| artist_name | STRING | 아티스트명 |
| album_name | STRING | 앨범명 |
| company_name | STRING | 소속사명 |
| total_quantity | FLOAT | 누적 제작수량 |
| memo | STRING | 비고 |

## pocaalbum_circlechart — 포카앨범 써클차트

| 컬럼 | 타입 | 설명 |
|---|---|---|
| year | INTEGER | 연도 |
| chart_count | FLOAT | 집계 수 |
