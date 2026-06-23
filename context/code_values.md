# 코드값 정의

BQ에서 실측한 값 목록. 의미 미확정 항목은 별도 표기.

---

## datamart.total_orders

### market_type
| 값 | 건수 | 설명 |
|---|---|---|
| B2C | 1,681,800 | 일반 소비자 직접 구매 |
| B2B | 199,029 | 기업/도매 구매 |
| 앨범버디 | 13,024 | AlbumBuddy 플랫폼 |
| 기타 | 4,628 | |
| 포카앨범제작 | 244 | 포카앨범 제작 매출 |

> GMV 집계 시 `market_type IN ('B2C','B2B')` 필터 사용

### biz_type
| 값 | 건수 |
|---|---|
| 한국(이벤트) | 1,032,628 |
| 중국 | 498,971 |
| B2B | 199,029 |
| 쇼핑 | 97,293 |
| APAC | 30,758 |
| 앨범버디 | 13,024 |
| 일본 | 10,608 |
| 미주유럽 | 7,113 |
| 공동구매 | 4,452 |
| 한국(매장) | 3,951 |
| 기타 | 610 |
| 포카앨범제작 | 244 |
| 앨범유통/도매 | 44 |

### channel_type
| 값 | 건수 |
|---|---|
| 메이크스타웹 | 1,387,988 |
| 위챗미니프로그램 | 314,513 |
| 웨이디엔 | 149,179 |
| 오프라인매장 | 21,276 |
| 앨범버디웹 | 13,024 |
| 스페이스상하이 | 4,485 |
| 스페이스광저우 | 3,706 |
| 큐텐재팬 | 1,759 |
| 스페이스선전 | 1,229 |
| 스페이스도쿄 | 1,111 |
| 외부거래 | 390 |
| 팬클럽 자체 링크 | 48 |
| 대외팝업 | 17 |

### product_type
| 값 | 건수 | 의미 |
|---|---|---|
| 리워드 | 1,084,843 | 메이크스타 이벤트 리워드 |
| 위챗미니 | 314,513 | 위챗 미니프로그램 |
| B | 199,828 | B2B |
| 웨이디엔 | 149,179 | 웨이디엔 |
| N | 97,536 | 쇼핑 B2C |
| 중국 오프라인매장 | 13,744 | 중국 오프라인 |
| 앨범버디 | 13,024 | AlbumBuddy |
| G | 4,524 | 공동구매 |
| 스페이스상하이 | 4,485 | 스페이스 상하이 |
| 메이크스타샵 | 3,951 | 오프라인 메이크스타샵 |
| C | 935 | 중국 커머스(위챗 외) |
| 포카앨범 제작 | 244 | 포카앨범 제작 매출 |
| M | 238 | 쇼핑 (특수 유형) |
| 차액지불 | 132 | 차액지불 |
| 앨범 유통/도매 | 44 | 앨범 유통/도매 |

### data_source
| 값 | 설명 |
|---|---|
| old_commerce_db | 구 커머스 DB |
| new_commerce_db | 신 커머스 DB |
| 위챗미니 | 위챗 미니프로그램 |
| 웨이디엔 | 웨이디엔 |
| albumbuddy.public.order | AlbumBuddy |
| `{지역} \| 데이터 입력` | 오프라인 수기 입력 |

---

## datamart.events_

### event_type
| 값 | 건수 |
|---|---|
| MEET&CALL | 1,744 |
| VIDEOCALL | 1,110 |
| ETC | 706 |
| PHOTOCARD | 562 |
| LUCKYDRAW | 243 |
| FANSIGN | 183 |
| SHOWCASE | 68 |
| SPECIAL EVENT | 59 |
| FANSIGN&PHOTO EVENT | 47 |
| PHOTO EVENT | 32 |
| ONLINE PHOTO&CALL | 20 |
| SPECIAL OFFLINE EVENT | 18 |
| VOICECALL | 6 |
| LISTENING PARTY | 1 |

---

## pg_mystarroom_public

### tb_auth_log.log_type
| 값 | 건수 | 설명 |
|---|---|---|
| 0 | 2,009,794 | 가입 |
| 1 | 2,140,728 | 로그인 |

