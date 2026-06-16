# production 스키마

_자동 생성 — `scripts/refresh_schema.py` 실행으로 갱신_


## project — SPM 프로젝트(이벤트) 원본

| 컬럼 | 타입 | 설명 |
|---|---|---|
| idx | INTEGER |  |
| id | STRING |  |
| url | STRING |  |
| title | STRING |  |
| type | STRING |  |
| project_type | STRING |  |
| creator_type | STRING |  |
| funding_type | STRING |  |
| funding_subtype | STRING |  |
| is_plux | INTEGER |  |
| goal | INTEGER |  |
| sdate | DATETIME |  |
| edate | DATETIME |  |
| pre_open_date | DATETIME |  |
| estimated_delivery_date | DATETIME |  |
| refund_end_date | DATETIME |  |
| status | STRING |  |
| post_status | STRING |  |
| post_status_update_date | DATETIME |  |
| collect_won | INTEGER |  |
| collect_dollar | FLOAT |  |
| followers | INTEGER |  |
| exchange | FLOAT |  |
| creator_idx | INTEGER |  |
| manager_id | STRING |  |
| delivery_allow | JSON |  |
| ticket_limit_count | INTEGER |  |
| write_date | TIMESTAMP |  |
| order_num | INTEGER |  |
| order_conditions | JSON |  |
| icon | STRING |  |
| view_count | INTEGER |  |
| comment_count | INTEGER |  |
| stretch_goals_percent | STRING |  |
| project_category | STRING |  |
| milestone | INTEGER |  |
| brand_idx | INTEGER |  |
| order_modifying_restrict_date | DATETIME |  |
| include_delivery_fee | INTEGER |  |
| super_pinned_thread_idx | INTEGER |  |
| has_item | INTEGER |  |
| hero_image_path | STRING |  |
| renewal | INTEGER |  |
| reward_name_required | INTEGER |  |
| url_en_date | TIMESTAMP |  |
| url_st_date | TIMESTAMP |  |
| comment_status | STRING |  |
| reward_exchange_date | TIMESTAMP |  |
| reward_exchange_i18n | JSON |  |
| currency_i18n | JSON |  |
| exchange_rate_i18n | JSON |  |
| exchange_date | TIMESTAMP |  |
| exchange_i18n | JSON |  |
| delivery | JSON |  |
| payment_method | JSON |  |
| address_control_date | TIMESTAMP |  |
| group_purchase_url | STRING |  |
| group_purchase | STRING |  |
| receive_delivery_fee_type | STRING |  |
| msg_div | JSON |  |
| same_identification_buy_limit | INTEGER |  |
| same_identification_buy_limit_count | INTEGER |  |
| _backers | INTEGER |  |
| _remain_reward_count | INTEGER |  |
| _total_reward_count | INTEGER |  |
| _payment_methods | INTEGER |  |
| _deliveries | INTEGER |  |
| _post_status | STRING |  |
| _status | STRING |  |
| _creator_type | STRING |  |
| _funding_type | STRING |  |
| _funding_subtype | STRING |  |
| _project_type | STRING |  |
| _sdate | DATETIME |  |
| _edate | DATETIME |  |
| refundable | INTEGER |  |
| AUTO_MOD_DTTM | DATETIME |  |

## user — 구 유저 테이블

| 컬럼 | 타입 | 설명 |
|---|---|---|
| idx | INTEGER |  |
| email | STRING |  |
| passwd | STRING |  |
| name | STRING |  |
| real_name | STRING |  |
| grade | STRING |  |
| role | STRING |  |
| locale | STRING |  |
| picture | STRING |  |
| auto_login | STRING |  |
| activated_date | TIMESTAMP |  |
| login_date | TIMESTAMP |  |
| write_date | TIMESTAMP |  |
| old_idx | INTEGER |  |
| email_subscribe | INTEGER |  |
| last_latitude | STRING |  |
| last_longitude | STRING |  |
| last_country_code | STRING |  |
| last_ip | STRING |  |
| selected_badge_idx | INTEGER |  |
| terms_level | INTEGER |  |
| external_code | STRING |  |
| birthday | DATE |  |
| gender | STRING |  |
| country_code | STRING |  |
| converted_email | STRING |  |
| invalid_email | INTEGER |  |
| country_code_publish | INTEGER |  |
| partner_idx | INTEGER |  |
| join_ymdh | INTEGER |  |
| login_ymdh | INTEGER |  |
| active_status | STRING |  |
| editor | STRING | 수정자 |
| edit_date | TIMESTAMP | 수정일시 |
| withdrawal_date | TIMESTAMP | 탈퇴일자 |
| AUTO_MOD_DTTM | DATETIME | 마지막 데이터 변경 발생 시점 ( 자동 업데이트 ) - 2022.10.31 현재 데이터이관( BigQuery ) 기준 컬럼 |
