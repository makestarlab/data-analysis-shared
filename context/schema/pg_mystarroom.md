# pg_mystarroom_public 스키마

_자동 생성 — `scripts/refresh_schema.py` 실행으로 BQ 컬럼 갱신, Excel로 도메인 설명 보강_

---

## 데이터 출처

Makestar 서비스 원본 Postgres DB → BigQuery CDC (Datastream)

---

## tb_auth_log — 로그인·탈퇴 로그 (NRU 기준 아님 — tb_auth_user.is_certified 사용)

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 인증 로그 고유 식별자 (PK) |
| log_type | integer |  | 로그 타입 (0:가입, 1:탈퇴 등) |
| service_name | text |  | 호출한 서비스명 (MAKESTAR, POCAALBUM 등) |
| created_at | timestamp with time zone |  | 로그 생성일시 |
| user_id | bigint | O | 사용자 FK (tb_auth_user) |

## tb_auth_user — 유저 계정

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 사용자 고유 식별자 (PK) |
| password | character varying |  | 암호화된 비밀번호 |
| last_login | timestamp with time zone | O | 마지막 로그인 일시 |
| email | character varying |  | 사용자 이메일 (로그인ID) |
| is_admin | boolean |  | 관리자 여부 |
| is_active | boolean |  | 계정 활성 여부 |
| is_certified | boolean |  | 이메일 인증 완료 여부 |
| created_at | timestamp with time zone |  | 회원가입 일시 |
| updated_at | timestamp with time zone |  | 계정 정보 수정일시 |
| is_superuser | boolean |  | Django 슈퍼유저 여부 |
| user_idx | bigint | O | 레거시 DB 사용자 인덱스 |
| is_withdrawn | boolean |  | 탈퇴 여부 |
| is_operator | boolean |  | 오퍼레이터 권한 여부 |
| user_type | integer |  | 사용자 타입 (MAKESTAR, POCAALBUM 등) |
| created_from | text |  | 가입 경로 (어느 서비스에서 가입) |
| withdrawn_at | timestamp with time zone | O | 탈퇴 일시 |
| has_group | boolean |  | B2B 그룹 소속 여부 |

## tb_auth_user_information — 유저 프로필 (닉네임·국가·생년월일)

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 사용자 상세 정보 고유 식별자 (PK) |
| birth | timestamp with time zone | O | 생년월일 |
| created_at | timestamp with time zone |  | 정보 등록일시 |
| updated_at | timestamp with time zone |  | 정보 수정일시 |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |
| nickname | character varying |  | 닉네임 |
| profile_image_id | bigint | O | 프로필 이미지 FK |
| is_agreed_marketing | boolean |  | 포카앨범 마케팅 수신 동의 |
| is_agreed_updated_notification | boolean |  | 업데이트 알림 수신 동의 |
| phone | character varying |  | 전화번호 |
| real_name | character varying |  | 실명 |
| agreed_marketing_services | ARRAY |  | 마케팅 수신 동의 서비스 목록 (Array) |
| available_services | ARRAY |  | 약관 동의 서비스 목록 (Array) |
| country_code | character varying |  | 국가 코드 |
| gender_type | integer |  | 성별 (0:여성, 1:남성, 3:알수없음) |

## tb_auth_user_address — 배송지 정보

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 배송지 주소 고유 식별자 (PK) |
| is_main | boolean |  | 기본 배송지 여부 |
| nickname | text |  | 배송지 별명 |
| surname | text |  | 성 |
| given_name | text |  | 이름 |
| country_code | character varying |  | 국가 코드 (ISO 3166-1 alpha-2) |
| phone | text |  | 전화번호 |
| zip_code | character varying |  | 우편번호 |
| address | text |  | 주소 |
| detail_address | text |  | 상세 주소 |
| city | text |  | 도시명 |
| state | text |  | 주/도 |
| created_at | timestamp with time zone |  | 배송지 등록일시 |
| updated_at | timestamp with time zone |  | 배송지 수정일시 |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |
| additional_info | jsonb |  | 추가 정보 (신분확인번호 등, JSON) |
| identity_image_back_id | bigint | O | 신분증 뒷면 이미지 FK |
| identity_image_front_id | bigint | O | 신분증 앞면 이미지 FK |

