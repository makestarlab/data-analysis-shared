# pg_oms_public 스키마

_OMS(주문관리시스템) 원본 DB. 물류·재고·SKU 관리._

---


## oms_order — 주문 원본 (OMS 핵심 테이블)

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 주문 레코드 고유 식별자 (PK) |
| order_id | character varying |  | OMS 주문 고유 번호 |
| order_status | character varying |  | 주문 상태 (ORDER_RECEIPT/DELIVERY_PREPARING 등) |
| customer_name | character varying |  | 주문자 이름 |
| customer_email | character varying |  | 주문자 이메일 |
| customer_telephone_no | character varying |  | 주문자 전화번호 |
| customer_country_code | character varying |  | 주문자 국가 코드 |
| customer_language_code | character varying |  | 주문자 언어 코드 (ko-KR/en-US 등) |
| receiver_zip_code | character varying |  | 수취인 우편번호 |
| receiver_address_state | character varying |  | 수취인 주소 - 시/도 |
| receiver_address_city | character varying |  | 수취인 주소 - 시/군/구 |
| receiver_address_1 | character varying |  | 수취인 주소 1 (기본주소) |
| receiver_address_2 | character varying |  | 수취인 주소 2 (상세주소) |
| poster_type | character varying |  | 포스터 배송 유형 (TUBE/FOLDED) |
| delivery_request_yn | character varying |  | 배송 요청 여부 (Y/N) |
| delivery_requested_at | timestamp without time zone | O | 배송 요청 처리 일시 |
| delivery_request_detail | character varying |  | 배송 요청 상세 내용 |
| receiver_email | character varying |  | 수취인 이메일 |
| receiver_name | character varying |  | 수취인 이름 |
| receiver_telephone_no | character varying |  | 수취인 전화번호 |
| receiver_country_code | character varying |  | 수취인 국가 코드 |
| logistics_code | character varying |  | 배송사 코드 |
| overseas_delivery | character varying |  | 해외 배송 여부 (Y/N) |
| payment_status | character varying |  | 결제 상태 (PAID/PENDING 등) |
| paid_at | timestamp without time zone | O | 결제 완료 일시 |
| currency_standard | character varying |  | 결제 통화 코드 (KRW/USD 등) |
| order_date | timestamp without time zone |  | 주문 일시 |
| created_at | timestamp without time zone |  | 레코드 생성 일시 |
| updated_at | timestamp without time zone |  | 레코드 최종 수정 일시 |
| sale_price | numeric |  | 주문 상품 총 판매가 |
| sale_price_usd | numeric |  | 주문 상품 총 판매가 (USD) |
| delivery_cost | numeric |  | 배송비 |
| delivery_cost_usd | numeric |  | 배송비 (USD 환산) |
| management_delivery_request_detail | character varying | O | 관리자 배송 요청 메모 |
| duties_and_taxes | numeric |  | 관세/세금 (주문 통화 기준) |
| duties_and_taxes_in_usd | numeric |  | 관세/세금 (USD 환산) |
| order_source | USER-DEFINED |  | 주문 채널 (메이크스타/웨이디엔) |

## oms_order_delivery_info — 배송 정보

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 배송정보 레코드 고유 식별자 (PK) |
| delivery_receipt_number | character varying | O | 배송 접수 번호 (내부 관리용) |
| order_id | character varying | O | OMS 주문번호 (FK to oms_order) |
| receiver_name | character varying |  | 수취인 이름 |
| overseas_delivery | character varying |  | 해외 배송 여부 |
| country_code | character varying |  | 배송 국가 코드 |
| telephone_no | character varying |  | 수취인 연락처 |
| receiver_email | character varying |  | 수취인 이메일 주소 |
| zip_code | character varying |  | 배송지 우편번호 |
| address | character varying |  | 배송지 기본 주소 |
| address_detail | character varying | O | 배송지 상세 주소 |
| address_detail_2 | character varying | O | 배송지 상세 주소 2 |
| address_state | character varying | O | 배송지 시/도 |
| address_city | character varying | O | 배송지 시/군/구 |
| delivery_request_detail | character varying | O | 배송 요청 메모 |
| delivery_status | character varying |  | 배송 진행 상태 |
| delivery_delay_yn | character varying |  | 배송 지연 플래그 (Y/N) |
| logistics_code | character varying | O | 배송사 식별 코드 |
| tracking_number | character varying | O | 운송장 번호 |
| hs_code | character varying | O | 통관용 HS 코드 |
| invoice_price | numeric | O | 세관 신고용 상품 가액 |
| delivery_receipt_datetime | timestamp without time zone |  | 배송 접수 처리 일시 |
| delivery_processing_datetime | timestamp without time zone | O | 출고 처리 일시 |
| delivery_completion_datetime | timestamp without time zone | O | 배송 완료 일시 |
| delivery_deadline_datetime | timestamp without time zone | O | 배송 완료 목표 일시 |
| return_reason | character varying | O | 반송/반품 사유 |
| modification_id | character varying | O | 마지막 수정한 관리자 ID |
| modification_datetime | timestamp without time zone | O | 레코드 최종 수정 일시 |
| auto_modification_datetime | timestamp without time zone | O | 시스템 자동 변경 일시 |

