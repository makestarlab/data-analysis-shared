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

---

## 뷰 테이블 (total_orders 파이프라인 핵심)

### vw_commerce_items_v2 — 상품 × SKU × 이벤트 통합 뷰 (권장)

상품-옵션-SKU-이벤트 관계를 하나로 펼친 핵심 룩업 뷰.
`vw_commerce_items`보다 컬럼이 풍부하므로 우선 사용.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| product_id | STRING | 대분류 ID |
| product_code | STRING | 대분류 코드 |
| product_name | STRING | 대분류명(앨범명) |
| product_release_at | TIMESTAMP | 상품 출시일 |
| artist_id | STRING | 아티스트 ID |
| artist_name | STRING | 아티스트명 |
| company_id | STRING | 소속사 ID |
| company_name | STRING | 소속사명 |
| product_event_id | STRING | 상품 ID |
| product_event_code | STRING | 상품코드 |
| product_event_name | STRING | 상품명 |
| product_event_type | STRING | 상품유형 (이벤트/펀딩/쇼핑) |
| product_event_market_type | STRING | 마켓 유형 |
| sales_start_at | TIMESTAMP | 판매 시작일 |
| sales_end_at | TIMESTAMP | 판매 종료일 |
| biz_type | STRING | 사업 유형 |
| announce_date | DATE | 공지 날짜 |
| event_date | DATE | 이벤트 날짜 |
| event_category_name | STRING | 이벤트 카테고리명 |
| product_option_index | INTEGER | 옵션 순서 |
| product_option_id | STRING | 옵션 ID |
| product_option_name | STRING | 옵션명 |
| product_option_group_name | STRING | 옵션 그룹명 |
| product_option_price | STRING | 옵션 판매가 |
| product_option_b2b_price | STRING | 옵션 B2B가 |
| product_option_content_type | INTEGER | 콘텐트 유형 |
| product_option_content_qty | INTEGER | 콘텐트 수량 |
| product_option_content_sales_base | STRING | 판매량 집계 기준 여부 |
| sku_code | STRING | SKU 코드 |
| sku_name | STRING | SKU명 |
| sku_type | STRING | P=부모 / C=자식 |
| sku_name_component_1 | STRING | SKU명 파싱 1 (event_id 추출에 사용) |
| sku_name_component_2 | STRING | SKU명 파싱 2 |
| parent_sku_code | STRING | 부모 SKU 코드 |
| first_publish_yn | STRING | 초도 여부 |
| purchase_price | NUMERIC | 매입가 |
| sku_is_album | STRING | 앨범 SKU 여부 |
| event_id | STRING | 이벤트 ID (total_orders.event_id 조인 키) |
| main_category_name | STRING | 대분류 카테고리명 |
| mid_category_name | STRING | 중분류 카테고리명 |
| category_name | STRING | 소분류 카테고리명 |
| production_company_product_code | STRING | 제작사 상품코드 |

### vw_commerce_orders — 커머스 주문 뷰

`pre_commerce_orders` 생성의 주문 소스. `new_commerce_db` 기준.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| order_id | STRING | 주문 ID |
| order_number | STRING | 주문번호 (식별번호) |
| order_status | STRING | 주문 상태 (코드값: data_lineage.md 참조) |
| order_type | STRING | B2B / B2C / ETC |
| payment_status | STRING | 결제 상태 |
| payment_method | STRING | 결제 수단 |
| pg_code | STRING | PG 코드 |
| logis_code | STRING | 배송사 코드 |
| user_id | INTEGER | 유저 ID |
| order_created_at | TIMESTAMP | 주문 생성일시 (UTC) |
| payment_at | TIMESTAMP | 결제일시 (UTC) |
| currency | STRING | 통화 |
| exchange_rate | FLOAT | 환율 (KRW 기준) |
| product_option_pay_amount | FLOAT | 상품 결제액 |
| logis_pay_amount | FLOAT | 배송비 |
| order_country_code | STRING | 주문 국가 |
| delivery_country_code | STRING | 배송 국가 |

### vw_commerce_order_items — 주문 라인아이템 뷰

| 컬럼 | 타입 | 설명 |
|---|---|---|
| order_id | STRING | 주문번호 |
| order_number | STRING | 식별번호 |
| product_event_id | STRING | 상품 ID |
| product_event_code | STRING | 상품코드 |
| product_event_type | STRING | 상품유형 (이벤트/펀딩/쇼핑) |
| product_event_name | STRING | 상품명 |
| product_id | STRING | 대분류 ID |
| product_code | STRING | 대분류 코드 |
| product_option_id | STRING | 옵션 ID |
| product_option_name | STRING | 옵션명 |
| product_option_pay_quantity | INTEGER | 옵션 구매 수량 |
| product_option_pay_amount | FLOAT | 옵션 결제액 |

### vw_product_option_info — 상품 옵션 × SKU 상세 뷰

`order_album_qty` 계산 시 `sales_qty` 사용 (`content_sales_base = 'true'` 필터).

| 컬럼 | 타입 | 설명 |
|---|---|---|
| artist_name | STRING | 아티스트명 |
| product_name | STRING | 대분류명(앨범명) |
| product_event_id | STRING | 상품 ID |
| product_event_code | STRING | 상품코드 |
| product_event_type | STRING | 상품유형 |
| product_option_id | STRING | 옵션 ID |
| product_option_name | STRING | 옵션명 |
| content_type_ko | STRING | 콘텐트명 |
| sku_info | STRING | SKU 정보 |
| content_sales_base | STRING | 판매량 집계 기준 여부 |
| sales_qty | INTEGER | 판매 단위 수량 (옵션 1개 = 앨범 N장) |