## tb_auth_user_event_info — 이벤트 응모 정보

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 이벤트 참여 정보 고유 식별자 (PK) |
| is_main | boolean |  | 기본 참여 정보 여부 |
| nickname | text |  | 이벤트용 닉네임 |
| phone | text |  | 전화번호 |
| year | integer |  | 생년 |
| month | integer |  | 생월 |
| day | integer |  | 생일 |
| messenger | integer |  | 메신저 타입 (0:카카오, 1:라인 등) |
| created_at | timestamp with time zone |  | 정보 등록일시 |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |
| messenger_id | text |  | 메신저 ID |
| real_name | text |  | 실명 |
| country_code | character varying |  | 국가 코드 |
| email | character varying |  | 이메일 |
| language | ARRAY |  | 사용 언어 목록 (Array) |
| surname | character varying |  | 성 |
| nationality | character varying | O | 국적 |

## tb_auth_social_account — 소셜 로그인 연동 계정

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 소셜 계정 연동 고유 식별자 (PK) |
| make_star | text |  | 메이크스타 소셜 ID |
| google | text |  | 구글 소셜 ID |
| twitter | text |  | 트위터(X) 소셜 ID |
| facebook | text |  | 페이스북 소셜 ID |
| apple | text |  | 애플 소셜 ID |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |
| kakao | text |  | 카카오 소셜 ID |
| naver | text |  | 네이버 소셜 ID |
| apple_data | jsonb |  | 애플 연동 데이터 (JSON) |
| facebook_data | jsonb |  | 페이스북 연동 데이터 (JSON) |
| google_data | jsonb |  | 구글 연동 데이터 (JSON) |
| kakao_data | jsonb |  | 카카오 연동 데이터 (JSON) |
| make_star_data | jsonb |  | 메이크스타 연동 데이터 (JSON) |
| naver_data | jsonb |  | 네이버 연동 데이터 (JSON) |
| twitter_data | jsonb |  | 트위터(X) 연동 데이터 (JSON) |
| spotify | text |  | 스포티파이 소셜 ID |
| spotify_data | jsonb |  | 스포티파이 연동 데이터 (JSON) |

## tb_auth_withdraw_user — 탈퇴 유저

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 탈퇴 사용자 기록 고유 식별자 (PK) |
| user_data | jsonb |  | 탈퇴 시점 사용자 데이터 (JSON) |
| user_auth_data | jsonb |  | 탈퇴 시점 인증 데이터 (JSON) |
| withdrawn_at | timestamp with time zone |  | 최종 탈퇴 일시 |
| user_id | bigint |  | 사용자 FK (tb_auth_user) |

## tb_artist_artist — 아티스트

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 아티스트 고유 식별자 (PK) |
| artist_type | integer |  | 아티스트 타입 (0:그룹, 1:솔로) |
| published_at | timestamp with time zone | O | 아티스트 데뷔일 |
| homepage | character varying | O | 아티스트 공식 홈페이지 URL |
| site_info | jsonb |  | 아티스트 SNS 정보 (JSON) |
| created_at | timestamp with time zone |  | 아티스트 등록일시 |
| updated_at | timestamp with time zone |  | 아티스트 최종 수정일시 |
| profile_image_id | bigint | O | 프로필 이미지 FK (tb_common_profile_image_file) |
| name | character varying |  | 아티스트 이름 |
| company_id | bigint | O | 소속사 FK (tb_artist_company) |
| introduction | text |  | 아티스트 소개 문구 |
| nickname | text |  | 아티스트 별명/닉네임 (검색용) |
| brand_idx | integer |  | 레거시 브랜드 인덱스 |
| i18n_name | jsonb |  | 아티스트 이름 다국어 (JSON) |
| index | integer |  | 아티스트 정렬 순번 |
| is_displayed | boolean |  | 앱 노출 여부 |
| logo_image_id | bigint | O | 로고 이미지 FK (tb_common_profile_image_file) |
| is_active | boolean |  | 아티스트 활성 여부 |
| fandom_name | character varying |  | 팬덤 이름 |
| i18n_artist_description | jsonb |  | 아티스트 설명 다국어 (JSON) |

