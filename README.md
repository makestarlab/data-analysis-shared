# Makestar 데이터 분석 공유 프레임워크

Makestar 데이터 분석에 필요한 **스키마, 도메인 지식, 코드값, SQL 패턴**을 팀 공통으로 관리하는 레포.

Claude Code(claude.ai/code)와 함께 사용하면 매번 테이블 구조나 비즈니스 로직을 설명하지 않아도 된다.

---

## 빠른 시작

### 1. 레포 클론

```bash
git clone https://github.com/makestarlab/data-analysis-shared.git ~/Documents/works/analysis-shared
```

### 2. Claude Code 전역 설정

`~/.claude/CLAUDE.md` 파일에 아래 한 줄을 추가한다. 파일이 없으면 새로 만든다.

```bash
echo "@$(echo ~)/Documents/works/analysis-shared/CLAUDE.md" >> ~/.claude/CLAUDE.md
```

또는 직접 `~/.claude/CLAUDE.md`를 열어 맨 위에 추가:

```
@/Users/{본인_계정명}/Documents/works/analysis-shared/CLAUDE.md
```

설정 후 모든 프로젝트에서 Claude Code를 열면 이 레포의 컨텍스트가 자동으로 적용된다.

### 3. 확인

Claude Code를 열고 질문해본다:

```
total_orders에서 GMV 집계할 때 어떤 필터 써야 해?
구매대행 유저 제외하는 쿼리 보여줘
event_order가 뭐야?
```

---

## 레포 구조

```
analysis-shared/
├── CLAUDE.md                     # Claude Code 진입점 (여기서 모든 파일 import)
│
├── context/
│   ├── service.md                # 핵심 도메인 지식
│   │                             # 유저 생애주기, 이탈 정의, 구매 라운드,
│   │                             # 구매대행, POB 특전, 풀세트 패턴 등
│   ├── code_values.md            # 코드값 정의
│   │                             # market_type, biz_type, order_status,
│   │                             # payment_method, 재고조정코드 등
│   ├── data_lineage.md           # total_orders 파이프라인 전체 흐름
│   │
│   └── schema/
│       ├── datamart.md           # 분석용 집계 테이블 스키마
│       │                         # total_orders, events_, vw_commerce_items_v2 등
│       ├── pg_mystarroom.md      # 메이크스타 서비스 원본 DB
│       ├── pg_oms.md             # OMS(주문관리시스템)
│       ├── pg_pocadb.md          # PocaDB 포토카드 DB
│       ├── makestar_pay.md       # PG 결제 처리 DB
│       ├── tms.md                # 배송관리시스템
│       └── production.md        # SPM 크라우드펀딩 원본
│
├── queries/
│   └── patterns.md               # 공통 SQL 패턴
│                                 # GMV, MAU, NRU, 이탈, 구매대행 탐지 등
│
└── scripts/
    └── refresh_schema.py         # BQ 스키마 자동 갱신 스크립트
```

---

## BQ 연결 설정 (개인별)

이 레포는 도메인 지식만 담고 있다. BQ 접속은 각자 설정한다.

```python
from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(
    "/path/to/your/service-account-key.json",
    project="makestar-dw"
)
```

서비스 계정 키는 개인별로 발급받아 사용한다.

---

## 업데이트 방법

### 내용 추가/수정

관련 파일을 직접 수정하고 PR 또는 main에 push.

| 추가할 내용 | 파일 |
|---|---|
| 새 테이블 스키마 | `context/schema/{데이터셋}.md` |
| 비즈니스 로직, 도메인 지식 | `context/service.md` |
| 코드값(status, type 등) | `context/code_values.md` |
| 자주 쓰는 SQL 패턴 | `queries/patterns.md` |
| 데이터 파이프라인 구조 | `context/data_lineage.md` |

### BQ 스키마 자동 갱신

`datamart.*`, `production.*` 테이블은 스크립트로 갱신 가능:

```bash
# scripts/refresh_schema.py의 KEY_PATH를 본인 키 경로로 변경 후 실행
python3 scripts/refresh_schema.py
```

`pg_mystarroom`, `pg_oms`, `makestar_pay`, `tms`는 Excel(`Makestar DB schema.xlsx`) 기반 수동 관리.

### 최신 내용 받기

```bash
git pull
```

---

## 주요 내용 요약

- **유저 ID**: `total_orders.user_id` (STRING) = `CAST(tb_auth_user.id AS STRING)`
- **GMV 기준**: `market_type IN ('B2C','B2B')`, 타임존 `Asia/Seoul`
- **NRU 기준**: `tb_auth_user.is_certified = true`
- **이탈 정의**: 단순 미구매 기간이 아닌 "후속 이벤트 오픈 후에도 미구매"
- **구매대행**: KPI 집계는 포함, B2C 유저 행동 분석 시 제외
- **구매 라운드**: `album_name` 1개 = 1라운드
- **포카 종류 수**: `mst_sku.virtual_child_sku_count`