## oms_order_delivery_parcel_info — 택배 송장 정보

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 소포 정보 레코드 고유 식별자 (PK) |
| order_id | character varying |  | OMS 주문번호 (FK to oms_order) |
| delivery_receipt_number | character varying |  | 내부 배송 접수 번호 |
| parcel_number | character varying |  | 박스/소포 식별 번호 |
| delivery_status | character varying | O | 소포 배송 상태 |
| logistics_code | character varying |  | 배송사 코드 |
| tracking_number | character varying |  | 운송장 번호 |
| delivery_process_date | timestamp without time zone | O | 출고 처리 일시 |
| delivery_complete_date | timestamp without time zone | O | 배송 완료 일시 |
| modifier_id | character varying |  | 마지막 수정한 관리자 ID |
| register_id | character varying |  | 소포 등록한 관리자 ID |
| trace_yn | character varying |  | 배송 추적 활성화 여부 (Y/N) |
| delay_yn | character varying |  | 배송 지연 플래그 (Y/N) |
| created_at | timestamp without time zone |  | 레코드 생성 일시 |
| updated_at | timestamp without time zone |  | 레코드 최종 수정 일시 |
| tracking_route_details | jsonb | O | 배송 경로 이력 JSON |

## oms_order_product — 주문 상품

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 주문 상품 레코드 고유 식별자 (PK) |
| order_id | character varying |  | OMS 주문번호 (FK to oms_order) |
| product_id | character varying |  | 메이크스타 상품 ID |
| product_type | character varying |  | 상품 유형 (PRODUCT/PROJECT) |
| option_id | character varying |  | 상품 옵션 ID |
| currency_standard | character varying |  | 결제 통화 코드 |
| total_paid_amount | numeric |  | 상품별 결제 금액 |
| order_quantity | integer |  | 주문 수량 |
| cancel_quantity | integer | O | 취소 수량 |
| hs_code | character varying | O | 통관용 HS 코드 |
| description_for_customs | character varying | O | 세관 신고용 상품 설명 |

## oms_order_line_item_sku — 주문 라인아이템 × SKU

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 주문 SKU 항목 레코드 고유 식별자 (PK) |
| order_no | character varying |  | OMS 주문번호 (FK to oms_order) |
| order_line_item_no | integer | O | 주문 내 상품 순번 |
| parcel_number | character varying | O | 할당된 소포 번호 |
| product_code | character varying |  | 메이크스타 상품 코드 |
| product_type | character varying |  | 채널 유형 — NCM_EVENT / NCM_SHOPPING / SHOPPING / NCM_FUNDING (아래 코드값 참조) |
| option_code | character varying | O | 상품 옵션/리워드 코드 |
| sku_line_item_no | integer | O | SKU 항목 순번 |
| sku_code | character varying |  | 할당된 SKU 코드 |
| bulk_purchase_reward_yn | character varying |  | 대량구매 특전 SKU 여부 |
| quantity | integer |  | SKU 할당 수량 |
| register_id | character varying |  | SKU 할당한 관리자 ID |
| created_at | timestamp without time zone | O | 레코드 생성 일시 |
| updated_at | timestamp without time zone | O | 레코드 최종 수정 일시 |