## tb_artist_artist_member — 아티스트 멤버

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 아티스트 멤버 고유 식별자 (PK) |
| born_at | timestamp with time zone | O | 멤버 생년월일 (레거시) |
| blood_type | integer |  | 멤버 혈액형 (0:O, 1:A, 2:B, 3:AB, 4:알수없음) |
| height | double precision |  | 멤버 키 (cm) |
| weight | double precision |  | 멤버 몸무게 (kg) |
| position | text |  | 멤버 포지션 (보컬, 래퍼 등) |
| created_at | timestamp with time zone |  | 멤버 등록일시 |
| updated_at | timestamp with time zone |  | 멤버 최종 수정일시 |
| company_id | bigint | O | 소속사 FK (tb_artist_company) |
| profile_image_id | bigint | O | 프로필 이미지 FK (tb_common_profile_image_file) |
| site_info | jsonb |  | 멤버 SNS 정보 (JSON) |
| name | character varying |  | 멤버 이름 |
| hash_tag | ARRAY |  | 멤버 해시태그 목록 (Array) |
| information | jsonb |  | 멤버 추가 정보 (다국어, JSON) |
| brand_idx | integer |  | 레거시 브랜드 인덱스 |
| i18n_name | jsonb |  | 멤버 이름 다국어 (JSON) |
| gender_type | integer |  | 멤버 성별 (0:여성, 1:남성, 3:알수없음) |
| birthday | date | O | 멤버 생년월일 |
| index | integer |  | 멤버 정렬 순번 |
| mbti | text |  | 멤버 MBTI |
| nationality | ARRAY |  | 멤버 국적 (ISO 3166-1 alpha-2 코드 리스트) |
| representative_emoji | character varying | O | 멤버 대표 이모지 |

## tb_artist_company — 소속사

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 회사 고유 식별자 (PK) |
| name | character varying |  | 회사명 |
| created_at | timestamp with time zone |  | 회사 등록일시 |
| updated_at | timestamp with time zone |  | 회사 최종 수정일시 |
| company_code | character varying |  | 회사 코드 |
| i18n_name | jsonb |  | 회사명 다국어 (JSON) |
| creator_idx_list | ARRAY |  | 레거시 크리에이터 인덱스 목록 (Array) |
| company_role_list | ARRAY |  | 회사 역할 목록 (제작사, 배급사 등, Array) |

