# Headroom and plan-fit analysis: what can and cannot be claimed

## What the extracts establish
The data contains GCP, plan, cumulative GTIN count and first/last creation timestamps. Validated matched population: Basic 32,911 GCPs (median 25 GTINs; 90th percentile 339), Premium 4,253 (median 42; 90th percentile 614), Trace 255 (median 23; 90th percentile approximately 458.4). These are usage distributions, **not capacity utilization**.

## Why true headroom cannot be calculated
No source provides the licensed GCP prefix length/capacity mapping, plan-specific entitlement, historical GTIN allocations, whether GTINs can be retired/reused, or permitted allocation rules for each record. GCP values have different lengths and cannot be assigned a universal capacity based solely on plan name. It would be unsound to label a customer '90% full' or forecast exhaustion from total_gtins alone.

## What to request
1. Authoritative GCP allocation/capacity for each GCP (or rules and prefix lengths sufficient to derive it).
2. Plan catalog, entitlements and commercial price history.
3. GTIN allocation ledger with event dates, retirements and transfers, including renewal history.
4. Current active product catalogue and actual usage patterns.

## Once capacity is available
For each verified GCP: `used_allocations / allowed_allocations` (with treatment of retired/reused codes explicitly documented); `remaining = allowed - used`. Group into <=50%, >50-80%, >80-95%, >95% utilization and separately flag invalid or unknown capacity. Combine with allocation velocity from the GTIN event ledger to estimate time-to-exhaustion, with uncertainty intervals. Validate capacity against GS1 authoritative rules.

## Decision possible today
Create a **headroom verification queue**, not an 'upgrade now' list. Prioritize the upper tail of cumulative GTIN counts for entitlement lookup and sales consultation. Do not estimate incremental revenue without verified price and capacity data.