> NRU 기준은 `tb_auth_log`가 아닌 `tb_auth_user.is_certified = true`

### tb_auth_user.created_from
유저가 어느 서비스에서 가입했는지.

| 값 | 건수 |
|---|---|
| MAKESTAR | 493,639 |
| POCAALBUM | 341,278 |
| VOTE | 2,414 |
| CALENDOL | 1,980 |
| POCADB | 1,820 |
| UNKNOWN | 129 |
| JOGIYO | 96 |
| STREAMWITH | 56 |
| SYSTEM | 9 |
| FANS | 8 |
| KPOPMATE | 1 |

> POCAALBUM 가입자가 34만명으로 MAKESTAR 다음으로 큰 서비스

### tb_auth_user.user_type
현재 모든 유저가 `0`. 의미 미확정.

### tb_commerce_order.order_status (INTEGER)
| 값 | 건수 | 의미 미확정 |
|---|---|---|
| 6 | 298,865 | |
| 999 | 248,927 | |
| 9 | 30,931 | |
| 3 | 28,816 | |
| 4 | 15,886 | |
| 5 | 3,732 | |
| 997 | 836 | |
| 11 | 125 | |
| 7 | 97 | |

> 정확한 코드 의미 확인 필요

### tb_commerce_order.payment_status
| 값 | 건수 |
|---|---|
| CONFIRMED | 276,324 |
| FAILED | 245,084 |
| CANCELED | 26,383 |
| PARTIAL_CANCELED | 3,921 |
| PENDING | 503 |
| CANCEL_FAILED | 110 |
| WAITING_FOR_DEPOSIT | 2 |

### tb_commerce_order.payment_method
| 값 | 건수 |
|---|---|
| CARD | 153,657 |
| NAVERPAY | 40,164 |
| DIRECT | 26,124 |
| TOSSPAY | 25,644 |
| PAYPAL | 25,202 |
| EASY_PAY_UNKNOWN | 25,191 |
| VIRTUAL_ACCOUNT | 24,376 |
| KAKAOPAY | 16,387 |
| TRANSFER | 14,568 |
| ALIPAY | 9,362 |
| PAYCO | 6,218 |
| MOBILE_PHONE | 3,290 |
| DEPOSIT | 3,261 |
| WECHATPAY | 3,124 |
| ALIPAYHK | 1,281 |
| TOUCHNGO | 847 |
| DANA | 552 |
| PAYPAY | 402 |
| RABBIT_LINE_PAY | 248 |
| TRUEMONEY | 176 |
| GCASH | 130 |
| APPLEPAY | 116 |

### tb_commerce_order.product_event_type
| 값 | 건수 | 의미 미확정 |
|---|---|---|
| 1 | 454,194 | |
| 2 | 97,242 | |
| 0 | 892 | |

---

## pg_oms_public

### oms_order_line_item_sku.product_type (실측)
채널 구분의 핵심. `order_no` 접두사와 함께 사용해야 B2C/B2B 구분 가능.

| 값 | order_no 접두사 | 실제 채널 | 주의 |
|---|---|---|---|
| `NCM_EVENT` | `E-` | 이벤트 주문 | |
| `NCM_SHOPPING` | `B-` (70%), `C-` (30%) | B2B + B2C 혼재 | B2B 구분 필요 |
| `SHOPPING` | `B`, `S` | B2B + 쇼핑 구형 | total_orders 조인 시 B2B로 매핑됨 |
| `NCM_FUNDING` | `C-` | 크라우드펀딩 | |

> **B2C 쇼핑만 필터**: `product_type IN ('NCM_SHOPPING') AND order_no LIKE 'C-%'`
> **이벤트만 필터**: `order_no LIKE 'E-%'`
> OMS order_no(E-xxx, B-xxx)와 커머스 order_no(C25xxx)는 **별개 체계 — JOIN 불가**

### oms_order_line_item_sku.order_no 접두사 (실측)