## tb_commerce_order — 결제 원본

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 주문 고유 식별자 (PK) |
| order_number | text |  | 주문번호 |
| order_status | integer |  | 주문 상태 (0:생성~7:취소) |
| shipping_information | jsonb |  | 배송비/배송방법/박스수/재고할당 + 배송지 정보(JSON). 개인정보 포함: information(address/detail_address/zip_code/surname/given_name + additional_info(email/phone/tax_id_number/delivery_name 등)). |
| event_join_information | jsonb |  | 이벤트 응모 정보 (JSON) |
| ordered_data | jsonb |  | 주문 상품/옵션/수량/가격/환율/배송비 등의 주문 스냅샷(JSON). 개인정보 포함 가능: manager{name,email} 등(담당자 정보). |
| payment_data | jsonb |  | 결제 정보(요청/응답, PG/결제수단/금액/영수증 URL 포함). 개인정보 포함 가능: request.customer_info(customerName/customerEmail/customerMobilePhone 등). 보안민감 포함: response.secret/paymentKey/lastTransactionKey 등. |
| cancel_reason_type | integer |  | 취소 사유 타입 |
| cancel_memo | text |  | 취소 메모 |
| canceled_at | timestamp with time zone | O | 취소일시 |
| created_at | timestamp with time zone |  | 생성일시 |
| updated_at | timestamp with time zone |  | 수정일시 |
| user_id | bigint | O | 사용자 FK |
| payment_request_id | text |  | 결제 요청 ID |
| event_pk_list | ARRAY |  | 이벤트 PK 목록 (ARRAY) |
| searching_event_text | text |  | 검색용 이벤트명 텍스트 |
| index | integer |  | 정렬 순서 |
| event_ticket_information | jsonb |  | 응모권 정보 (JSON) |
| cancel_requested_ordered_data | jsonb |  | 취소 요청 주문 데이터 (JSON) |
| refund_at | timestamp with time zone | O | 환불일시 |
| refund_data | jsonb |  | 환불 데이터 (JSON) |
| refund_memo | text |  | 환불 메모 |
| refund_reason_type | integer |  | 환불 사유 타입 |
| refund_status | integer |  | 환불 상태 |
| ip_address | text |  | 주문 IP 주소 |
| ip_address_info_id | bigint | O | IP 주소 정보 FK |
| user_order_number | text |  | 사용자용 주문번호 |
| approved_at | timestamp with time zone | O | 승인일시 |
| shipping_process_started_at | timestamp with time zone | O | 배송처리 시작일시 |
| payment_status | text |  | 결제 상태 (Generated Column) |
| product_event_type | text |  | 상품 이벤트 타입 (Generated Column) |
| shipping_method | text |  | 배송 방법 (Generated Column) |
| recipient_name | text | O | 수령인명 (Generated Column) |
| stock_allocation_type | text | O | 재고 할당 타입 (Generated Column) |
| stock_allocated_at | timestamp with time zone | O | 재고 할당일시 (Generated Column) |
| delivery_requested | boolean |  | 배송 요청 여부 (Generated Column) |
| delivery_requested_at | timestamp with time zone | O | 배송 요청일시 (Generated Column) |

## tb_commerce_product — 상품

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 상품 고유 식별자 (PK) |
| product_code | text |  | 상품 코드 (legacy PD_CD, project idx) |
| title | jsonb |  | 상품명 (다국어 JSON) |
| hash_tag | ARRAY |  | 해시태그 목록 (ARRAY) |
| is_displayed | boolean |  | 노출 여부 |
| is_active | boolean |  | 활성 상태 |
| artist_id | bigint | O | 아티스트 FK |
| company_id | bigint | O | 기획사 FK |
| manager_id | bigint | O | 담당자 FK |
| created_at | timestamp with time zone |  | 생성일시 |
| released_at | timestamp with time zone | O | 발매일시 |

## tb_commerce_product_event_data — 이벤트 상품 데이터

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 상품 이벤트 고유 식별자 (PK) |
| product_id | bigint | O | 상품 FK |
| code | text |  | 이벤트 코드 |
| creator_type | integer |  | 크리에이터 타입 (0:애니, 1:아티스트, 2:팬) |
| description | jsonb |  | 설명 (다국어 JSON) |
| event_info | jsonb |  | 이벤트 정보 (JSON) |
| event_status | integer |  | 판매 상태 (0:작업중~6:품절) |
| funding_info | jsonb |  | 펀딩 정보 (JSON) |
| title | jsonb |  | 이벤트 제목 (다국어 JSON) |
| product_event_type | integer |  | 판매 유형 (0:펀딩, 1:예약판매, 2:쇼핑) |
| is_displayed | boolean |  | 노출 여부 |
| market_type | integer |  | 마켓 노출 타입 (0:전체, 1:B2B전용, 2:일반전용) |
| manager_id | bigint | O | 담당자 FK |
| created_at | timestamp with time zone |  | 생성일시 |
| winning_category_id | bigint | O | 당첨 카테고리 FK |
| purchase_limit_type | integer |  | 수량 제한 타입 (0:없음, 1:수량제한, 2:재고확인) |
| b2b_discount_type | integer |  | B2B 할인 타입 (0:없음, 1:기본, 2:특전) |
| is_contain_poster | boolean |  | 포스터 포함 여부 |
| is_display_stock | boolean |  | 재고 표시 여부 |
| is_refundable | boolean |  | 환불 가능 여부 |
| winner_announcement_status | character varying |  | 당첨자 발표 상태 |

