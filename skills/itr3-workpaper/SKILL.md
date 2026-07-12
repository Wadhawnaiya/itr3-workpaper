---
name: itr3-workpaper
description: This skill should be used when the user asks to "prepare an ITR-3 workpaper", "draft ITR-3", "generate ITR-3 JSON", "map these documents to ITR-3 schedules", "prepare business return workpaper", or hands over a client's Form 16, AIS/TIS, Form 26AS, trial balance, financial statements, capital gains statements, house property details, deduction proofs, bank interest, GST summaries, or similar source documents for an Income-tax Act ITR-3 return. Produces a schedule-by-schedule draft workpaper (Word + HTML) plus a schema-validated ITR-3 e-filing JSON for Chartered Accountant / taxpayer review — it does not file, sign, or replace professional judgment.
version: 0.1.0
---

# ITR-3 Workpaper (AY 2026-27)

## What this skill does and does not do

Turn a client's raw Indian tax/accounting documents into a first-pass, schedule-by-schedule **ITR-3 workpaper** for **Assessment Year 2026-27 / Previous Year 2025-26** (1-Apr-2025 to 31-Mar-2026) under the **Income-tax Act, 1961**. Target users are CA-firm junior staff; the reviewing CA should spend time on judgment, AIS mismatches, and missing proofs — not first-pass data entry.

**Produces (when possible):**
1. `<client>_itr3_workpaper.docx` — schedule-by-schedule Word workpaper
2. `<client>_itr3_workpaper.html` — same content, color-coded review UI + dashboards
3. `<client>_itr3_efiling_upload.json` — official-schema-shaped ITR-3 draft JSON, **validated** against the bundled ITD schema before write

**Never:**
- File anything on the Income Tax portal
- Sign / replace CA or taxpayer verification / DSC / EVC
- Fabricate a factual figure not present in source documents
- Claim schema validation = guaranteed portal acceptance
- Store or request client passwords
- Silently switch to another ITR form

Every output must be labeled **"Draft — for CA / taxpayer review before filing"**.

**Do not confuse with:**
- `itr-preparation-skill` (MCP portal tools — different product)
- `itr-ca-report` (post-filing CA reports from filed ITR JSON under 44AD)
- `tax-audit-workpaper` (Form 3CA/3CB-3CD — architectural twin only)

## Design principles (non-negotiable)

1. **Never invent facts.** Missing figure → status `missing` + notes naming the usual source.
2. **Judgment is allowed.** Facts present, treatment interpretive → `judgment` + best-guess + notes.
3. **N/A is affirmative.** Use `not_applicable` only when documents support N/A. Unchecked = `missing`.
4. **Two JSON conventions:**
   - **Workpaper JSON:** explicit entry for every canonical section id (even N/A).
   - **E-filing JSON:** only official schema keys (`additionalProperties: false`). Omit optional schedules when N/A.
5. **Schema is law** for the third file — field names from `references/schema/schema_ITR3.json`. Schema wins over guides if they disagree.
6. **Thresholds authority:** `references/thresholds-ay2026-27.md`.
7. **Renderer is dumb** — layout + JSON Schema validation only. Tax reasoning is in the agent-built JSONs.
8. **AIS / 26AS / Form 16 reconciliation is first-class** — never silently pick one source without notes.
9. **Tax regime (old vs new, Sec 115BAC) must be explicit** — do not assume without evidence.
10. **High-risk areas:** business vs presumptive; partners/194T; tax depreciation (not books WDV); CG 112A/VDA; HP; VI-A evidence + regime; FA/AL never invent; TDS vs 26AS; audit info/UDIN never invent; Part B-TI/TTI consistency; Verification placeholders only as schema allows.

## Step 1 — Confirm form, year, regime; gather documents

Read `references/form-applicability-and-cover.md` first.

- Confirm **ITR-3** applicability (individual/HUF with business/profession income, partner in firm, etc.).
- If facts clearly indicate **ITR-1 / ITR-2 / ITR-4 only**, **stop and say so** — do not force ITR-3.
- Confirm AY **2026-27** / PY 2025-26.
- Capture: name, PAN, DOB, address, residential status, filing section, tax regime (new/old/unknown), auditor details if any.

**Reading documents:**
- PDF/images → Read tool natively
- xlsx/xls/docx → `python3 scripts/extract_text.py <file>`
- csv/txt/json → Read directly

**Typical sources:** client profile/KYC, Form 16/16A, AIS/TIS, Form 26AS, bank interest, broker/CG statements, VDA statements, house property details, trial balance, P&L/BS/notes, tax depreciation register, GST summary, deduction proofs, prior-year ITR/computation, tax audit report if any.

## Step 2 — Map documents to schedules

Read the relevant reference guides. Each includes purpose, statutory basis, source documents, extraction steps, common mistakes, and **Schema mapping:** official field names.

