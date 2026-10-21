# GS1 India — Customer Intelligence Challenge

**Snapshot:** 2026-10-20. **Grain:** GCP; company-level outreach ranking. All data synthetic but confidential. Raw CSVs are intentionally excluded from Git.

## Run from a clean checkout (Windows PowerShell)
```powershell
python -m pip install -r requirements.txt
# Copy private gtin_activity.csv and subscriptions.csv into data/ (never commit them)
python src/analyze.py --data-dir data --output-dir outputs
python -m pytest -q
```
The single `analyze.py` command rebuilds the core KPI, score and company-priority aggregate outputs from both raw files. It runs locally, so Snowflake credentials are not required. The source data was also ingested and explored in Snowflake; see the analytical methods in `reports/`. This is a local reproducibility path, **not** an automated Snowflake refresh or a complete replacement for the dashboard export pipeline.

## Reproduced metrics
See `outputs/run_log.txt` and `outputs/metrics.json` from the verification run (generated outputs are ignored by Git). 37,477 model GCPs; 37,410 scored; 67 require review; 26,718 matched GCPs quiet/dormant/zero GTIN; 14 show post-expiry activity relative to recorded expiry.

## Deliverables
- `reports/CEO_Memo.pdf` — one-page CEO brief
- `reports/Data_Quality_Report.md` — row-level decision log and caveats
- `reports/Headroom_Limitations.md` — what is unmeasurable and required extra fields
- `reports/Findings_and_Score.md` — business findings, scoring method and checks
- `reports/Submission_Checklist.md` — final steps, hours and AI disclosure
- `src/analyze.py` and `tests/` — runnable reproducibility pipeline

## Public dashboard
Use the separately prepared aggregate-only Streamlit app. Do not deploy any GCP/company-level files, raw CSVs or Snowflake credentials. Dashboard URL: **ADD AFTER DEPLOYMENT**.

## Assumptions and limitations
Dates day-first for subscriptions; UTC calendar day for GTIN activity; fixed as-of 2026-10-20. Duplicated/sentinel GCPs quarantined. A missing activity record is not proof of no activity. Post-expiry evidence is not proof of unauthorized access. True headroom, churn, monetary value and renewal outcomes cannot be derived from the two extracts alone.

## Time and AI usage
Complete the actual hours and verification statement in `reports/Submission_Checklist.md` before submitting.
