# Answer key — Rohan Mehta demo (DO NOT FEED TO SKILL AS SOURCE)

A correct first-pass run should surface roughly these planted issues. Not every amount must match exactly; flags and non-hallucination matter most.

## Must catch

1. **AIS bank interest 24,500 vs books 18,000** → reconciliation `mismatch`; do not silently use books only.
2. **Form 16 TDS 12,000 vs 26AS/AIS 10,000** → reconciliation `mismatch`; credit claim should not exceed 26AS without notes.
3. **Cash expense 55,000 to Shree Balaji Packaging** → 40A(3) style attention in BP/OI computation notes (`judgment`).
4. **Computer put to use 01-Jan-2026 (<180 days)** → half tax depreciation rate (`judgment` if rate applied correctly).
5. **80D 22,000 without policy proof** → `missing` or `judgment`.
6. **Equity scrip XYZ cost missing** → CG line `missing`; do not invent cost.
7. **Municipal tax paid 12,000 vs claimed 15,000** → HP inconsistency flag.
8. **GST turnover 72,00,000 vs books sales 68,50,000** → reconciliation mismatch.
9. **Carry-forward loss 45,000 without prior-year ITR** → `missing`/`judgment` on BFLA/CFL; do not invent full CFL schedule.
10. **Partner firm / 194T** → N/A (profile says not partner) — correct N/A.
11. **Schedule FA** → `not_applicable` (no foreign assets); **must not invent FA rows**.
12. **Schedule AL** → `judgment` or conditional N/A based on income threshold — do not invent asset list.
13. **Bank NEFT 15,000 tax without challan** → Schedule IT partial `missing`.
14. **Regime NEW but 80C/ELSS/LIC folder present** → conflict flag; do not allow 80C under new regime without regime change evidence.
15. **Verification** → placeholders only; no fake DSC/signature/UDIN (no audit UDIN invented).

## Must NOT hallucinate

- Foreign assets / Schedule FA content
- UDIN / auditor details (audit not applicable / not provided)
- Cost of acquisition for XYZ Ltd
- Bank account numbers beyond what docs show (only masked accounts given)
- 80D policy number
- Prior-year loss details beyond client claim amount

## Expected form

ITR-3 is correct (proprietor with business income + salary + HP + CG).

## Deliverables check

- All canonical section ids present in workpaper
- At least one mismatch in reconciliations[] and HTML dashboard
- E-filing JSON uses only schema keys; optional FA omitted; AssetOutIndiaFlag consistent (NO)
