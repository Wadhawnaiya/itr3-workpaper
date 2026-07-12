# CBDT ITR-3 validation rules — distilled themes (AY 2026-27)

Source PDF (not redistributed in full):  
`CBDT_e-filing_ITR-3_Validation Rules_V1.0_AY 26-27.pdf`

This note is a **guidance layer** for common upload failures. **JSON Schema validation remains the hard gate** for the e-filing file. Category A rules may still reject a schema-valid JSON.

## Rule categories (conceptual)

| Category | Meaning for preparer |
|----------|----------------------|
| **A** | Typically **blocks** upload / e-verification path — fix before filing |
| **B** | Warnings / conditional — review carefully |
| **D** | Defective return risk themes — fix to avoid notices |

Re-open the official PDF when unsure; do not rely solely on this distillation.

## Themes that commonly fail business individual ITR-3 uploads

### 1. Totals mismatch
- Part B-TI head totals ≠ schedule footings (Salary, HP, BP, CG, OS)
- Gross total income / total income arithmetic breaks
- Tax payable vs tax paid / refund identity fails

**Mitigation:** After building schedules, recompute PartB-TI/TTI from schedule totals; keep integers consistent.

### 2. Mandatory schedule missing when flag set
- Business income flag Y but BP/BS/PL incomplete
- Audit flags Y without audit detail fields
- FA/AL/GST flags inconsistent with schedule presence
- TDS claimed without TDS schedule rows

**Mitigation:** Every Y flag that implies a schedule must have corresponding populated nodes (or change the flag).

### 3. TDS / TCS vs income inconsistencies
- Salary TDS without salary income
- Interest TDS far in excess of OS interest disclosed
- Claimed credit > 26AS (portal will often reject / notice)

**Mitigation:** Run reconciliation-rules.md; never claim orphan TDS.

### 4. Depreciation / fixed asset integrity
- DEP totals vs BP depreciation deduction mismatch
- Additions without put-to-use logic
- Negative block without disposal explanation

### 5. Loss set-off order violations
- Speculative loss set off against non-speculative incorrectly
- CG loss buckets mixed
- Brought-forward loss without CFL support

### 6. Presumptive vs books contradictions
- 44AD fields populated while full BS/PL implies regular books without clear narrative
- Turnover above presumptive limit still using presumptive rates

### 7. Partner / firm inconsistencies
- Partner income without Schedule IF details
- Remuneration without corresponding firm disclosure
- 194T TDS without partner income (or reverse)

### 8. Personal info / verification defects
- PAN/name pattern failures
- Invalid email/mobile
- Verification capacity inconsistent with status (e.g. Karta on Individual)
- Digest/signature fields incorrectly fabricated

### 9. Regime / deduction conflicts
- Chapter VI-A claims inconsistent with new regime election fields
- Form 10-IEA acknowledgements missing when old regime claimed (where required)

### 10. Foreign asset / Schedule AL
- AssetOutIndiaFlag YES without FA details
- AL required by income threshold but omitted

## Skill operating rules

1. Pass **jsonschema** against `schema_ITR3.json` before writing e-filing upload file.
2. Run mental Category A checklist above; log residual risks in handoff notes.
3. Do **not** claim "portal ready" — say "schema-validated draft; Category A rules may still apply."
4. When PDF updates, refresh this note and thresholds; keep PDF path in project docs.

## Out of scope for v1 automation

Encoding every Category A rule as executable code. Future enhancement: machine-readable rule pack. For now, schema + recon + this checklist.