## tb_commerce_product_event_sales_data — 이벤트 상품 판매 데이터

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 이벤트 판매 데이터 고유 식별자 (PK) |
| sales_start_at | timestamp with time zone | O | 판매 시작일시 |
| sales_end_at | timestamp with time zone | O | 판매 종료일시 |
| exchange_rate_correction_rate | double precision |  | 환율 보정률 |
| user_purchase_limit | integer |  | 사용자별 구매 제한 |
| exchange_rate_id | bigint | O | 기준 환율 FK |
| product_event_id | bigint |  | 이벤트 FK |
| option_list | jsonb |  | 옵션 목록 (JSON) |
| bonus_list | jsonb |  | 보너스 목록 (JSON) |
| country_code_list | ARRAY |  | 판매 국가 코드 목록 (ARRAY) |
| sales_country_limits_type | integer |  | 판매 국가 제한 타입 (0:없음, 1:화이트리스트, 2:블랙리스트) |
| free_shipping_info | jsonb |  | 무료배송 정보 (JSON) |
| limit_base_option_item_id | bigint | O | 구매 제한 기준 품목 FK |
| option_item_purchase_limit | integer |  | 품목 구매 제한 수량 |
| sales_channel | character varying |  | 판매 채널 (MAKESTAR/WEIDIAN) |
| has_option_item_purchase_limit | boolean |  | 품목 구매 제한 여부 |
| has_option_purchase_limit | boolean |  | 옵션 구매 제한 여부 |
| has_user_purchase_limit | boolean |  | 사용자별 구매 제한 여부 |

## tb_commerce_order_event_participant — 이벤트 응모 주문

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 주문 이벤트 참가자 고유 식별자 (PK) |
| status | character varying |  | 당첨 상태 (PENDING/WINNER/LOSER/FAKE_WINNER/EXCLUDE) |
| announcing_order | integer | O | 발표시 노출순서 |
| is_exclude_album_quantity | boolean |  | 앨범 수량 제외 여부 |
| warehouse_request_note | text |  | 물류센터 요청사항 |
| created_at | timestamp with time zone |  | 생성일시 |
| updated_at | timestamp with time zone |  | 수정일시 |
| event_id | bigint |  | 이벤트 FK |
| winner_group_id | bigint | O | 당첨자 그룹 FK |
| is_active | boolean |  | 활성 여부 |

## tb_wallet_wallet — 지갑

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 지갑 고유 식별자 (PK) |
| point | integer |  | 보유 포인트 |
| created_at | timestamp with time zone |  | 생성일시 |
| user_id | bigint |  | 사용자 FK (1:1) |
| event_chance_count | integer |  | 이벤트 기회 횟수 |

## tb_wallet_point_earn_log — 포인트 적립 로그

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 포인트 적립 로그 고유 식별자 (PK) |
| earnings_type | integer |  | 적립 타입 (앨범/이벤트 등) |
| point | integer |  | 적립 포인트 |
| used_point | integer |  | 사용된 포인트 |
| remained_point | integer |  | 잔여 포인트 |
| earnings_message | text |  | 적립 메시지 |
| created_at | timestamp with time zone |  | 적립일시 |
| expired_at | timestamp with time zone | O | 만료일시 |
| purchase_id | bigint | O | 구매 FK |
| wallet_id | bigint | O | 지갑 FK |

