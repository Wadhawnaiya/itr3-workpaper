# Form applicability, Cover, Part A GEN1/GEN2, envelope

## 1. When ITR-3 applies (practical CA-firm tree)

**ITR-3** — Individual or HUF who has income from **profits and gains of business or profession** (including partners in firms receiving remuneration/interest/share, and many cases where tax audit applies). Also used when business income coexists with salary, HP, CG, OS.

| Situation | Typical form |
|-----------|--------------|
| Salary + HP + other sources only (no business) | ITR-1 or ITR-2 (by conditions) |
| Capital gains / more than one HP / foreign assets etc. without business | ITR-2 |
| Presumptive business/profession under 44AD/44ADA and eligible | Often **ITR-4** — but confirm eligibility |
| Business/profession with books, partner in firm, director with certain disclosures, depreciation schedules, etc. | **ITR-3** |
| Company / firm / LLP as assessee | Different ITRs (not this skill) |

**Skill rule:** If facts clearly show no business/profession and no partner-firm income → **stop** and recommend correct form. Never auto-switch silently. Borderline → recommend ITR-3 only with CA confirmation note.

## 2. Year and form metadata

| Item | Value for this skill |
|------|----------------------|
| Assessment Year | 2026-27 |
| Previous Year | 01-Apr-2025 to 31-Mar-2026 |
| FormName | `ITR-3` |
| AssessmentYear (schema) | `"2026"` |
| SchemaVer / FormVer | `Ver1.0` |

## 3. Cover section (workpaper id: `Cover`)

Capture at minimum:

- Name, PAN, DOB, Aadhaar (if provided), status (Individual/HUF)
- Address, mobile, email
- Residential status (RES / NOR / NRI) with basis if known
- Tax regime: **new / old / unknown**
- Nature of business (brief)
- Whether books maintained; whether tax audit u/s 44AB
- Partner in firm? (Y/N)
- Filing section if known (139(1) original, belated, revised, etc.)
- Preparer note: draft for CA/taxpayer review

**Status:** `missing` if PAN/DOB/regime unknown.

## 4. PartA_GEN1 (workpaper id: `PartA_GEN1`)

### Purpose
Personal information and filing status.

### Source documents
Client profile/KYC, prior ITR, Aadhaar/PAN card copies, AIS residential clues, Form 16 address (weak).

### Extraction
1. Legal name as on PAN → AssesseeName (SurNameOrOrgName required; FirstName if individual)
2. PAN pattern `[A-Z]{5}[0-9]{4}[A-Z]`
3. DOB `YYYY-MM-DD`
4. Status: `I` Individual / `H` HUF
5. Address: ResidenceNo, LocalityOrArea, CityOrTownOrDistrict, StateCode, CountryCode (`91` for India), mobile, email
6. FilingStatus:
   - `ReturnFileSec` integer enum (e.g. 11 = original under 139(1) — **confirm mapping table in schema**)
   - `IncFrmBusOrProf`: `Y` for ITR-3 business cases
   - `ResidentialStatus`: `RES` | `NRI` | `NOR`
   - Flags: HeldUnlistedEqShrPrYrFlg, ForeignExchangeFlag, FiiFpiFlag → `Y`/`N` from facts
   - `ItrFilingDueDate` must be schema enum (e.g. `2026-07-31` not always valid — use allowed dates only)
   - `SeventhProvisio139`: Y/N per facts

### Common mistakes
- Using display date formats in schema fields (use ISO)
- Inventing Aadhaar
- Wrong residential status from incomplete stay facts
- Leaving IncFrmBusOrProf as N while filing ITR-3 with BP income

### Schema mapping:
- `ITR.ITR3.PartA_GEN1.PersonalInfo.*`
- `ITR.ITR3.PartA_GEN1.FilingStatus.*`
- Required PersonalInfo: AssesseeName, PAN, Address, SecondaryAdd, DOB, Status

## 5. PartA_GEN2 (workpaper id: `PartA_GEN2`)

### Purpose
Audit information and nature of business.

### Source documents
Tax audit report (3CA/3CB-3CD), engagement letter, books note, GST registration / nature codes, partner deed.

### Extraction
1. `LiableSec44AAflg` — books of account obligation
2. `LiableSec44ABflg` — tax audit (Y/N) from turnover + cash tests + presumptive opt-out
3. `AccountAuditFlag` — whether accounts audited
4. If audited: auditor name, membership, firm, UDIN, report date, form 3CA/3CB — **only if provided; never invent UDIN**
5. `LiableSec92Eflg` — transfer pricing report if international transactions
6. Nature of business codes (`NatOfBus`) when known

### Common mistakes
- Marking audit N when turnover clearly above 44AB without cash-light analysis
- Inventing UDIN / membership number
- Forgetting partner-firm audit implications for firm (assessee is still individual partner on ITR-3)

### Schema mapping:
- `ITR.ITR3.PartA_GEN2.AuditInfo.*` (required)
- `ITR.ITR3.PartA_GEN2.NatOfBus` (optional but important when known)

## 6. Tax regime election handling

1. Read client_profile / Form 10-IEA acknowledgements if any
2. New regime is default for many individuals — still require **explicit** workpaper field
3. Old-regime claims need evidence of valid option / Form 10-IEA as applicable for the year
4. Conflict (new regime + full 80C basket) → Cover + ScheduleVIA `judgment`

### Schema mapping:
FilingStatus regime-related fields (Form10IEA* family) — populate only from documents; see `ITR3_structure.txt` under FilingStatus.

## 7. E-filing envelope + CreationInfo + Form_ITR3 + Verification

### Form_ITR3
```json
{
  "FormName": "ITR-3",
  "Description": "ITR-3 draft for CA / taxpayer review before filing",
  "AssessmentYear": "2026",
  "SchemaVer": "Ver1.0",
  "FormVer": "Ver1.0"
}
```

### CreationInfo
SWVersionNo, SWCreatedBy (`SW########`), JSONCreatedBy, JSONCreationDate, IntermediaryCity, Digest (`"-"` if unknown).

### Verification (workpaper id: `Verification`)
- Declaration: AssesseeVerName, FatherName, AssesseeVerPAN
- Capacity: `S` Self | `R` Representative | `K` Karta | `A` Authorised Signatory
- Date, Place
- **Never fake DSC/EVC.** Leave only what schema requires; note CA will complete verification at filing.

### Schema mapping:
- `ITR.ITR3.CreationInfo`
- `ITR.ITR3.Form_ITR3`
- `ITR.ITR3.Verification`
