# Deductions, loss schedules, Part B-TI / Part B-TTI

## ScheduleVIA_and_80s (workpaper id: `ScheduleVIA_and_80s`)

### Purpose
Chapter VI-A deductions. Workpaper groups 80C/80D/80G/… for review; e-filing expands to schema schedules.

### Source documents
Investment proofs, insurance premium receipts, donation receipts (80G), tuition fees, housing loan principal (80C), medical insurance (80D), NPS statements.

### Extraction
1. Confirm **tax regime** first — most 80C/80D claims invalid under new regime
2. Only amounts with evidence
3. 80G: donee name, PAN, amount, with/without qual. limit, donation type
4. Cap claims at statutory limits (thresholds file)
5. Employer NPS 80CCD(2) may still apply under new regime — check payslip/Form 16

### Common mistakes
- Claiming full 80C under new regime without flagging conflict
- 80D without policy document (premium amount from AIS alone may be incomplete)
- 80G without donee approval status

### Schema mapping (e-filing — expand):
- `Schedule80C`, `Schedule80D`, `Schedule80DD`, `Schedule80U`, `Schedule80E`, `Schedule80EE`, `Schedule80EEA`, `Schedule80EEB`
- `Schedule80G`, `Schedule80GGA`, `Schedule80GGC`
- `Schedule80_IA`, `Schedule80_IB`, `Schedule80_IC`, `Schedule80RA`
- Aggregator: `ScheduleVIA`
- Totals → `PartB-TI.DeductionsUndSchVIADtl`

---

## ScheduleCYLA / ScheduleBFLA / ScheduleCFL (workpaper ids: same)

### Purpose
- **CYLA**: set-off of current-year losses across heads
- **BFLA**: brought-forward losses set-off against current income
- **CFL**: carry-forward loss inventory for future years

### Source documents
Prior-year ITR / computation / loss schedules, current year head-wise incomes.

### Extraction
1. Build head-wise current income/loss
2. Apply statutory set-off order (house property loss, business loss, speculation, STCG/LTCG buckets)
3. Brought-forward: only if prior-year return filed within time where required
4. Incomplete carry-forward support → `judgment`/`missing` — do not invent b/f amounts

### Schema mapping:
- `ITR.ITR3.ScheduleCYLA` (**required**)
- `ITR.ITR3.ScheduleBFLA` (**required**)
- `ITR.ITR3.ScheduleCFL` (optional but needed when losses exist)
- `ITR3ScheduleUD` for unabsorbed depreciation when applicable (workpaper id `ScheduleUD`)

---

## ScheduleAMT / ScheduleAMTC (workpaper ids: same)

### Purpose
Alternate minimum tax / credit for eligible assessees.

### Rule
Often N/A for many individuals under new regime — confirm before skipping. If AMT history exists, populate credit carefully from prior computations.

### Schema mapping:
- `ScheduleAMT`, `ScheduleAMTC`

---

## PartB-TI — Computation of Total Income (workpaper id: `PartB-TI`)

### Purpose
Aggregate salaries, HP, PGBP, CG, OS → GTI → deductions → Total Income. Must be **arithmetically consistent** with schedules populated.

### Extraction checklist
1. Salaries ← ScheduleS
2. IncomeFromHP ← ScheduleHP
3. ProfBusGain ← ITR3ScheduleBP
4. CapGain ← CG family
5. IncFromOS ← ScheduleOS
6. TotalTI / losses / set-off bridges (CYLA/BFLA)
7. GrossTotalIncome
8. DeductionsUndSchVIADtl
9. TotalIncome (rounded as per practice / schema integers)

### Common mistakes
- Totals not matching schedule footings
- Ignoring special-rate income buckets
- Deductions exceeding available GTI without note

### Schema mapping:
- `ITR.ITR3.PartB-TI.*` (**required** — many integer fields)

---

## PartB_TTI — Tax computation & taxes paid (workpaper id: `PartB_TTI`)

### Purpose
Tax on total income (normal + special rates), surcharge/cess, interest 234A/B/C, relief, taxes paid, refund/payable, foreign asset flag.

### Extraction
1. TaxPayableOnTI from slabs for chosen regime + special rates (CG, lottery, VDA)
2. GrossTaxPayable, credits (115JD etc.) if any
3. Interest 234 only if computable
4. TaxPaid.TaxesPaid ← advance tax (Schedule IT) + TDS + TCS + self-assessment
5. RefundDue + BankAccountDtls (BankDtlsFlag Y/N; account numbers only if provided — never invent IFSC/account)
6. AssetOutIndiaFlag: `YES` | `NO` (not Y/N)

### Common mistakes
- Wrong regime slabs
- TDS credit not matching TDS schedules / 26AS
- Inventing bank account for refund
- AssetOutIndiaFlag inconsistent with Schedule FA

### Schema mapping:
- `ITR.ITR3.PartB_TTI.ComputationOfTaxLiability`
- `ITR.ITR3.PartB_TTI.TaxPaid`
- `ITR.ITR3.PartB_TTI.Refund`
- `ITR.ITR3.PartB_TTI.AssetOutIndiaFlag`