| 접두사 | 채널 |
|---|---|
| `E-` | 이벤트 주문 |
| `B-` | B2B 도매 주문 (NCM_SHOPPING에 혼재) |
| `C-` | 쇼핑 B2C 주문 |
| `S` | 쇼핑 구형 |

### oms_order.order_status
| 값 | 건수 |
|---|---|
| COMPLETE | 318,330 |
| CANCEL | 30,619 |
| FAIL | 6 |
| PARTIAL_CANCEL | 2 |

### oms_order.order_source
| 값 | 건수 |
|---|---|
| MAKESTAR | 348,956 |
| WEIDIAN | 1 |

### oms_stock_item_quantity_adjustment.code — 재고 조정 코드
| 값 | 코드명 |
|---|---|
| 10 | 정상입고 |
| 11 | 기타입고 |
| 19 | 입고취소 |
| 20 | 재고할당 |
| 29 | 재고할당취소 |
| 30 | 정상출고 |
| 31 | 기타출고 |
| 40 | 보류등록 |
| 44 | 보류불량화 |
| 45 | 불량보류화 |
| 49 | 보류취소 |
| 50 | 폐기예정 |
| 59 | 폐기예정취소 |
| 60 | 임의재고조정 |

> code=30(정상출고) 시 `message` 앞 8자에서 출고 유형 판별:
> `C` = 쇼핑, `B` = B2B, `E` = 이벤트, `S` = 쇼핑

### mst_sku.sku_type
| 값 | 의미 |
|---|---|
| P | 부모 SKU (랜덤 포토카드 등 상위 단위) |
| C | 자식 SKU (실제 개별 카드) |

> `child_sku_count_in_use = 0`인 SKU가 실제 재고 집계 대상(leaf SKU)

### total_orders.order_no 접두사 (실측)
`total_orders.order_no` 첫 글자로 채널 구분 가능. B2C/B2B 필터에 활용.

| 접두사 | market_type | biz_type | 설명 |
|---|---|---|---|
| `C` | B2C | 이벤트/쇼핑/해외 | B2C 커머스 주문 (주력) |
| `P` | B2C | 이벤트/중국/해외 | B2C 구형 또는 특정 채널 |
| `B` | B2B + B2C 혼재 | B2B/이벤트/기타 | B2B 주력, B2C 소수 혼재 |
| `S` | B2C | 쇼핑/일본 | B2C 쇼핑 구형 |
| `M` | B2C | 중국/쇼핑 | 위챗 계열 |
| `E` | B2B | B2B | B2B 이벤트 |
| `8`, `9`, `1` | B2C | 중국/일본 | 오프라인/외부 채널 |

```sql
-- B2C 쇼핑 필터 (order_no 기준)
WHERE order_no LIKE 'C%' OR order_no LIKE 'S%'
-- B접두사는 B2B 주력이나 B2C 소수 혼재 → market_type 이중 확인 권장
```

### tb_commerce_order.user_order_number 접두사
주문 유형을 구분하는 핵심 규칙. 다수의 쿼리에서 사용.

| 접두사 | 주문 유형 |
|---|---|
| `B` | B2B |
| `C` | 쇼핑(커머스) |
| `E` | 이벤트 |

---

## datamart.lead_time

### 주문유형
`tb_commerce_order.user_order_number` 접두사 + 특전(POB) 포함 여부 조합.

| 값 |
|---|
| B2B 특전&일반 |
| B2B 특전 |
| B2B 일반 |
| 쇼핑 특전&일반 |
| 쇼핑 특전 |
| 쇼핑 일반 |

> 특전(POB) 여부: `total_orders.event_id IS NOT NULL`

### 비고
| 값 | 의미 |
|---|---|
| NULL | 정상 주문 |
| 재고할당 실패로 홀딩 | `external.release_holding_orders`에 등록된 주문 |

### 기준일시 계산 규칙
`greatest(결제일시, 발매일시)` 기준으로 영업시간 보정:
- 금요일 17시 이후 → 다음 월요일 08:00
- 토요일 → 다음 월요일 08:00
- 일요일 → 다음 월요일 08:00
- 월~목 17시 이후 → 다음날 08:00
- 월요일 00:00~08:00 → 당일 08:00