| Reference | Covers |
|-----------|--------|
| `references/form-applicability-and-cover.md` | ITR form decision, Part A GEN1/GEN2, regime, audit, envelope |
| `references/schedules-income-heads.md` | Salary, HP, CG, OS, EI |
| `references/schedules-business-bs-pl.md` | BS, PL, manufacturing/trading, OI, QD, BP, ICDS, depreciation |
| `references/schedules-deductions-and-ti.md` | VI-A, AMT, CYLA/BFLA/CFL, Part B-TI/TTI |
| `references/schedules-tds-tcs-taxes-paid.md` | IT, TDS1/2/3, TCS |
| `references/schedules-special.md` | FA, AL, GST, FSI/TR, PTI, SPI, SI, ESOP, VDA, 5A |
| `references/reconciliation-rules.md` | AIS/TIS/26AS/Form16/books playbook |
| `references/thresholds-ay2026-27.md` | Rates, slabs, limits (authoritative numerics) |

## Step 3 — Build the workpaper JSON

Per `references/workpaper_schema.md`:

```json
{
  "form_type": "ITR-3",
  "assessment_year": "2026-27",
  "schema_ver": "Ver1.0",
  "client": { "name": "...", "pan": "...", "tax_regime": "new|old|unknown", "...": "..." },
  "sections": [
    {
      "id": "PartB-TI",
      "title": "Computation of Total Income",
      "status": "filled|missing|judgment|not_applicable",
      "answer": "...",
      "table": [{"line": "...", "amount": "..."}],
      "source_refs": ["AIS interest", "TB Interest Received"],
      "notes": "..."
    }
  ],
  "reconciliations": [
    {
      "item": "Salary Form 16 vs AIS",
      "status": "matched|mismatch|missing",
      "form16": 0, "ais": 0, "workpaper_amount": 0,
      "notes": "..."
    }
  ]
}
```

Rules:
- Emit **every canonical section id** (see renderer / workpaper_schema) — explicit N/A if needed
- Order: Cover → GEN → BS/PL → income → deductions → TI/TTI → taxes paid → special
- `notes` mandatory when status is `missing` or `judgment`
- `source_refs` strongly recommended for filled amounts

### Canonical section ids

```
Cover,
PartA_GEN1, PartA_GEN2,
PARTA_BS, ManufacturingAccount, TradingAccount, PARTA_PL, PARTA_OI, PARTA_QD,
ScheduleS, ScheduleHP, ITR3ScheduleBP,
ScheduleDPM, ScheduleDOA, ScheduleDEP, ScheduleDCG, ScheduleESR,
ScheduleCG, Schedule112A, Schedule115AD, ScheduleVDA, ScheduleOS,
ScheduleCYLA, ScheduleBFLA, ScheduleCFL, ScheduleICDS, ScheduleUD,
ScheduleVIA_and_80s, ScheduleAMT, ScheduleAMTC,
ScheduleSI, ScheduleSPI, ScheduleIF, ScheduleEI, SchedulePTI,
ScheduleIT, ScheduleTDS1, ScheduleTDS2, ScheduleTDS3, ScheduleTCS,
ScheduleFSI, ScheduleTR, ScheduleFA, ScheduleAL, ScheduleGST, ScheduleESOP, Schedule5A,
PartB-TI, PartB_TTI, Verification
```

## Step 3b — Build the e-filing JSON

Follow `references/schema/efiling_json_shape.md`.

- Envelope only: `{"ITR": {"ITR3": { ... }}}`
- Required nodes: `CreationInfo`, `Form_ITR3`, `PartA_GEN1`, `PartA_GEN2`, `PARTA_BS`, `PARTA_PL`, `ITR3ScheduleBP`, `ScheduleCYLA`, `ScheduleBFLA`, `PartB-TI`, `PartB_TTI`, `Verification`
- Optional schedules only when applicable/known
- Field names/enums/patterns **only** from official schema
- Never pad invented numbers to "pass" schema
- Use `references/schema/minimal_valid_itr3_skeleton.json` as structural starter; replace with real facts
- Start Form_ITR3: `FormName`=`ITR-3`, `AssessmentYear`=`2026`, `SchemaVer`/`FormVer`=`Ver1.0`

```
python3 scripts/render_output.py <workpaper.json> <output_dir> <efiling.json>
```

On validation fail: print every JSON-path error; still write docx/html; **do not** write e-filing upload file.

## Step 4 — Hand off

Present outputs + short summary:
- counts filled / judgment / missing / N/A
- top reconciliation mismatches
- sections needing CA attention first
- whether e-filing JSON validated
- reminder: draft only; file via official portal/utility with taxpayer authentication

## Testing

`assets/demo-client/` is a synthetic proprietor pack with planted issues.  
`assets/demo-client/_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md` is for developers only — **never feed as a source document**.

## Additional resources

- `references/schema/schema_ITR3.json` — official ITD ITR-3 Main V1.1 (verbatim)
- `references/schema/ITR3_structure.txt` — flattened field dump
- `references/schema/efiling_json_shape.md` — envelope + validation workflow
- `references/schema/validation_rules_notes.md` — CBDT Category A/B/D themes
- `references/workpaper_schema.md` — full workpaper contract
- `scripts/extract_text.py` — Excel/Word → text
- `scripts/dump_schema_structure.py` — regenerate structure dump
- `scripts/render_output.py` — workpaper → docx+html; optional efiling validate+write

## Maintenance

- Refresh `thresholds-ay2026-27.md` each Finance Act / slab change
- New ITD schema version → replace `schema_ITR3.json`, regenerate structure dump, re-check every "Schema mapping:"
- Re-read CBDT validation rules PDF when updated
- Keep form-applicability notes current (regime/deduction interactions change often)
