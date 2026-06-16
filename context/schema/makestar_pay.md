# makestar-pay 스키마

_makestar-pay 서비스 전용 DB. PG 결제 처리 담당._

---


## tb_payment_payment — 결제 원장 (PG 결제 건)

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 결제 고유 식별자 (PK) |
| request_id | bigint |  | 결제 요청 메타 FK (tb_payment_request_meta) |
| status | integer |  | 결제 상태 코드 (READY/CONFIRMED/FAILED 등) |
| payment_method | text |  | 실제 결제 수단 문자열 |
| payment_key | text |  | PG 결제 식별자(paymentKey). 결제 조회/취소 API에서 사용되는 토큰성 식별자라 보안 민감. |
| response | jsonb |  | PG(Toss) 결제 응답 원본 JSON. 주요 키: mId; orderId; orderName; status; method; currency; totalAmount/balanceAmount; vat/suppliedAmount; approvedAt/requestedAt. 보안 민감: secret; transactionKey/lastTransactionKey; X-Tosspayments-Trace-Id; checkout.url. 결제수단 상세(card/easyPay 등) 포함 가능: card.number(마스킹된 카드번호); approveNo; issuerCode/acquirerCode; receiptUrl; installmentPlanMonths. |
| canceled_order_id_list | jsonb |  | 취소 처리된 주문 ID 목록 JSON |
| cancel_reason | text |  | 취소 사유 텍스트 |
| cancel_response | jsonb |  | PG(Toss) 취소 응답 원본 JSON. response와 유사한 메타(mId/orderId/status/paymentKey 등) + cancels 배열 포함 가능. cancels[] 예시 키: canceledAt; cancelAmount; cancelReason; cancelStatus; refundableAmount; taxAmount/taxFreeAmount/taxExemptionAmount; transactionKey. 보안 민감: secret; transactionKey/lastTransactionKey; receipt.url; checkout.url. |
| updated_at | timestamp with time zone |  | 변경 일시 |
| created_at | timestamp with time zone |  | 생성 일시 |
| canceled_at | timestamp with time zone | O | 취소 일시 |

## tb_payment_request_meta — 결제 요청 메타

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 결제 요청 메타 고유 식별자 (PK) |
| request_id | text |  | 결제 요청 ID (주문/결제 흐름 식별자 - PG 주문번호) |
| request_pg | integer |  | 요청한 PG 타입 (예: TOSS/EXIMBAY/WISE) |
| application | integer |  | 요청한 애플리케이션 타입 (예: COMMERCE/POCAALBUM/ALBUMBUDDY) |
| payment_method | text |  | 요청 시 지정된 결제 수단 문자열 |
| amount_info | jsonb |  | 금액 정보 JSON (value/currency 등) |
| product_info | jsonb |  | 주문/상품 정보 JSON |
| customer_info | jsonb |  | 주문자 정보 JSON. 예시 키: id(통합 customer_id); customerName(이름-개인정보); customerEmail(이메일-개인정보); customerMobilePhone(전화번호-개인정보); isB2BCustomer(B2B 여부-개인정보 아님). |
| additional_info | jsonb |  | 추가 정보 JSON (환불 계좌 등 개인정보/보안민감 정보 포함 가능) |
| confirm_url | character varying |  | 결제 완료 후 호출될 백엔드 콜백 URL |
| created_at | timestamp with time zone |  | 생성 일시 |

## tb_payment_method — 결제수단 정의

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 결제수단 고유 식별자 (PK) |
| request_pg | integer |  | 결제수단이 속한 PG 타입 |
| user_id | bigint | O | 사용자 FK (tb_auth_user) |
| is_active | boolean |  | 활성 여부 |
| customer_key | text |  | Toss CustomerKey (보안 민감) |
| billing_key | text |  | Toss BillingKey (보안 민감) |
| response | jsonb |  | 결제수단 등록 응답 원본 JSON (보안 민감 정보 포함 가능) |
| created_at | timestamp with time zone |  | 생성 일시 |

## tb_payment_payment_log — 결제 상태 변경 로그

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 결제 로그 고유 식별자 (PK) |
| payment_id | bigint |  | 결제 FK (tb_payment_payment) |
| before_status | integer |  | 결제 상태 변경 전 값 |
| after_status | integer |  | 결제 상태 변경 후 값 |
| response | jsonb |  | 상태 변경 시점의 PG 응답 JSON (보안 민감 정보 포함 가능) |
| created_at | timestamp with time zone |  | 생성 일시 |

## tb_auth_user — makestar-pay 서비스 유저 (pg_mystarroom와 별도 DB)

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 사용자 고유 식별자 (PK) |
| password | character varying |  | 암호화된 비밀번호 |
| last_login | timestamp with time zone | O | 마지막 로그인 일시 |
| is_superuser | boolean |  | Django 슈퍼유저 여부 |
| user_id | bigint |  | 통합 사용자 ID (레거시/외부 시스템 연동용) |
| email | character varying |  | 사용자 이메일 (로그인 ID) |
| is_active | boolean |  | 계정 활성 여부 |
| created_at | timestamp with time zone |  | 회원가입 일시 |
| updated_at | timestamp with time zone |  | 계정 정보 수정일시 |

## tb_auth_user_groups

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 사용자-권한그룹 관계 고유 식별자 (PK) |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |
| group_id | integer |  | 권한 그룹 FK (auth_group) |

## tb_auth_user_user_permissions

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 사용자-권한 관계 고유 식별자 (PK) |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |
| permission_id | integer |  | 권한 FK (auth_permission) |

## tb_task_in_task_item

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 태스크 아이템 고유 식별자 (PK) |
| task_id | text |  | Cloud Tasks 태스크 식별자 |
| status | integer |  | 태스크 처리 상태 코드 |
| relative_url | text |  | 호출 대상 URL 또는 relative URL |
| request_data | jsonb |  | 태스크 요청 데이터 JSON (환불 계좌 등 개인정보 포함 가능) |
| task_data | jsonb |  | Cloud Task 원본 데이터 JSON (헤더/바디 포함. 개인정보/보안민감 정보 포함 가능) |
| created_at | timestamp with time zone |  | 생성일시 |
| updated_at | timestamp with time zone |  | 수정일시 |

## tb_common_user_profile_image_file

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 사용자 프로필 이미지 고유 식별자 (PK) |
| filename | text |  | 파일명 |
| mime | character varying |  | 파일 MIME 타입 |
| is_active | boolean |  | 유효성 (삭제된 파일은 False) |
| created_at | timestamp with time zone |  | 생성일시 |
| origin | character varying |  | 원본 이미지 경로 |
| origin_size | integer |  | 원본 이미지 크기 (bytes) |
| thumb | character varying |  | 썸네일 이미지 경로 |
| thumb_size | integer |  | 썸네일 이미지 크기 (bytes) |
| width | integer |  | 가로 크기 (px) |
| height | integer |  | 세로 크기 (px) |
| exif | jsonb |  | EXIF 메타데이터 (JSON) |
| thumb_cropped | character varying |  | 크롭된 썸네일 이미지 경로 |
| thumb_cropped_size | integer |  | 크롭된 썸네일 이미지 크기 (bytes) |

## tb_backend_cached_data

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| cache_key | character varying |  | Django 캐시 키 |
| value | text |  | 캐시 데이터 값 |
| expires | timestamp with time zone |  | 캐시 만료 일시 |