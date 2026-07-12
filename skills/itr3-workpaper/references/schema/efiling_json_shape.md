# Building the third output: validated ITR-3 e-filing JSON

Map, not territory. Per-schedule field mappings live under **"Schema mapping:"** headings in the schedule reference files. This file covers envelope, required vs optional nodes, validation workflow, and known quirks.

## Purpose

Second JSON (`efiling.json`) mirrors workpaper facts but uses **only** Income Tax Department ITR-3 Main V1.1 schema keys (`references/schema/schema_ITR3.json`). Renderer validates with `jsonschema` Draft-04 before writing `<slug>_itr3_efiling_upload.json`.

**Schema-valid ≠ portal-accepted.** Category A validation rules (CBDT PDF) may still fail. Incomplete-but-valid (or incomplete-and-failing with clear errors) is expected — never pad invented numbers.

## Top-level envelope

```json
{
  "ITR": {
    "ITR3": {
      "CreationInfo": { ... },
      "Form_ITR3": { ... },
      "PartA_GEN1": { ... },
      "PartA_GEN2": { ... },
      "PARTA_BS": { ... },
      "PARTA_PL": { ... },
      "ITR3ScheduleBP": { ... },
      "ScheduleCYLA": { ... },
      "ScheduleBFLA": { ... },
      "PartB-TI": { ... },
      "PartB_TTI": { ... },
      "Verification": { ... }
      /* + optional schedules only when applicable */
    }
  }
}
```

`additionalProperties: false` everywhere. Wrong key = validation failure.

## Schema-required nodes on ITR3

Confirm against `definitions.ITR3.required` in `schema_ITR3.json` (current Main V1.1):

| Node | Role |
|------|------|
| `CreationInfo` | Software metadata; Digest may be `"-"` per pattern `-|.{44}` if not knowable — **never fake crypto digests** |
| `Form_ITR3` | FormName=`ITR-3`, AssessmentYear=`2026`, SchemaVer/FormVer=`Ver1.0` |
| `PartA_GEN1` | PersonalInfo + FilingStatus |
| `PartA_GEN2` | AuditInfo (+ NatOfBus when known) |
| `PARTA_BS` | FundSrc + FundApply (or NoBooks path as schema allows) |
| `PARTA_PL` | Credits/Debits/TaxProvAppr etc. |
| `ITR3ScheduleBP` | Business income computation |
| `ScheduleCYLA` | Current-year loss adjustment |
| `ScheduleBFLA` | Brought-forward loss adjustment |
| `PartB-TI` | Total income build-up |
| `PartB_TTI` | Tax computation + tax paid + refund + AssetOutIndiaFlag |
| `Verification` | Declaration, Capacity, Date, Place — placeholders only as allowed; never fake signature |

Optional properties (include only when applicable): ScheduleS, ScheduleHP, ManufacturingAccount, TradingAccount, PARTA_OI, PARTA_QD, depreciation family, ScheduleCGFor23, Schedule112A, ScheduleVDA, ScheduleOS, ScheduleVIA / 80*, ScheduleIT, ScheduleTDS*, ScheduleTCS, ScheduleFA, ScheduleAL, ScheduleGST, ScheduleESOP, etc.

## Form_ITR3 (copy-paste legal values)

```json
{
  "FormName": "ITR-3",
  "Description": "ITR-3 draft for CA / taxpayer review before filing",
  "AssessmentYear": "2026",
  "SchemaVer": "Ver1.0",
  "FormVer": "Ver1.0"
}
```

## CreationInfo

Typical fields (all required in V1.1):

| Field | Notes |
|-------|-------|
| `SWVersionNo` | e.g. `"1.0"` |
| `SWCreatedBy` | pattern `[S][W][0-9]{8}` e.g. `SW00000001` |
| `JSONCreatedBy` | same pattern |
| `JSONCreationDate` | `YYYY-MM-DD` |
| `IntermediaryCity` | city string |
| `Digest` | `"-"` or 44-char digest — do not invent signatures |

## Starter skeleton

`references/schema/minimal_valid_itr3_skeleton.json` is a **schema-valid empty-ish** tree (zeros / N flags). Use it as structure only — replace with client facts. Do not ship skeleton figures as if they were client numbers.

## Workpaper ↔ e-filing discipline

| Workpaper status | E-filing handling |
|------------------|-------------------|
| `filled` | Populate corresponding schema nodes |
| `missing` | Omit optional nodes; leave required zeros only if structurally needed — **never invent** business figures |
| `judgment` | Populate only known fields; notes stay in workpaper |
| `not_applicable` | **Omit** optional schedule keys (opposite of workpaper, which requires explicit N/A entry) |

## Validation command

```
python3 scripts/render_output.py <workpaper.json> <output_dir> <efiling.json>
```

- Pass → writes `<slug>_itr3_efiling_upload.json`
- Fail → all violations (JSON path + message) on stderr; **no** efiling write; docx/html still written

Needs `jsonschema` (`pip install jsonschema`).

## Field-name lookup

1. `references/schema/ITR3_structure.txt` — flattened dump
2. `python3 scripts/dump_schema_structure.py` — regenerate dump
3. Grep `schema_ITR3.json` definitions
4. Per-schedule **"Schema mapping:"** in `references/schedules-*.md`

## Known quirks

1. Schema property for capital gains schedule is often `ScheduleCGFor23` (not bare `ScheduleCG`) — check schema.
2. Some Y/N patterns are unanchored (`Y|N`) — substring typos can pass validation; eyeball flags.
3. `AssetOutIndiaFlag` uses `YES`/`NO` (not Y/N).
4. Filing due date enum is constrained (e.g. `2026-08-31`, `2026-10-31`, `2026-11-30`) — use legal enum values only.
5. `JSONCreatedBy` / `SWCreatedBy` require `SW` + 8 digits.
6. Workpaper id `ScheduleVIA_and_80s` expands to multiple schema schedules (`Schedule80C`, `Schedule80D`, `ScheduleVIA`, …).
7. Official schema node `ScheduleTR1` may map to workpaper `ScheduleTR` — use schema key names in efiling JSON.

## Incompleteness is expected

Required nodes may force deep zero trees when books are incomplete. Document gaps in workpaper notes. User finishes in official offline utility / firm software with taxpayer authentication.
