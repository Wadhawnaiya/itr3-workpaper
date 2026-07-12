# Reconciliation playbook — AIS / TIS / 26AS / Form 16 / books

Reconciliation is **first-class**. Every material income/TDS figure should cite source and flag mismatches. Never silently pick one source.

## Workpaper `reconciliations[]` status

| Status | When |
|--------|------|
| `matched` | Sources agree within Rs. 1–100 rounding (note if rounded) |
| `mismatch` | Material difference; notes must state both amounts and which was adopted |
| `missing` | Expected source document absent |

Suggested fields: `item`, `status`, `form16`, `books`, `ais`, `form26as`, `workpaper_amount`, `notes`.

## Mandatory cross-checks

### 1. Salary — Form 16 vs AIS vs Schedule S / TDS1

| Step | Action |
|------|--------|
| 1 | Gross salary Form 16 Part B |
| 2 | AIS salary information |
| 3 | 26AS u/s 192 TDS |
| 4 | Compare TDS Form 16 vs 26AS |
| 5 | If mismatch: adopt supportable figure; flag; list missing employer revision |

### 2. Bank interest — AIS vs books vs OS

| Step | Action |
|------|--------|
| 1 | Sum AIS interest (savings/FD) |
| 2 | Books / TB Interest Received + bank certificates |
| 3 | If AIS > books: often unrecorded interest — adopt AIS unless books prove error; flag mismatch |
| 4 | If books > AIS: missing AIS feed or non-AIS bank — judgment |

### 3. TDS credit — 26AS vs Schedule TDS* vs PartB_TTI

| Step | Action |
|------|--------|
| 1 | Export 26AS totals by section |
| 2 | Build TDS1/2/3 rows |
| 3 | Sum claimed credit ≤ 26AS unless documented dispute |
| 4 | Partner 194T lines present if firm payments exist |

### 4. Turnover — GST vs books vs BP / PL

| Step | Action |
|------|--------|
| 1 | GSTR-3B taxable outward + exempt if relevant |
| 2 | Books gross receipts |
| 3 | Explain differences (non-GST income, advances, credit notes timing) |
| 4 | Material unexplained gap → mismatch + judgment on BP income |

### 5. Capital gains — broker vs AIS vs CG schedules

| Step | Action |
|------|--------|
| 1 | Broker realised CG statement |
| 2 | AIS securities CG / 112A tables |
| 3 | Line missing cost → missing status on that scrip |
| 4 | Do not invent ISIN-level gains |

### 6. Prior-year losses — CFL/BFLA

| Step | Action |
|------|--------|
| 1 | Prior ITR loss schedule / assessment order |
| 2 | Confirm return filed within time for carry-forward eligibility where required |
| 3 | Incomplete → missing/judgment; never invent b/f loss |

### 7. Advance tax — bank vs Schedule IT

| Step | Action |
|------|--------|
| 1 | Identify direct tax challans in bank |
| 2 | Match BSR/date/serial/amount |
| 3 | Unmatched bank debit → missing challan detail |

### 8. Regime vs deductions

| Step | Action |
|------|--------|
| 1 | Profile regime vs VI-A folder |
| 2 | New regime + 80C/80D stack → **mismatch/conflict** reconciliation item |

## How much difference is material?

- TDS/tax credits: any difference > Rs. 100 → flag
- Interest/salary: > Rs. 1,000 or 1% → flag
- Turnover: > 1% or Rs. 10,000 → flag
- Always flag if signs differ or a whole source is missing

## Order of preference when sources conflict (default)

1. Use **primary legal source** for the item (Form 16 for salary TDS structure; 26AS for credit claim; books for PGBP; AIS as check)
2. Prefer the source that **supports credit claim** without excess credit
3. Document alternative in notes
4. CA judgment for which amount enters final filing

## Demo-oriented examples (patterns)

- AIS interest 24,500 vs books 18,000 → mismatch; adopt AIS 24,500 pending certificate
- Form 16 TDS 12,000 vs 26AS 10,000 → mismatch; claim 10,000 unless Form 16 revised
- GST turnover 1.20 cr vs books 1.15 cr → mismatch; explain or adjust BP
- Profile new regime + 80C proofs present → conflict item; do not allow 80C without regime change evidence
