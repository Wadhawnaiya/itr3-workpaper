# Special schedules — FA, AL, GST, FSI/TR, PTI, SPI, SI, ESOP, VDA, 5A

**Highest hallucination risk area.** Prefer `not_applicable` with affirmative basis over inventing rows.

---

## ScheduleFA — Foreign Assets (workpaper id: `ScheduleFA`)

### Purpose
Disclosure of foreign assets/income for residents (and as applicable).

### Do / Don't
- **Do** fill only if passport, foreign bank, overseas property, foreign equity, or AIS foreign items exist
- **Don't invent** foreign bank accounts, pe accounts, or trusts to "complete" the form
- If resident with no foreign assets stated → `not_applicable` + note "no foreign assets per profile/AIS"
- AssetOutIndiaFlag in PartB_TTI must be consistent (`NO` if FA N/A)

### Schema mapping:
- `ITR.ITR3.ScheduleFA`

---

## ScheduleAL — Assets & Liabilities (workpaper id: `ScheduleAL`)

### Purpose
Statement of assets and liabilities above applicability threshold.

### Rule
1. Check current applicability threshold (thresholds file / CA confirmation)
2. If applicable: list immovable property, movables, financial assets, liabilities from client data
3. If threshold unclear → `judgment`
4. **Never invent** jewellery/property values

### Schema mapping:
- `ITR.ITR3.ScheduleAL`

---

## ScheduleGST (workpaper id: `ScheduleGST`)

### Purpose
GST turnover / tax details for cross-check with books.

### Source documents
GSTR-3B/1/9 summaries, GST portal export, books sales.

### Extraction
Turnover per GST vs books vs PARTA_PL — mismatches → reconciliation **mismatch**.

### Schema mapping:
- `ITR.ITR3.ScheduleGST`

---

## ScheduleFSI / ScheduleTR (workpaper ids: `ScheduleFSI`, `ScheduleTR`)

### Purpose
Foreign source income and tax relief (DTAA / Sec 90/90A/91).

### Rule
Only if foreign income/tax credit documents exist. Schema key may be `ScheduleTR1` — use **schema names** in e-filing JSON.

### Schema mapping:
- `ITR.ITR3.ScheduleFSI`
- `ITR.ITR3.ScheduleTR1` (verify in structure dump)

---

## SchedulePTI — Pass Through Income (workpaper id: `SchedulePTI`)

### Purpose
Income from business trusts / AIF / pass-through entities as reported.

### Source documents
Form 64A/64B etc., AIS pass-through.

### Schema mapping:
- `ITR.ITR3.SchedulePTI`

---

## ScheduleSPI / ScheduleSI (workpaper ids: same)

### Purpose
- SPI: Specified person income clubbing
- SI: Income chargeable at special rates

### Rule
Clubbing only with facts (spouse/minor). Special rates for lottery, unexplained, certain CG — align with PartB_TTI.

### Schema mapping:
- `ScheduleSPI`, `ScheduleSI`

---

## ScheduleIF — Partner in firm (workpaper id: `ScheduleIF`)

### Purpose
Details of firms where assessee is partner; share of income, remuneration, interest.

### Source documents
Partnership deed, firm ITR / computation, 26AS 194T, capital account.

### High-risk
- Remuneration/interest taxable under PGBP
- TDS u/s **194T** (new) — reconcile
- Do not invent firm PAN/share ratios

### Schema mapping:
- `ITR.ITR3.ScheduleIF` (and related GEN partner detail structures if present)

---

## ScheduleESOP (workpaper id: `ScheduleESOP`)

### Purpose
ESOP/ESOS taxation events.

### Source documents
Employer ESOP statement, Form 12BA, AIS.

### Schema mapping:
- `ITR.ITR3.ScheduleESOP`

---

## ScheduleVDA (workpaper id: `ScheduleVDA`)

Also covered under income heads. Include here for special schedule completeness.

### Schema mapping:
- `ITR.ITR3.ScheduleVDA`

---

## Schedule5A (workpaper id: `Schedule5A`)

### Purpose
Portuguese Civil Code apportionment (Goa etc.) when spouses governed by that code elect apportionment.

### Rule
Almost always N/A outside that fact pattern. Do not populate casually.

### Schema mapping:
- `ITR.ITR3.Schedule5A2014` (schema key name — verify)

---

## Quick N/A decision table

| Schedule | Affirmative N/A when |
|----------|----------------------|
| FA | Profile + AIS: no foreign assets; RES confirmed |
| AL | Below threshold **and** CA agrees / threshold documented |
| GST | Not registered and no GST turnover |
| FSI/TR | No foreign income |
| ESOP | No employer stock plans |
| VDA | No crypto/VDA trades |
| 5A | Not under Portuguese Civil Code apportionment |
| PTI | No pass-through income in AIS/docs |
