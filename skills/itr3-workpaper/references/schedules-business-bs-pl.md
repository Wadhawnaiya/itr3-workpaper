# Business schedules — BS, PL, BP, OI, QD, ICDS, depreciation

## PARTA_BS — Balance Sheet (workpaper id: `PARTA_BS`)

### Purpose
Sources and application of funds as on 31-Mar-2026 (or no-books path).

### Source documents
Audited/unaudited BS, trial balance, schedules of capital, loans, fixed assets, inventories, debtors/creditors.

### Extraction
1. If books maintained: map FundSrc (capital, reserves, loans, current liabilities) and FundApply (fixed assets, investments, current assets)
2. If no books: use schema `NoBooksOfAccBS` path only when truly no books — do not invent a BS
3. TB must foot; BS must balance (FundSrc total ≈ FundApply total) — flag imbalance as judgment/missing

### Common mistakes
- Mixing books WDV with tax WDV on BS (BS is books)
- Omitting proprietor's capital account movements
- Inventing closing stock

### Schema mapping:
- `ITR.ITR3.PARTA_BS.FundSrc` / `FundApply` (required pair in standard path)
- Optional `NoBooksOfAccBS`

---

## ManufacturingAccount / TradingAccount (workpaper ids: same)

### Purpose
Manufacturing and trading accounts when activity type requires (manufacturers / traders).

### Source documents
P&L notes, stock records, manufacturing a/c in financial statements.

### Rule
Mark `not_applicable` for pure service proprietors with no manufacturing/trading. Populate when financials show these accounts.

### Schema mapping:
- `ITR.ITR3.ManufacturingAccount`
- `ITR.ITR3.TradingAccount`

---

## PARTA_PL — Profit & Loss (workpaper id: `PARTA_PL`)

### Purpose
Credits and debits to P&L, tax provisions, presumptive fields if used.

### Source documents
P&L, TB, notes to accounts, GST turnover summaries.

### Extraction
1. CreditsToPL: gross receipts, other income
2. DebitsToPL: expenses by major head
3. TaxProvAppr: tax provision / appropriations as schema requires
4. Presumptive: NatOfBus44AD / 44ADA / 44AE fields only if opted
5. Turnover vs GST: reconcile (see reconciliation-rules)

### Common mistakes
- Using GST taxable turnover as books turnover without adjustment notes
- Booking personal expenses without 40A/disallowance note in computation
- Ignoring 43B unpaid statutory dues still open at year-end

### Schema mapping:
- `ITR.ITR3.PARTA_PL.*` (many required nodes — see structure dump)

---

## PARTA_OI — Other Information (workpaper id: `PARTA_OI`)

### Purpose
Disallowances / adjustments often linked to tax audit style info (method of accounting, 40A(3), 43B, etc.) as schema provides for ITR-3.

### Source documents
Tax audit report if any, cash payment registers, MSME dues, PF/ESI challans.

### High-risk
- Cash expenses > Rs. 10,000/day/payee → 40A(3) attention in taxable profit computation notes
- 43B(h) MSME unpaid beyond statutory period
- Employee PF late deposit (36(1)(va)) — permanent disallowance risk

### Schema mapping:
- `ITR.ITR3.PARTA_OI` (optional but important when books maintained)

---

## PARTA_QD — Quantitative Details (workpaper id: `PARTA_QD`)

### Purpose
Quantitative details of principal items (trading/manufacturing).

### Source documents
Stock register, audit report quantitative annexures.

### Rule
N/A for service businesses without goods. Missing stock register for trader → `missing`.

### Schema mapping:
- `ITR.ITR3.PARTA_QD`

---

## ITR3ScheduleBP — Business Profession (workpaper id: `ITR3ScheduleBP`)

### Purpose
Compute income chargeable under PGBP — non-speculative, speculative, specified business; set-off.

### Source documents
P&L + tax adjustments computation, depreciation (tax), partner remuneration from firm (Schedule IF / firm), presumptive worksheets.

### Extraction
1. Start from net profit per P&L
2. Add disallowed expenses; deduct allowed incentives
3. Depreciation: **tax WDV** from DPM/DOA/DEP — not books depreciation alone
4. Partner: remuneration/interest taxable as business; check 194T TDS
5. Populate BusinessIncOthThanSpec, SpecBusinessInc, SpecifiedBusinessInc, IncChrgUnHdProftGain, BusSetoffCurrYr

### Common mistakes
- Using books depreciation in BP without Schedule DEP bridge
- Ignoring disallowances identified in OI
- Mixing presumptive income with full books without clear election notes

### Schema mapping:
- `ITR.ITR3.ITR3ScheduleBP.*` (**required** node)
- Flows to `PartB-TI.ProfBusGain`

---

## Depreciation family (workpaper ids: `ScheduleDPM`, `ScheduleDOA`, `ScheduleDEP`, `ScheduleDCG`, `ScheduleESR`)

### Purpose
Tax depreciation block-wise (plant & machinery, other assets), depreciation summary, capital gains on depreciable assets, scientific research.

### Source documents
Fixed asset register **with tax WDV**, additions/deletions dates, put-to-use dates, sale proceeds.

### Critical rules
1. Asset put to use **< 180 days** → generally **half** depreciation rate for that year
2. Opening WDV = tax WDV brought forward — not books WDV
3. Sale of depreciable asset → DCG / block adjustment, not always normal CG schedule alone
4. Missing put-to-use date on large addition → `missing` or `judgment`

### Schema mapping:
- `ScheduleDPM`, `ScheduleDOA`, `ScheduleDEP`, `ScheduleDCG`, `ScheduleESR`

---

## ScheduleICDS (workpaper id: `ScheduleICDS`)

### Purpose
ICDS adjustments where applicable to business income computation.

### Source documents
Tax computation notes, auditor ICDS disclosures.

### Rule
If no ICDS adjustments identified and books simple cash/mercantile without differences → may be N/A or zeros with note. Do not invent ICDS deltas.

### Schema mapping:
- `ITR.ITR3.ScheduleICDS`