## mst_sku — SKU 마스터

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| sku_code | character varying |  | SKU 고유 코드 (SKU + 숫자) |
| sku_name | character varying |  | SKU 상품명 |
| sku_type | character |  | P: 부모/C: 자식 (랜덤 포토카드 등) |
| parent_sku_code | character varying |  | 자식 SKU인 경우 부모 SKU 코드 |
| distribution_code | character varying | O | 외부 유통사 코드 (바코드 등) |
| category_code | character varying |  | SKU 카테고리 코드 (FK to mst_sku_category) |
| first_publish_yn | character varying |  | 초도(발매일 전) 상품 여부 |
| first_publish_sku_code | character varying | O | 초도 상품의 일반 판매 SKU 코드 |
| sku_description | character varying |  | SKU 상세 설명 |
| price | numeric |  | 소비자 판매가 |
| purchase_price | numeric |  | 공급처 매입가 |
| issue_date | date | O | 상품 공식 발매일 |
| weight | numeric |  | 상품 무게 |
| length | numeric |  | 박스 가로 길이 |
| width | numeric |  | 박스 세로 길이 |
| height | numeric |  | 박스 높이 |
| volume | numeric |  | 상품 부피 |
| thumbnail | character varying |  | 섬네일 이미지 URL |
| full_image | character varying |  | 상품 상세 이미지 URL |
| first_week_closing_date | date | O | 앨범 초동 집계 마감일 |
| last_order_closing_date | date | O | 발주 가능 마감일 |
| use_yn | character varying |  | SKU 사용/미사용 상태 (Y/N) |
| reg_id | character varying |  | SKU 등록한 관리자 ID |
| taxation_yn | character varying | O | 부가세 과세 여부 (Y/N) |
| reg_dttm | timestamp without time zone |  | 레코드 생성 일시 |
| mod_id | character varying | O | 마지막 수정한 관리자 ID |
| mod_dttm | timestamp without time zone | O | 레코드 최종 수정 일시 |
| sku_name_component_1 | character varying | O | SKU명 파싱 첫 번째 구성요소 |
| sku_name_component_2 | character varying | O | SKU명 파싱 두 번째 구성요소 |
| virtual_child_sku_count | integer |  | 포카 종류 수 (멤버 수×버전). 풀세트 구매 판별 기준. child_sku_count_in_use보다 신뢰도 높음 |
| child_sku_count_in_use | integer |  | 실제 사용 중인 자식 SKU 수 |
| artist_id | integer |  | 아티스트 ID (FK to oms_artist) |
| vendor_id | bigint |  | SKU 공급처 ID |
| production_company_id | bigint |  | 실제 제작 업체 ID |
| production_company_product_code | character varying | O | 제작사 내부 제품 코드 |
| sku_code_normalized | character varying | O | 검색용 정규화된 SKU 코드 |
| sku_name_normalized | character varying | O | 검색용 정규화된 SKU명 |
| production_company_product_code_normalized | character varying | O | 검색용 정규화된 제작사 코드 |
| vendor_pack_size | integer |  | 공급처 최소 출고 단위 |

## mst_sku_category — SKU 카테고리

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| category_code | character varying |  | 카테고리 고유 코드 (PK) |
| ctgr_div | character varying |  | 카테고리 계층 구분 |
| main_ctgr_cd | character varying | O | 대분류 카테고리 코드 |
| mid_ctgr_cd | character varying | O | 중분류 카테고리 코드 |
| ctgr_nm | character varying |  | 카테고리 표시명 |
| ctgr_desc | character varying | O | 카테고리 상세 설명 |
| hs_code | character varying | O | 국제 통관 HS코드 |
| description_for_customs | character varying | O | 통관용 상품명 |
| ctgr_order | integer |  | 카테고리 정렬 순서 |
| reg_id | character varying |  | 카테고리 등록한 관리자 ID |
| reg_dttm | timestamp without time zone |  | 레코드 생성 일시 |
| mod_id | character varying | O | 마지막 수정한 관리자 ID |
| mod_dttm | timestamp without time zone | O | 레코드 최종 수정 일시 |
| record_yn | character varying |  | 카테고리 유효 상태 (Y/N) |
| bulk_purchase_condition_yn | character varying |  | 대량구매 특전 적용 카테고리 여부 |
| weight | numeric |  | 카테고리 기본 무게 |
| length | numeric |  | 카테고리 기본 가로 길이 |
| width | numeric |  | 카테고리 기본 세로 길이 |
| height | numeric |  | 카테고리 기본 높이 |
| volume | numeric |  | 카테고리 기본 부피 |
| max_box_quantity | integer | O | 박스당 최대 적재 수량 |

