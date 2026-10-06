# Known Incidents

## INC-014 — Stale market price used by equity valuation

### Symptoms
- Equity valuation completes but shows an unexpectedly large variation.
- Logs contain a market-data timestamp mismatch.
- A fallback price may be applied.
- The business variation control can exceed its threshold.

### Typical cause
The upstream market-data feed has returned a price whose date does not match the valuation date. If fallback behaviour is enabled, the engine can complete using the stale price.

### Recommended investigation
1. Identify the affected execution and instrument.
2. Compare requested valuation date with received price date.
3. Confirm whether fallback pricing was applied.
4. Verify the upstream market-data feed before rerunning.

## INC-009 — Duplicate position ingestion

### Symptoms
- Portfolio exposure is approximately doubled.
- Position count is higher than expected.
- Logs mention duplicate business keys.

### Typical cause
A position file was ingested twice after a retry.

## INC-021 — Missing FX rate

### Symptoms
- Valuation fails for portfolios containing foreign-currency positions.
- Logs contain FX_RATE_NOT_FOUND.

### Typical cause
The FX feed did not publish a required currency pair.