## tb_wallet_point_spend_log — 포인트 사용 로그

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 포인트 소비 로그 고유 식별자 (PK) |
| spend_type | integer |  | 소비 타입 (만료/투표/아이템 등) |
| used_point | integer |  | 사용 포인트 |
| spend_message | text |  | 소비 메시지 |
| created_at | timestamp with time zone |  | 소비일시 |
| wallet_id | bigint | O | 지갑 FK |

## tb_vote_vote — 투표

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 투표 고유 식별자 (PK) |
| title | text |  | 투표 제목 |
| information | jsonb |  | 투표 정보 (JSON) |
| is_live_result | boolean |  | 실시간 결과 공개 여부 |
| result | jsonb |  | 투표 결과 (JSON) |
| result_at | timestamp with time zone | O | 결과 발표일시 |
| start_at | timestamp with time zone | O | 시작일시 |
| end_at | timestamp with time zone | O | 종료일시 |
| created_at | timestamp with time zone |  | 생성일시 |
| image_id | bigint | O | 투표 이미지 FK |
| index | integer |  | 정렬 순서 |
| program_id | bigint | O | 투표 프로그램 FK |
| guide_image_id | bigint | O | 가이드 이미지 FK |
| daily_vote_limit | integer |  | 일간 투표 제한 (-1:무제한) |
| guide_image_en_id | bigint | O | 영문 가이드 이미지 FK |
| guide_image_dark_id | bigint | O | 다크모드 가이드 이미지 FK |
| guide_image_en_dark_id | bigint | O | 영문 다크모드 가이드 이미지 FK |
| point | integer |  | 투표당 포인트 |
| point_type | integer |  | 포인트 타입 (소비/적립) |
| display_timer | boolean |  | 타이머 표시 여부 |

## tb_vote_vote_log — 투표 로그

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 투표 로그 고유 식별자 (PK) |
| created_at | timestamp with time zone |  | 투표일시 |
| option_id | bigint | O | 선택 옵션 FK |
| ticket_id | bigint |  | 투표 티켓 FK |
| vote_id | bigint | O | 투표 FK |
| ip_address | text |  | IP 주소 |
| ip_description | jsonb |  | IP 정보 (JSON) |
| device_location | text |  | 디바이스 위치 |
| device_location_info | jsonb |  | 디바이스 위치 정보 (JSON) |
| geocoding_info | jsonb |  | 지오코딩 정보 (JSON) |

## tb_vote_vote_ticket — 투표 티켓

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 투표 티켓 고유 식별자 (PK) |
| ticket_status | integer |  | 티켓 상태 |
| is_used | boolean |  | 사용 여부 |
| available_at | timestamp with time zone | O | 사용 가능일시 |
| used_at | timestamp with time zone | O | 사용일시 |
| created_at | timestamp with time zone |  | 생성일시 |
| user_id | bigint |  | 사용자 FK |
| spend_log_id | bigint | O | 포인트 소비 로그 FK |
| earn_log_id | bigint | O | 포인트 적립 로그 FK |
| device_id | text |  | 디바이스 ID |

