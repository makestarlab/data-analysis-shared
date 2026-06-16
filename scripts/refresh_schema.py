"""
BigQuery에서 스키마를 읽어 context/schema/ 파일들을 자동 갱신.

사용법:
  source ~/bq-analysis/.venv/bin/activate
  python3 scripts/refresh_schema.py
"""

from google.cloud import bigquery
from pathlib import Path
import sys

KEY_PATH = "/Users/songakim/Documents/system/makestar-dw-5132eea235fa.json"
PROJECT_ID = "makestar-dw"
SCHEMA_DIR = Path(__file__).parent.parent / "context" / "schema"

# 갱신할 테이블 목록: (dataset, table, 설명)
TABLES = {
    "datamart": [
        ("total_orders",             "GMV/결제 집계 기준"),
        ("events_",                  "이벤트 메타 (권장)"),
        ("events",                   "이벤트 메타 (구버전, artist_id=INTEGER)"),
        ("customer_analysis_visit",  "GA 기반 방문자 (MAU)"),
        ("dau",                      "일별 DAU"),
        ("wau",                      "주별 WAU"),
        ("vw_master_order",          "주문 마스터 뷰"),
        ("vw_master_user",           "유저 마스터 뷰"),
    ],
    "pg_mystarroom_public": [
        ("tb_auth_log",              "로그인/가입 로그 (NRU: log_type=0)"),
        ("tb_commerce_order",        "결제 원본"),
        ("tb_auth_user",             "유저 계정"),
        ("tb_auth_user_information", "유저 프로필"),
        ("tb_artist_artist",         "아티스트"),
    ],
    "production": [
        ("project", "SPM 프로젝트(이벤트) 원본"),
        ("user",    "구 유저 테이블"),
    ],
}

def fetch_schema(client, dataset, table):
    try:
        t = client.get_table(f"{PROJECT_ID}.{dataset}.{table}")
        rows = []
        for f in t.schema:
            desc = f.description or ""
            mode = f" [{f.mode}]" if f.mode != "NULLABLE" else ""
            if f.field_type == "RECORD":
                rows.append(f"| {f.name} | RECORD{mode} | {desc} |")
            else:
                rows.append(f"| {f.name} | {f.field_type}{mode} | {desc} |")
        return t.description, rows
    except Exception as e:
        return None, [f"ERROR: {e}"]

def build_dataset_md(client, dataset, tables):
    lines = [f"# {dataset} 스키마\n", "_자동 생성 — `scripts/refresh_schema.py` 실행으로 갱신_\n"]
    for table, table_desc in tables:
        bq_desc, rows = fetch_schema(client, dataset, table)
        lines.append(f"\n## {table} — {table_desc}")
        if bq_desc:
            lines.append(f"\n{bq_desc}\n")
        lines.append("\n| 컬럼 | 타입 | 설명 |")
        lines.append("|---|---|---|")
        lines.extend(rows)
    return "\n".join(lines) + "\n"

def main():
    client = bigquery.Client.from_service_account_json(KEY_PATH, project=PROJECT_ID)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)

    for dataset, tables in TABLES.items():
        out_file = SCHEMA_DIR / f"{dataset.replace('_public', '')}.md"
        print(f"→ {out_file.name} 갱신 중...")
        content = build_dataset_md(client, dataset, tables)
        out_file.write_text(content, encoding="utf-8")
        print(f"  완료 ({len(tables)}개 테이블)")

    print("\n스키마 갱신 완료.")

if __name__ == "__main__":
    main()
