# TMS 스키마

_TMS(배송관리시스템). 송장·배송 추적 담당._

---


## delivery_invoice — 배송 송장 (배송 추적 핵심)

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 송장 레코드 고유 식별자 (PK) |
| order_id | bigint |  | OMS 주문 ID. 주문과 송장을 연결하는 외래키 |
| order_no | character varying |  | OMS 주문번호. 배송사/송장번호와 함께 유니크 제약조건 구성 |
| invoice_no | character varying |  | 운송장(송장) 번호. 배송 추적의 핵심 식별자 |
| carrier_code | character varying |  | 배송사 코드 (HANJIN/SF_EXPRESS/UPS 등). CarrierCode enum 참조 |
| source | character varying |  | 송장 등록 출처 (API/CALLBACK 등). DeliverySource enum 참조 |
| status_code | character varying |  | 배송 상태 코드. DeliveryStatus enum (PREPARING_FOR_SHIPMENT/IN_TRANSIT/DELIVERED 등) |
| raw_delivery_status | character varying | O | 외부 배송사로부터 받은 원본 배송 상태값 (정규화 전) |
| is_tracking | boolean |  | 배송 추적 활성화 여부. false면 GoodsFlow 등 추적 서비스에서 제외 |
| invoice_items | jsonb |  | 송장에 포함된 상품 목록 JSON. 상품명/수량/가격 등 포함 |
| invoice_total_amount | numeric | O | 송장 내 상품 총 금액 합계 |
| invoice_total_quantity | integer | O | 송장 내 상품 총 수량 합계 |
| created_at | timestamp without time zone |  | 레코드 생성 일시 |
| updated_at | timestamp without time zone |  | 레코드 최종 수정 일시 |
| location | text | O | 현재 배송 위치 정보 텍스트 |
| tracking_route_details | jsonb | O | 배송 경로 추적 상세 정보 JSON. 시간/위치/상태 이력 포함 |

## order_header — TMS 주문 헤더

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 주문 헤더 레코드 고유 식별자 (PK) |
| order_no | character varying |  | OMS 주문번호 (UK). 주문 식별의 핵심 키 |
| recipient_name | character varying |  | 수취인(수령인) 이름 |
| recipient_phone | character varying | O | 수취인 전화번호 |
| recipient_address | text | O | 수취인 배송 주소 (상세주소 포함) |
| sender_name | character varying |  | 발송인 이름 |
| sender_phone | character varying | O | 발송인 전화번호 |
| order_date | timestamp without time zone | O | 주문 일시 |
| payment_date | timestamp without time zone | O | 결제 완료 일시 |
| customer_memo | text | O | 고객이 작성한 주문 메모 |
| delivery_memo | text | O | 배송 요청 메모 (배송기사 전달용) |
| created_at | timestamp without time zone |  | 레코드 생성 일시 |
| updated_at | timestamp without time zone |  | 레코드 최종 수정 일시 |