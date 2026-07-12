# Workpaper JSON schema (input to `scripts/render_output.py`)

Build one JSON object per client, then run:

```
python3 scripts/render_output.py <workpaper.json> <output_dir> [efiling.json]
```

Produces `<slug>_itr3_workpaper.docx` and `<slug>_itr3_workpaper.html`. Optionally validates and writes e-filing JSON.

The renderer only lays out data — it does **not** compute tax, invent figures, or judge positions.

## Top-level shape

```json
{
  "form_type": "ITR-3",
  "assessment_year": "2026-27",
  "schema_ver": "Ver1.0",
  "client": {
    "name": "Rohan Mehta",
    "pan": "ABCDE1234F",
    "dob": "15-Jan-1990",
    "status": "Individual",
    "residential_status": "RES",
    "tax_regime": "new",
    "previous_year": "01-Apr-2025 to 31-Mar-2026",
    "address": "..."
  },
  "sections": [
    {
      "id": "ScheduleS",
      "title": "Salary",
      "status": "filled",
      "answer": "Gross salary per Form 16 ...",
      "table": [{"line": "Gross salary", "amount": "420000"}],
      "source_refs": ["Form 16 Part B", "AIS salary"],
      "notes": ""
    }
  ],
  "reconciliations": [
    {
      "item": "Bank interest AIS vs books",
      "status": "mismatch",
      "books": 18000,
      "ais": 24500,
      "workpaper_amount": 24500,
      "notes": "AIS higher by 6500 — obtain bank certificate / passbook."
    }
  ]
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `form_type` | yes | Always `"ITR-3"` for this skill |
| `assessment_year` | yes | `"2026-27"` |
| `schema_ver` | recommended | `"Ver1.0"` matching Form_ITR3.SchemaVer pattern |
| `client` | yes | Flat label→value cover facts |
| `sections` | yes | Ordered array — **every canonical id** present |
| `reconciliations` | strongly recommended | AIS/26AS/Form16/books cross-checks |

## Section entry fields

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Exact canonical id (see list below). Completeness checker matches these strings. |
| `title` | yes | Short human heading |
| `status` | yes | `filled` \| `missing` \| `judgment` \| `not_applicable` |
| `answer` | no | Free-text drafted answer |
| `table` | no | List of objects (keys = headers) or list of lists |
| `source_refs` | recommended | Documents/ledgers supporting amounts |
| `notes` | when missing/judgment | Mandatory explanation for flags |

## Status values

- **`filled`** — confident, fully sourced. No badge.
- **`missing`** — factual figure/document absent. **Never invent** to avoid this. Notes: what is missing and usual source.
- **`judgment`** — facts present; tax treatment needs CA sign-off. Best-guess answer + explanation in notes.
- **`not_applicable`** — affirmatively N/A from documents/profile. Unchecked ≠ N/A (use `missing`).

## Canonical section ids (must match renderer)

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

**Workpaper vs e-filing:** workpaper may group VI-A under `ScheduleVIA_and_80s` with internal tables. E-filing JSON must expand to exact schema keys (`Schedule80C`, `Schedule80D`, `ScheduleVIA`, etc.).

## Reconciliation entry fields

| Field | Notes |
|-------|-------|
| `item` | What is being compared |
| `status` | `matched` \| `mismatch` \| `missing` |
| `form16` / `books` / `ais` / `form26as` | Source amounts (use whichever apply) |
| `workpaper_amount` | Amount adopted in workpaper |
| `notes` | Always for mismatch/missing |

## Completeness checking

Any canonical id absent from `sections` (not even `not_applicable`) triggers a red warning banner in docx/html. Silent omission looks identical to forgetting a schedule — always emit an explicit entry.

## Example minimal section

```json
{
  "id": "ScheduleFA",
  "title": "Foreign Assets",
  "status": "not_applicable",
  "answer": "Client profile and AIS show no foreign assets/income. Resident and ordinarily resident — Schedule FA not required on facts stated.",
  "notes": "Do not invent foreign assets. Reconfirm if residential status changes or overseas bank account appears."
}
```