## tb_streaming_party — 스트리밍 파티

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 스트리밍 파티 고유 식별자 (PK) |
| title | text |  | 파티 제목 |
| index | integer |  | 정렬 순서 |
| translated_description | jsonb |  | 다국어 설명 (JSON) |
| joined_member_ids | ARRAY |  | 참여 멤버 ID 목록 (ARRAY) |
| target_track_spotify_ids | ARRAY |  | 시그니처 트랙 Spotify ID 목록 (ARRAY) |
| all_track_spotify_ids | ARRAY |  | 전체 트랙 Spotify ID 목록 (ARRAY) |
| track_information | jsonb |  | 트랙 정보 (JSON) |
| is_active | boolean |  | 활성화 여부 |
| started_at | timestamp with time zone | O | 파티 시작일시 |
| created_at | timestamp with time zone |  | 생성일시 |
| fandom_id | bigint | O | 팬덤 FK |
| image_id | bigint | O | 파티 이미지 FK |
| ended_at | timestamp with time zone | O | 파티 종료일시 |
| party_time | integer |  | 목표 시간 (분) |
| partyroom_id | text |  | Firestore 파티룸 ID |
| party_type | integer |  | 파티 타입 (공식/사용자) |
| goal_streams | integer |  | 목표 스트리밍 수 |
| updated_count | integer |  | 플레이리스트 재구성 횟수 |
| spotify_playlist_id | text |  | Spotify 플레이리스트 ID |
| target_chart_position | integer |  | 목표 차트 순위 |
| people_count | integer |  | 목표 참여 인원 |
| creator_id | bigint | O | 생성자 팬덤멤버 FK |
| streams | integer |  | 현재 스트리밍 수 |
| track_index | integer |  | 현재 트랙 인덱스 |
| status | integer |  | 파티 상태 (대기/진행/종료) |
| sub_track_spotify_ids | ARRAY |  | 2순위 트랙 Spotify ID 목록 (ARRAY) |
| service_information | jsonb |  | 외부 서비스 정보 (JSON) |
| banned_artist_list | ARRAY | O | 금지 아티스트 목록 (ARRAY) |
| genres | ARRAY | O | 추천곡 장르 목록 (ARRAY) |
| request_params | jsonb |  | 입력 파라미터 (JSON) |

## tb_streaming_fandom — 팬덤

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 팬덤 고유 식별자 (PK) |
| title | text |  | 팬덤명 |
| is_active | boolean |  | 활성화 여부 |
| created_at | timestamp with time zone |  | 생성일시 |
| artist_id | integer | O | 스트리밍 아티스트 FK |
| image_id | bigint | O | 팬덤 대표 이미지 FK |

## tb_streaming_fandom_member — 팬덤 멤버

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 팬덤 멤버 고유 식별자 (PK) |
| level | integer |  | 멤버 등급 (0:일반, 1:관리자 등) |
| nickname | text |  | 닉네임 (고유) |
| introduction | text |  | 소개글 |
| site_info | jsonb |  | SNS 정보 (JSON) |
| created_at | timestamp with time zone |  | 생성일시 |
| fandom_id | bigint |  | 팬덤 FK |
| profile_image_id | bigint | O | 프로필 이미지 FK |
| user_id | bigint |  | 사용자 FK |
| firestore_member_id | text | O | Firestore 멤버 ID |

## tb_notification_fcm_token — FCM 푸시 토큰

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | FCM 토큰 고유 식별자 (PK) |
| app_name | text |  | 앱 이름 (POCAALBUM, VOTE 등) |
| device_id | text |  | 디바이스 고유 ID |
| fcm_token | text |  | FCM 토큰 |
| created_at | timestamp with time zone |  | 생성일시 |
| updated_at | timestamp with time zone |  | 수정일시 |
| user_id | bigint | O | 사용자 FK |
| device_agent | text |  | 디바이스 에이전트 |
| device_type | text |  | 디바이스 타입 (android/ios) |

## tb_notification_notification_agreement — 알림 수신 동의

| 컬럼 | 타입 | Null | 설명 |
|---|---|---|---|
| id | bigint |  | 알림 동의 설정 고유 식별자 (PK) |
| vote | jsonb |  | 투표 앱 알림 설정 (JSON) |
| pocaalbum | jsonb |  | 포카앨범 앱 알림 설정 (JSON) |
| commerce | jsonb |  | 커머스 앱 알림 설정 (JSON) |
| user_id | bigint |  | 사용자 FK |