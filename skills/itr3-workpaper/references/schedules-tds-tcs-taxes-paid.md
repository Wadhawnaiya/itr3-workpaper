# Taxes paid — Schedule IT, TDS1/2/3, TCS

## ScheduleIT — Advance tax & self-assessment (workpaper id: `ScheduleIT`)

### Purpose
Row-level advance tax / self-assessment tax payments (BSR code, date, challan, amount, serial).

### Source documents
Tax paid challans, bank statement (direct tax debits), AIS tax payment section, prior computation.

### Extraction
1. Each payment: BSR code, date, serial number, amount
2. Classify advance tax vs self-assessment by date/intent if known
3. Bank statement credit without challan detail → `missing` challan fields (do not invent BSR)

### Common mistakes
- Booking bank transfer as advance tax without challan matching
- Double counting self-assessment already in AIS

### Schema mapping:
- `ITR.ITR3.ScheduleIT`
- Totals → `PartB_TTI.TaxPaid.TaxesPaid`

---

## ScheduleTDS1 — TDS on salary (workpaper id: `ScheduleTDS1`)

### Purpose
TDS u/s 192 from Form 16 / 26AS / AIS.

### Source documents
Form 16 Part A, Form 26AS, AIS TDS salary, employer TAN.

### Extraction
1. Employer TAN, name, amount paid/credited, TDS deducted, TDS claimed
2. Must reconcile to ScheduleS and Form 16
3. If Form 16 TDS ≠ 26AS → flag reconciliation **mismatch**; claim the supportable amount with notes

### Schema mapping:
- `ITR.ITR3.ScheduleTDS1`

---

## ScheduleTDS2 — TDS other than salary (workpaper id: `ScheduleTDS2`)

### Purpose
TDS on interest, contract, professional fees, rent, 194Q, **194T** (partner payments), etc.

### Source documents
Form 26AS, AIS, Form 16A, books, partner firm TDS certificates.

### Extraction
1. One row per TAN/deductor line as in 26AS (aggregate carefully)
2. Match income recognition: interest TDS should align with OS interest; contractor TDS with expenses/receipts
3. **194T**: firm payments to partners — new and easy to miss; if partner income present, look for 194T credits

### Schema mapping:
- `ITR.ITR3.ScheduleTDS2`

---

## ScheduleTDS3 — TDS per other forms / special cases (workpaper id: `ScheduleTDS3`)

### Purpose
Additional TDS schedule as schema defines (e.g. certain Form 26QC / property / other categories — verify structure dump).

### Rule
Populate only when 26AS/AIS shows lines belonging to this schedule. Else N/A in workpaper; omit in e-filing.

### Schema mapping:
- `ITR.ITR3.ScheduleTDS3`

---

## ScheduleTCS (workpaper id: `ScheduleTCS`)

### Purpose
Tax collected at source credits.

### Source documents
26AS TCS section, AIS, collector certificates.

### Note for FY 2025-26
**206C(1H) removed w.e.f. 1-Apr-2025** — do not expect sale-of-goods TCS under that clause for this year. Other TCS sections may still appear.

### Schema mapping:
- `ITR.ITR3.ScheduleTCS`

---

## Cross-schedule tax paid integrity

| Check | Action |
|-------|--------|
| Sum TDS schedules vs 26AS total | Reconciliation entry |
| Sum TDS vs PartB_TTI taxes paid credit | Must match within rounding |
| Advance tax Schedule IT vs bank | Match challans |
| Claim > 26AS without explanation | Forbidden without notes / judgment |

Never claim TDS/TCS credit without a supporting 26AS/AIS/Form 16 line unless notes document a known portal lag and CA judgment.
