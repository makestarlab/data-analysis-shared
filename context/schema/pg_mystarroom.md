# pg_mystarroom_public 스키마

_자동 생성 — `scripts/refresh_schema.py` 실행으로 갱신_


## tb_auth_log — 로그인/가입 로그 (NRU: log_type=0)

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER |  |
| log_type | INTEGER |  |
| service_name | STRING |  |
| created_at | TIMESTAMP |  |
| user_id | INTEGER |  |
| datastream_metadata | RECORD |  |

## tb_commerce_order — 결제 원본

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER |  |
| order_number | STRING |  |
| order_status | INTEGER |  |
| shipping_information | JSON |  |
| event_join_information | JSON |  |
| ordered_data | JSON |  |
| payment_data | JSON |  |
| cancel_reason_type | INTEGER |  |
| cancel_memo | STRING |  |
| canceled_at | TIMESTAMP |  |
| created_at | TIMESTAMP |  |
| updated_at | TIMESTAMP |  |
| user_id | INTEGER |  |
| payment_request_id | STRING |  |
| event_pk_list | JSON |  |
| searching_event_text | STRING |  |
| index | INTEGER |  |
| event_ticket_information | JSON |  |
| cancel_requested_ordered_data | JSON |  |
| refund_at | TIMESTAMP |  |
| refund_data | JSON |  |
| refund_memo | STRING |  |
| refund_reason_type | INTEGER |  |
| refund_status | INTEGER |  |
| ip_address | STRING |  |
| ip_address_info_id | INTEGER |  |
| user_order_number | STRING |  |
| datastream_metadata | RECORD |  |
| approved_at | TIMESTAMP |  |
| shipping_process_started_at | TIMESTAMP |  |
| payment_status | STRING |  |
| delivery_requested | BOOLEAN |  |
| stock_allocation_type | STRING |  |
| product_event_type | STRING |  |
| shipping_method | STRING |  |
| recipient_name | STRING |  |
| stock_allocated_at | TIMESTAMP |  |
| delivery_requested_at | TIMESTAMP |  |
| last_released_at | TIMESTAMP |  |
| payment_method | STRING |  |
| user_group_id | INTEGER |  |
| shipment_confirmed_at | TIMESTAMP |  |

## tb_auth_user — 유저 계정

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER |  |
| password | STRING |  |
| last_login | TIMESTAMP |  |
| email | STRING |  |
| is_admin | BOOLEAN |  |
| is_active | BOOLEAN |  |
| is_certified | BOOLEAN |  |
| created_at | TIMESTAMP |  |
| updated_at | TIMESTAMP |  |
| is_superuser | BOOLEAN |  |
| user_idx | INTEGER |  |
| is_withdrawn | BOOLEAN |  |
| is_operator | BOOLEAN |  |
| user_type | INTEGER |  |
| created_from | STRING |  |
| withdrawn_at | TIMESTAMP |  |
| datastream_metadata | RECORD |  |
| has_group | BOOLEAN |  |

## tb_auth_user_information — 유저 프로필

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER |  |
| birth | TIMESTAMP |  |
| created_at | TIMESTAMP |  |
| updated_at | TIMESTAMP |  |
| user_id | INTEGER |  |
| nickname | STRING |  |
| profile_image_id | INTEGER |  |
| is_agreed_marketing | BOOLEAN |  |
| is_agreed_updated_notification | BOOLEAN |  |
| phone | STRING |  |
| real_name | STRING |  |
| agreed_marketing_services | JSON |  |
| available_services | JSON |  |
| datastream_metadata | RECORD |  |
| country_code | STRING |  |
| gender_type | INTEGER |  |

## tb_artist_artist — 아티스트

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER |  |
| artist_type | INTEGER |  |
| published_at | TIMESTAMP |  |
| homepage | STRING |  |
| site_info | JSON |  |
| created_at | TIMESTAMP |  |
| updated_at | TIMESTAMP |  |
| profile_image_id | INTEGER |  |
| name | STRING |  |
| company_id | INTEGER |  |
| introduction | STRING |  |
| nickname | STRING |  |
| datastream_metadata | RECORD |  |
| index | INTEGER |  |
| i18n_name | JSON |  |
| is_displayed | BOOLEAN |  |
| logo_image_id | INTEGER |  |
| brand_idx | INTEGER |  |
| is_active | BOOLEAN |  |
| fandom_name | STRING |  |
| i18n_artist_description | JSON |  |
