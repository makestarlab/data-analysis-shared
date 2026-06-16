# Makestar 데이터 분석 공유 컨텍스트

팀 공통 분석 환경. 개별 프로젝트 CLAUDE.md에서 아래처럼 import:
```
@/Users/songakim/Documents/works/analysis-shared/CLAUDE.md
```

---

## BigQuery 연결

- **프로젝트**: `makestar-dw`
- **인증키**: `~/Documents/system/makestar-dw-5132eea235fa.json`
- **Python 환경**: `source ~/bq-analysis/.venv/bin/activate`

```python
from google.cloud import bigquery
client = bigquery.Client.from_service_account_json(
    "/Users/songakim/Documents/system/makestar-dw-5132eea235fa.json",
    project="makestar-dw"
)
```

---

## 주요 데이터셋

| 데이터셋 | 용도 |
|---|---|
| `datamart` | 분석용 집계 테이블. 대부분의 분석 여기서 시작 |
| `pg_mystarroom_public` | 메이크스타 서비스 원본 DB (Postgres CDC) |
| `pg_oms_public` | OMS(주문관리시스템) 원본 |
| `production` | SPM(크라우드펀딩) 원본 |
| `external` | 광고/외부 데이터 |
| `analytics_*` | GA4 원본 이벤트 (앱별 분리) |
| makestar-pay | PG 결제 처리 전용 DB |
| TMS | 배송관리시스템 (송장·배송 추적) |

---

@context/schema/datamart.md
@context/schema/pg_mystarroom.md
@context/schema/pg_oms.md
@context/schema/makestar_pay.md
@context/schema/tms.md
@context/schema/production.md
@context/segments.md
@context/service.md
@queries/patterns.md