## oms_product — 상품 마스터

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | OMS 상품 레코드 고유 식별자 (PK) |
| product_id | character varying |  | 메이크스타 상품 ID |
| product_type | character varying |  | 상품 유형 (PRODUCT/PROJECT) |
| event_type | character varying | O | 이벤트 유형 (펀딩/프리오더 등) |
| option_id | character varying |  | 상품 옵션 ID |
| album_quantity | integer | O | 앨범 포함 수량 (초동 집계용) |
| sale_price | jsonb |  | 판매가 다통화 JSON |
| end_date | timestamp without time zone | O | 판매 종료일 |
| event_id | character varying | O | 메이크스타 이벤트 ID |
| created_at | timestamp without time zone |  | 레코드 생성 일시 |
| updated_at | timestamp without time zone |  | 레코드 최종 수정 일시 |
| maximum_quantity_per_box | integer | O | 박스당 최대 적재 수량 |
| product_name | jsonb | O | 상품명 다국어 JSON |
| option_name | jsonb | O | 옵션명 다국어 JSON |
| hs_code | character varying | O | 통관용 HS 코드 |
| description_for_customs | character varying | O | 세관 신고용 상품 설명 |
| release_date | timestamp without time zone | O | 상품 공식 발매일 |
| opportunity_type_list | jsonb | O | 기회 유형 목록 JSON |
| display_channels | jsonb | O | 판매 채널 목록 JSON |

## oms_product_option_item — 상품 옵션 아이템

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 품목 레코드 고유 식별자 (PK) |
| product_code | character varying |  | 메이크스타 상품 코드 |
| product_type | character varying |  | 상품 유형 (PRODUCT/PROJECT) |
| option_code | character varying |  | 상품 옵션 코드 |
| item_code | character varying |  | 품목 고유 코드 |
| item_name | character varying |  | 품목 표시명 |
| kit_code | character varying |  | 연결된 KIT/SKU 코드 |
| kit_type | character varying |  | KIT/SKU 구분 |
| delivery_type | character varying |  | 배송 방식 (PARCEL/DIGITAL 등) |
| number_of_delivery_units | integer |  | 품목당 배송 단위 수량 |
| variety_count | integer |  | 품목 내 종류 수 (랜덤 상품 등) |
| sku_code_list | jsonb |  | 연결된 SKU 목록 JSON |
| created_at | timestamp without time zone |  | 레코드 생성 일시 |
| updated_at | timestamp without time zone | O | 레코드 최종 수정 일시 |
| created_by | character varying |  | 품목 등록한 관리자 ID |
| updated_by | character varying | O | 마지막 수정한 관리자 ID |

## oms_shipping_costs — 배송비 기준

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 배송비 테이블 레코드 고유 식별자 (PK) |
| carrier_code | character varying |  | 배송사 코드 |
| country_code | character varying |  | 배송 국가 코드 |
| max_weight_kg | numeric |  | 최대 중량 (kg) |
| price_krw | integer |  | 배송비 (원) |
| price_per | character varying |  | 단위 (BOX/KG 등) |

## oms_shipping_margin_rates — 배송비 마진율

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 배송 마진율 레코드 고유 식별자 (PK) |
| country_code | character varying |  | 배송 국가 코드 |
| carrier_code | character varying |  | 배송사 코드 |
| margin_rate | numeric |  | 배송비 마진율 (%) |

## oms_stock_item_quantity — 재고 수량

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | integer |  | 재고 수량 레코드 고유 식별자 (PK) |
| sku_code | character varying |  | SKU 코드 (FK to mst_sku) |
| available_quantity | integer |  | 주문 가능 재고 수량 |
| allocated_quantity | integer |  | 주문에 할당된 재고 수량 |
| held_quantity | integer |  | 출고 보류 중인 재고 수량 |
| lost_or_damaged_quantity | integer |  | 분실/파손 재고 수량 |
| total_quantity | integer | O | 총 재고 수량 (계산 필드) |
| safety_quantity | integer | O | 안전 재고 기준 수량 |

