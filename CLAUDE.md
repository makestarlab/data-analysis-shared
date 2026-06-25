# Makestar 데이터 분석 공유 컨텍스트

Makestar 데이터 분석을 위한 공유 프레임워크. 스키마, 도메인 지식, 코드값, SQL 패턴을 담고 있다.

- **BQ 프로젝트**: `makestar-dw`

---

## 주요 데이터셋

| 데이터셋 | 용도 |
|---|---|
| `datamart` | 분석용 집계 테이블. 대부분의 분석 여기서 시작 |
| `pg_mystarroom_public` | 메이크스타 서비스 원본 DB (Postgres CDC) |
| `pg_oms_public` | OMS(주문관리시스템) 원본 |
| `pg_pocadb_public` | PocaDB 포토카드 DB |
| `production` | SPM(크라우드펀딩) 원본 |
| `external` | 광고/외부 데이터 |
| `analytics_*` | GA4 원본 이벤트 (앱별 분리) |
| makestar-pay | PG 결제 처리 전용 DB |
| TMS | 배송관리시스템 (송장·배송 추적) |

---

@context/schema/datamart.md
@context/schema/pg_mystarroom.md
@context/schema/pg_oms.md
@context/schema/pg_pocadb.md
@context/schema/makestar_pay.md
@context/schema/tms.md
@context/schema/production.md
@context/service.md
@context/code_values.md
@context/data_lineage.md
@context/data_model.md
@context/kpi.md
@context/kpi_tree.md
@queries/patterns.md
@queries/kpi_metrics.md
