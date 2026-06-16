# total_orders 데이터 파이프라인

`datamart.total_orders` 생성 전체 흐름.

---

## 파이프라인 구조

```
[원본 소스들]
    ↓
pre_commerce_orders      ← new_commerce_db 주문 (confirmed + waiting 혼재)
    ↓
pre_total_orders         ← confirmed 주문만 + 외부 소스 합산
    ↓
total_orders             ← market_type != '제외' 필터
```

```
pre_commerce_orders      ← payment_status NOT IN (CONFIRMED, PARTIAL_CANCELED)
    ↓
pre_total_orders_waiting
    ↓
total_orders_waiting     ← 결제 진행 중/미확정 주문
```

---

## 소스별 흐름

| 소스 | 원본 테이블 | data_source 값 |
|---|---|---|
| 메이크스타 커머스 | `vw_commerce_orders` + `vw_commerce_order_items` | `new_commerce_db` |
| 위챗/웨이디엔 | `vw_weidian_orders` | `웨이디엔` |
| 오프라인 매장 | `offline_orders_makestarshop` 외 | `{지역} \| 데이터 입력` |
| AlbumBuddy | `albumbuddy_internal` 제외 후 집계 | `albumbuddy.public.order` |
| 포카앨범 제작 | `pocaalbum_orders` | `포카앨범 제작매출 \| 데이터 입력` |
| 앨범 유통/도매 | `album_extra_orders` | `앨범 유통/도매 매출 \| 데이터 입력` |
| B2C 기타 | `extra_orders` | `B2C 기타 매출 \| 데이터 입력` |
| 아카이브 | `archived_orders` | (기존 값 유지) |

---

## market_type / biz_type / channel_type 결정 로직

`product_type` × `product_category` 조합으로 자동 분류.
예외 케이스는 아래 두 테이블로 오버라이드:

- `order_biz_mapper_objects` — 상품/이벤트/주문번호 단위 오버라이드
- `order_biz_mapper_users` — 유저 단위 오버라이드

`market_type = '제외'` 인 행은 `total_orders`에서 제외됨.

---

## 핵심 조인 관계

```sql
-- 커머스 상품 정보 연결
vw_commerce_order_items.product_id → vw_commerce_items_v2.product_id  (artist_name)
vw_commerce_order_items.product_event_id + product_option_id
    → vw_product_option_info  (sales_qty = 앨범 수량)
    → vw_commerce_items_v2    (sku_code, event_id)

-- 쇼핑 상품의 event_id 추출
vw_commerce_items.sku_name_component_1  → production.project.id 또는
                                         tb_commerce_product_event_data (product_event_type=1)
```

---

## events_ 의 역할

`datamart.events_`는 `total_orders` 파이프라인에 포함되지 않음.

`total_orders.event_id`는 소스에서 직접 저장되며, 분석 시점에 `events_`와 조인해서 메타 정보를 보강하는 **룩업 테이블**로 사용:

```sql
-- 분석 시 이벤트 메타 조인 패턴
SELECT t.*, e.artist_id, e.event_type, e.sales_start_at
FROM `makestar-dw.datamart.total_orders` t
LEFT JOIN `makestar-dw.datamart.events_` e ON t.event_id = e.event_id
```

---

## vw_commerce_orders 주요 상태값

### order_status (커머스 주문 상태)
| 값 | 의미 |
|---|---|
| PAYMENT_PROCESSING | 결제 진행 중 |
| PAYMENT_COMPLETED | 결제 완료 |
| INVENTORY_CHECKING | 재고 확인 중 |
| SHIPPING_PROCESSING | 배송 준비 중 |
| COMPLETED | 배송 완료 |
| CANCELED | 취소 |

> `total_orders`에 포함되는 상태: PAYMENT_PROCESSING ~ COMPLETED (CANCELED 제외)

### order_type
| 값 | 의미 |
|---|---|
| B2C | 일반 소비자 |
| B2B | 기업/도매 |
| ETC | 차액지불 등 기타 |

---

## vw_weidian_orders 상태값

### order_status
| 값 | 의미 |
|---|---|
| 20 | 결제 완료 (배송 전) |
| 30 | 배송 중 |
| 50 | 배송 완료 |
| 60 | 환불 완료 (집계 제외) |

### refund_status
| 값 | 의미 |
|---|---|
| 0 | 환불 없음 |
| 1 | 환불 신청 (환불액 0으로 간주) |
| 2 | 부분 환불 |
| 3 | 환불 실패/거절 (환불액 0으로 간주) |

---

## tb_commerce_product_event_data.product_event_type
| 값 | 의미 |
|---|---|
| 1 | 이벤트 (POB 특전 상품) |

> `vw_commerce_order_items.product_event_type` 문자열 버전:
> `이벤트` = 이벤트 리워드, `펀딩` = SPM 펀딩, `쇼핑` = 일반 쇼핑