## oms_task — OMS 작업

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | Cloud Task 마스터 레코드 고유 식별자 (PK) |
| cloud_task_id | character varying |  | GCP Cloud Tasks 태���크 ID |
| idempotency_key | character varying |  | 중복 실행 방지용 고유 키 |
| task_type | character varying |  | 태스크 처리 유형 코드 |
| failure_reason | character varying | O | 태스크 실패 시 상세 사유 |
| total_count | integer |  | 처리 대상 아이템 총 개수 |
| completed_count | integer |  | 처리 완료된 아이템 수 |
| business_failed_count | integer |  | 비즈니스 로직 실패 아이템 수 |
| failed_count | integer |  | 시스템 오류 실패 아이템 수 |
| payload | jsonb |  | 태스크 실행 파라미터 JSON |
| status | character varying |  | 태스크 진행 상태 (PENDING/RUNNING/COMPLETED 등) |
| cloud_task_name | character varying | O | GCP Cloud Tasks 전체 이름 |
| cloud_task_queue | character varying | O | GCP Cloud Tasks 큐 이름 |
| created_at | timestamp with time zone |  | 레코드 생성 일시 |
| updated_at | timestamp with time zone |  | 레코드 최종 수정 일시 |

## spm_logistics — SPM 물류 정보

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| logis_cd | character varying |  | 배송사 고유 코드 (PK) |
| logis_nm | character varying |  | 배송사 표시명 |
| logis_stat | character varying |  | 배송사 활성 상태 (Y/N) |
| ovs_dlvy | character varying |  | 해외 배송 지원 여부 (Y/N) |
| tel_no | character varying | O | 배송사 연락처 |
| ods_file_nm | character varying |  | 주문서 템플릿 파일명 |
| ods_file_url | character varying |  | 주문서 템플릿 다운로드 URL |
| dlvy_fee_file_nm | character varying | O | 배송비 표 파일명 |
| dlvy_fee_file_url | character varying | O | 배송비 표 다운로드 URL |
| reg_id | character varying |  | 배송사 등록한 관리자 ID |
| reg_dttm | timestamp without time zone |  | 레코드 생성 일시 |
| mod_id | character varying | O | 마지막 수정한 관리자 ID |
| mod_dttm | timestamp without time zone | O | 레코드 최종 수정 일시 |
| goodsflow_cd | character varying | O | GoodsFlow 연동 배송사 코드 |
| hp_url | character varying | O | 배송사 홈페이지 URL |
| tracking_url | character varying | O | 배송 추적 페이지 URL 패턴 |
| combined_weighted_value | numeric |  | 합배송 무게 계산 가중치 |
| max_weight_per_box | numeric |  | 박스당 최대 허용 무게 (mg) |
| max_cnt_product_per_box | integer |  | 박스당 최대 상품 수 |
| max_cnt_paper_tube | integer |  | 포스터 지관통 최대 수 |
| max_poster_cnt_per_paper_tube | integer | O | 지관통당 포스터 최대 수 |
| min_weight_per_box | numeric |  | 박스당 최소 무게 (mg) |
| additional_exchange_rate_difference | jsonb | O | 통화별 추가 환율 차액 JSON |
| divisor_weight_for_convert_volume_to_weight | numeric | O | 부피 → 무게 환산 계수 |
| box_sub_material_weighted_value | numeric |  | 포장재 무게 가중치 |
| logis_buy_limit_count_yn | character varying | O | 구매 수량 제한 적용 여부 |

## spm_shipping_cntry_manage — SPM 배송 국가 관리

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| logis_cd | character varying |  | 배송사 코드 (PK/FK to spm_logistics) |
| cntry_cd | character varying |  | 국가 코드 (PK) |
| use_yn | character varying |  | 해당 국가 배송 가능 여부 (Y/N) |
| reg_id | character varying |  | 레코드 등록한 관리자 ID |
| reg_dttm | timestamp without time zone |  | 레코드 생성 일시 |
| mod_id | character varying | O | 마지막 수정한 관리자 ID |
| mod_dttm | timestamp without time zone | O | 레코드 최종 수정 일시 |