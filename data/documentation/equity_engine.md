# Equity Engine — Technical Notes

The equity engine calculates portfolio valuations using market prices associated with the requested valuation date.

## Market data
Prices should correspond to the valuation date expected by the run. The engine records warnings when market-data timestamps do not match the requested date.

## Fallback behaviour
When a valid current price is unavailable, the engine may use a fallback price depending on configuration. A successful technical execution therefore does not necessarily imply that business controls will pass.

## Controls
Large variations against the previous close are reported by the controls component and should be investigated using execution logs and market-data evidence.
