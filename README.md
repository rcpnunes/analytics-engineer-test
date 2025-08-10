# Analytics Engineer Test

This repo contains solution for Pismo's Analytics Engineer technical challenge, including a complete ETL pipeline, data quality checks, and Power BI dashboard.

## Structure
- `src/` → main scripts (ETL)
- `sql/` → scripts SQL (DDL e queries)
- `tests/` → automated tests
- `data/` → local files (SQLite, CSVs) - Git ignored

## How to run
1. Clone repo
2. Create `.env` like `.env.example` with your credentials
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
