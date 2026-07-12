# Income heads — Salary, HP, Capital Gains, Other Sources, Exempt Income

## ScheduleS — Salary (workpaper id: `ScheduleS`)

### Purpose
Income under the head Salaries (including pension).

### Source documents
Form 16 (Parts A/B), AIS salary tables, Form 26AS TDS u/s 192, employer salary register, arrears details.

### Extraction
1. Gross salary, perquisites, profits in lieu of salary
2. Exemptions u/s 10 (HRA, LTA, etc.) only with evidence / Form 12BB
3. Standard deduction (confirm AY amount from thresholds file)
4. Professional tax / entertainment allowance as applicable
5. TDS credit must flow to Schedule TDS1 and PartB_TTI TaxPaid

### Reconciliation
Form 16 gross vs AIS salary — see `reconciliation-rules.md`. Mismatch → do not silently pick one source.

### Common mistakes
- Double counting reimbursements already exempt
- Ignoring multiple employers
- Claiming HRA without rent evidence when required

### Schema mapping:
- `ITR.ITR3.ScheduleS` (optional schedule — omit if no salary)
- Salary total flows to `PartB-TI.Salaries`

---

## ScheduleHP — House Property (workpaper id: `ScheduleHP`)

### Purpose
Self-occupied / let-out / deemed let-out property income.

### Source documents
Property details note, municipal tax receipts, loan interest certificate (bank), co-ownership deed, rent agreements, AIS (rarely for rent).

### Extraction
1. Property address, ownership share, type (SOP/LOP)
2. Gross annual value / rent received
3. Municipal taxes **paid** by owner during year
4. Standard deduction 30% of NAV (let-out)
5. Interest u/s 24(b) — SOP cap Rs. 2,00,000 (see thresholds)
6. Pre-construction interest amortisation if applicable

### Common mistakes
- Claiming municipal tax not paid by assessee
- Full interest on co-owned property without share split
- Treating vacant let-out as SOP without legal basis

### Schema mapping:
- `ITR.ITR3.ScheduleHP`
- Flows to `PartB-TI.IncomeFromHP`

---

## Capital gains family (workpaper ids: `ScheduleCG`, `Schedule112A`, `Schedule115AD`, `ScheduleVDA`)

### Purpose
STCG/LTCG across asset classes; special schedules for 112A equity, 115AD, virtual digital assets.

### Source documents
Broker P&L / capital gains statement, contract notes, AIS (securities), demat statements, property sale deed + stamp value, VDA exchange statements, cost of acquisition proofs.

### Extraction
1. Classify each disposal: STCG vs LTCG; section rate bucket
2. 112A: STT-paid equity/equity MF — fill Schedule112A rows; apply exemption threshold per current law
3. Property: full value of consideration vs stamp duty value (50C/43CA interactions if relevant)
4. VDA: ScheduleVDA — rate as per current law; losses set-off restrictions
5. Missing cost → status `missing` for that line — **never invent cost**

### Common mistakes
- Applying outdated indexation rules post CG reforms
- Ignoring AIS CG entries not in broker statement (or vice versa)
- Netting VDA incorrectly against other CG

### Schema mapping:
- Primary CG schedule in schema: **`ScheduleCGFor23`** (verify name — workpaper id remains `ScheduleCG`)
- `Schedule112A`, `Schedule115AD`, `ScheduleVDA`
- Totals feed `PartB-TI.CapGain` and special-rate fields

---

## ScheduleOS — Other Sources (workpaper id: `ScheduleOS`)

### Purpose
Interest, dividends, family pension, gifts u/s 56(2)(x), winnings, etc.

### Source documents
AIS interest/dividend, bank interest certificates, 26AS, books (Interest Received), gift deeds, lottery TDS.

### Extraction
1. Savings / FD / other interest — reconcile AIS vs books (planted mismatches common)
2. Dividends (taxable)
3. Family pension deduction if applicable
4. Lottery/crossword winnings at special rates → also Schedule SI
5. Do not force 80TTA/80TTB under wrong regime

### Schema mapping:
- `ITR.ITR3.ScheduleOS`
- Flows to `PartB-TI.IncFromOS`

---

## ScheduleEI — Exempt Income (workpaper id: `ScheduleEI`)

### Purpose
Incomes not forming part of total income (e.g. agri income reporting, certain 10 exemptions for disclosure).

### Source documents
Agri income proofs, PF interest exemptions as disclosed, other exempt receipts in AIS.

### Rule
Disclose when required; do not invent agricultural income to fill the schedule.

### Schema mapping:
- `ITR.ITR3.ScheduleEI`
