# Data quality and reproducibility report
**GS1 India | Snapshot: 20 October 2026 | Source: two synthetic CSV extracts**

## Scope and grain
GTIN activity: 37,466 rows, 37,424 distinct GCP values. Subscriptions: 37,483 rows, 37,480 distinct GCP values. One row is *intended* per GCP, but this assumption is violated. GCP is the primary analysis grain; company_id is used to consolidate multiple GCPs at company level.

## Decision log
| Observation | Records affected | Decision | Consequence |
|---|---:|---|---|
| GCP `0` reused | 40 GTIN rows / 40 company IDs | Exclude from valid GCP model; preserve raw data | Avoids 40 false matches to a sentinel identifier |
| Nonzero duplicated GCP | 3 distinct GCPs, 6 activity rows and 6 subscription rows | Quarantine all three until identity/expiry verified | Excludes 3 GCPs; prevents many-to-many join and misleading expiry classification |
| Subscription-only GCP | 57 GCPs | Retain, label unmatched | Missing activity extract does not prove zero GTIN creation |
| Activity-only GCP | 1 raw distinct GCP (`0`) | Exclude sentinel | No valid activity-only GCP remains |
| Cross-file company ID mismatch | 1 matched GCP | Flag and exclude from risk scoring | Does not inflate certainty about company ownership |
| Registration date missing or unparsable | 2 rows | Preserve NULL, exclude from adoption-duration comparisons | Avoids fabricated registration dates |
| Expiry date missing or unparsable | 6 rows | Preserve NULL; expiry status unknown | Excludes from expiry-sensitive calculations |
| End before start | 3 subscription rows | Flag; do not repair without evidence | Excludes from expiry-sensitive calculations and scoring |
| Pre-registration first GTIN | 1,722 model GCPs in Snowflake adoption anomaly segment | Flag as historical/data chronology anomaly; no valid activation duration | Cohort comparisons require caution |
| Missing first/last GTIN timestamps | Several thousand | Distinguish no recorded activity from missing activity extract | Cannot infer all GTIN events from first/last dates |

## Date handling
Subscription dates interpreted as `DD-MM-YYYY`, then `DD/MM/YYYY`, then `YYYY-MM-DD`. Slash-format interpretation is an explicit assumption; ambiguous values should be checked with the exporting team. GTIN timestamps are parsed with timezone awareness and compared using UTC calendar dates in the Python pipeline. Date and score snapshots use 2026-10-20. Source placeholders `NULL`, `NULQ`, `nan`, and blanks are treated as missing.

## Population reconciliation
37,477 valid model GCPs = 37,420 matched + 57 subscription-only. 34,736 distinct company IDs. 37,410 GCPs scoreable, 67 require review. The validated matched engagement population is 37,419 after removing one company ID mismatch.

## Caveats
A missing GTIN activity row is not proof of never using a GCP. Cumulative GTIN counts are not monthly activity. Last GTIN date after a recorded expiry is evidence of a post-expiry creation event relative to that expiry, but renewals and platform access rights are not available. A historical GTIN can continue to be used commercially without new platform activity. Multiple GCPs per company require company-level aggregation for customer counts.

## Audit and verification
Run `python src/analyze.py --data-dir data --output-dir outputs` from the repository root. `outputs/metrics.json` captures the reproducible numbers. `pytest -q` checks date parsing. No raw or company-level data is committed. Reconcile against Snowflake exported aggregates and investigate differences before reporting.
