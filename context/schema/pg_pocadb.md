# pg_pocadb_public 스키마

_PocaDB 서비스 원본 DB. 포토카드 데이터베이스·컬렉션 관리._

---

## poca — 포토카드

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK |
| album_id | INTEGER | FK to album.id |
| artist_id | INTEGER | FK to artist.id |
| artist_member_id | INTEGER | FK to artist_member.id |
| title | STRING | 포카 제목 |
| name | JSON | 포카명 다국어 |
| category | STRING | 포카 카테고리 |
| image_id | STRING | 이미지 ID |
| tag_id | INTEGER | 태그 ID |
| version | JSON | 버전 정보 |
| seq | INTEGER | 정렬 순서 |
| visibility | BOOLEAN | 공개 여부 |
| missing_poca | BOOLEAN | 미등록 포카 여부 |
| contributor | STRING | 기여자 |
| created_at | TIMESTAMP | 생성일 |
| deleted_at | TIMESTAMP | 삭제일 |

## album — 앨범

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK |
| artist_id | INTEGER | FK to artist.id |
| title | STRING | 앨범 제목 |
| name | JSON | 앨범명 다국어 |
| description | STRING | 앨범 설명 |
| image_id | STRING | 커버 이미지 |
| published_at | DATE | 발매일 |
| visibility | BOOLEAN | 공개 여부 |
| data | JSON | 추가 메타데이터 |

## artist — 아티스트

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK |
| title | STRING | 아티스트명 |
| name | JSON | 다국어 아티스트명 |
| image_id | STRING | 프로필 이미지 |
| visibility | BOOLEAN | 공개 여부 |
| ready | BOOLEAN | 서비스 준비 여부 |

## artist_member — 아티스트 멤버

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK |
| artist_id | INTEGER | FK to artist.id |
| title | STRING | 멤버명 |
| name | JSON | 다국어 멤버명 |
| image_id | STRING | 프로필 이미지 |
| order_in_group | INTEGER | 그룹 내 순서 |
| visibility | BOOLEAN | 공개 여부 |

## my_poca — 유저 포토카드 컬렉션

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK |
| user_id | INTEGER | FK to user_profile.id |
| card_id | INTEGER | FK to poca.id |
| own | BOOLEAN | 보유 여부 (false=위시리스트) |
| quantity | INTEGER | 보유 수량 |
| created_at | TIMESTAMP | 등록일 |

## user_profile — 유저

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK (pg_mystarroom_public.tb_auth_user.id와 별도 체계) |
| nickname | STRING | 닉네임 |
| data | JSON | 추가 프로필 정보 |
| deleted_at | TIMESTAMP | 탈퇴일 |

## user_log — 유저 행동 로그

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER | PK |
| user_id | INTEGER | FK to user_profile.id |
| event_name | STRING | 이벤트명 |
| event_params | JSON | 이벤트 파라미터 |
| created_at | TIMESTAMP | 발생일시 |

## poca_wishlist — 위시리스트

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | STRING | PK |
| user_id | INTEGER | FK to user_profile.id |
| artist_id | INTEGER | 아티스트 ID |
| member_id | INTEGER | 멤버 ID |
| member_ids | JSON | 멤버 ID 목록 |
| visits | INTEGER | 방문 수 |
| open | BOOLEAN | 공개 여부 |
