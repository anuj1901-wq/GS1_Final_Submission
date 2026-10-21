# GS1 India — Findings, assumptions and customer score

## Executive summary
The extracts reveal a substantial absence of recent GTIN creation, but not proof that customers derive no subscription value. A small set of GCPs shows post-expiry GTIN creation relative to the recorded expiry. Commercial action should start with a segmented outreach pilot and an audit of expiry anomalies.

## Findings (snapshot 2026-10-20)
1. **Engagement:** 26,718 of 37,419 validated matched GCPs (71.4%) are quiet (4,250), dormant (18,190), or have zero recorded GTINs (4,278). Confidence high for observed GTIN creation recency, low for conclusions about customer value. Decision: segmented onboarding and renewal outreach, not blanket churn classification.
2. **Post-expiry:** 14 of 1,133 expired GCPs (1.24%) have a last GTIN creation date after recorded expiry. Confidence medium for temporal comparison, low for unauthorized-access interpretation. Decision: reconcile these 14 against renewal history and access logs.
3. **Plan usage:** Basic median 25, Premium 42, Trace 23 GTINs; P90 respectively 339, 614 and 458.4. Confidence high for volume distribution, low for upgrade entitlement. Decision: request plan limits and prices before making upgrade claims.

## Additional lenses
- **Adoption:** 2023 cohort 30-day adoption 53.32%, 2025 78.08%, 2026 79.23% in the Snowflake cohort query. Chronology anomalies and cohort eligibility must be stated; trend is descriptive, not causal.
- **Headroom:** Cannot quantify capacity without verified allocation limits. See Headroom_Limitations.md.
- **Original lens — activation versus later engagement:** Compare 30-day activators against slower activators using tenure-matched cohorts and current GTIN recency. This can show association but cannot prove activation causes renewal. The available extracts lack actual renewal outcomes.

## Customer scoring design
Score each eligible GCP from 0 to 100: expiry urgency (40), engagement recency (30), activation (20), cumulative usage (10). Segments: 75-100 Critical; 50-74 High; 25-49 Medium; 0-24 Low. Non-scoreable records are 'Review required'. At company level use maximum eligible GCP score so an urgent GCP is not hidden by averaging, and separately flag any unresolved GCPs. 37,410 GCPs scored; 67 need review. Company priority counts: Critical 1,242; High 7,583; Medium 15,465; Low 10,389; Review 57.

## Validation and limitations
Score is a **transparent outreach priority heuristic**, not a churn probability. Removing the 10-point usage component changes 1,087 / 37,410 (2.9%) high-priority classifications. The model uses no renewal outcomes and has not been prospectively validated. Date anomalies are treated neutrally for activation rather than presumed healthy. Recalibrate weights with actual renewal outcomes, customer feedback and sales capacity.

## Recommendation and value/risk
Commercial owner: Head of Commercial, with Product and Data. Pilot targeted outreach for never-activated/quiet GCPs with upcoming expiry, while separately auditing 14 post-expiry cases. Measure contacted-to-renewed conversion versus a comparable holdout group. Financial value cannot be defensibly monetized without fee/renewal history; risk is misallocating retention effort or treating historic barcode use as illicit access.
