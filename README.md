# ITR-3 Workpaper Skill (AY 2026-27)

A [Claude Code](https://claude.com/claude-code) / [Agent Skill](https://www.anthropic.com/news/skills) that turns a client’s raw Indian tax and accounting documents into a **first-pass ITR-3 workpaper** for **Assessment Year 2026-27** (Previous Year 2025-26), under the **Income-tax Act, 1961**.

**Who this is for:** Chartered Accountant firms where junior staff do the first-pass document mapping, and the reviewing CA focuses on judgment, AIS mismatches, missing proofs, and sign-off — not pure data entry.

**What this is not:** it does **not** file on the Income Tax portal, does **not** replace DSC/EVC/UDIN, and does **not** invent figures. Every output is labeled **draft — for CA / taxpayer review before filing**.

---

## What it produces

Given a client document folder, the skill builds a structured workpaper JSON (and optional e-filing JSON), then renders:

| File | Purpose |
|------|---------|
| `<client>_itr3_workpaper.docx` | Schedule-by-schedule Word workpaper for review / re-keying |
| `<client>_itr3_workpaper.html` | Same content with color-coded status badges + dashboards |
| `<client>_itr3_efiling_upload.json` | ITR-3 draft JSON shaped to ITD **Main V1.1**, written **only if** it passes JSON Schema validation |

### Status badges (review workflow)

| Status | Meaning |
|--------|---------|
| **Filled** | Confident, fully sourced answer (no badge noise) |
| **Judgment call** | Facts present; tax treatment needs CA confirmation |
| **Missing data** | Fact not in documents — flagged, **never invented** |
| **N/A** | Affirmatively not applicable (not “didn’t check”) |

### Reconciliation dashboard

First-class AIS / TIS / Form 26AS / Form 16 / books cross-checks, with `matched` / `mismatch` / `missing` rows (e.g. interest, salary TDS, GST vs books, regime vs 80C conflict).

---

## What this is not (related products)

| Product | Difference |
|---------|------------|
| **itr-preparation-skill** (MCP) | Portal login / AIS download automation |
| **itr-ca-report** | Post-filing CA reports from *already filed* ITR JSON (e.g. 44AD packaging) |
| **tax-audit-workpaper** | Form 3CA/3CB-3CD — architectural twin for tax audit, not ITR |

This skill is **pre-filing ITR-3 only** (AY 2026-27).

---

## Installation

### Dependencies

Python 3.10+ recommended:

```bash
pip install -r requirements.txt
# or: pip install python-docx openpyxl jsonschema
```

**Code execution** must be available so the agent can run `scripts/extract_text.py` and `scripts/render_output.py`.

### Option A — Claude Desktop / claude.ai (upload zip)

1. Download **[`itr3-workpaper-skill.zip`](itr3-workpaper-skill.zip)** from this repo.
2. In Claude: **Settings → Capabilities → Skills** (wording may vary).
3. **Upload skill** and select the zip **as-is** (do not re-zip).  
   The archive contains a single top-level folder `itr3-workpaper/` with `SKILL.md` inside.
4. Enable **code execution** for the conversation/account.
5. New chat → attach client documents → ask to prepare an ITR-3 workpaper.

### Option B — Claude Code (copy skill into project)

```bash
git clone https://github.com/Wadhawnaiya/itr3-workpaper.git
cd itr3-workpaper

# Copy skill into your working project's skills folder
mkdir -p /path/to/your-project/.claude/skills
cp -r skills/itr3-workpaper /path/to/your-project/.claude/skills/
```

Then open that project in Claude Code and ask for an ITR-3 workpaper.

### Option C — Claude Code plugin directory

This repo is also a plugin package (`.claude-plugin/plugin.json` + `skills/`):

```bash
claude --plugin-dir /path/to/itr3-workpaper
```

---

## Quick start — demo client (recommended first run)

The repo ships a **synthetic** proprietor pack: **Rohan Mehta / Mehta Trading Co.** with planted issues (AIS interest mismatch, Form 16 vs 26AS TDS, GST vs books, 40A(3) cash, missing CG cost, new regime vs 80C folder, no invented foreign assets, etc.).

### 1. Renderer-only smoke test (no LLM)

```bash
cd skills/itr3-workpaper

python3 scripts/render_output.py \
  assets/demo-client/demo_workpaper.json \
  ../../../demo-output \
  examples/rohan_mehta_efiling_draft.json
```

You should get:

```
demo-output/
├── Rohan_Mehta_itr3_workpaper.docx
├── Rohan_Mehta_itr3_workpaper.html
└── Rohan_Mehta_itr3_efiling_upload.json   # only if schema-valid
```

Open the HTML in a browser for the review dashboard.

### 2. Full agent workflow

1. Point the AI at `skills/itr3-workpaper/assets/demo-client/`.
2. **Do not** feed `_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md` as a source (it is for human QA only).
3. Prompt example:

> Prepare an ITR-3 workpaper for this client for AY 2026-27. Use the itr3-workpaper skill. Produce Word, HTML, and schema-validated e-filing JSON.

4. Compare flags to the answer key after the run.

### 3. Extract Excel/Word for the agent

```bash
python3 scripts/extract_text.py assets/demo-client/trial_balance.xlsx
python3 scripts/extract_text.py assets/demo-client/bank_interest_summary.xlsx
```

PDFs/images: use the agent’s Read tool directly (demo “PDFs” may be text placeholders for workflow testing).

---

## How to use on a real client

1. **Confirm form & year**  
   - ITR-3 applicable? (business/profession income, partner in firm, etc.)  
   - If facts clearly point to ITR-1 / ITR-2 / ITR-4 only → **stop**; do not force ITR-3.  
   - This skill is hard-scoped to **AY 2026-27**.

2. **Gather documents** (whatever mix you have):  
   Client profile/KYC, Form 16/16A, AIS/TIS, Form 26AS, bank interest, broker/CG, VDA, house property, trial balance, P&L/BS, tax depreciation register, GST summary, deduction proofs, prior-year ITR/computation, tax audit report if any.

3. **Ask the agent** to prepare the ITR-3 workpaper using this skill. It will:  
   - Map docs → schedules using `references/*`  
   - Run reconciliations  
   - Build workpaper JSON (`sections[]` + `reconciliations[]`)  
   - Build e-filing JSON (`{"ITR":{"ITR3":{...}}}`) from official field names only  
   - Run `render_output.py`

4. **CA review focus order**  
   1. All **missing** and **judgment** sections  
   2. Reconciliation **mismatches**  
   3. Regime vs Chapter VI-A  
   4. BP / depreciation / 40A(3) / 43B-style notes  
   5. Whether e-filing JSON validated  

5. **File only via** official e-filing portal / offline utility / firm software, with taxpayer authentication.  
   Schema-valid ≠ portal Category A acceptance.

### Suggested prompt

```text
Prepare an ITR-3 workpaper for AY 2026-27 from the documents in <folder>.
Tax regime: <new|old|unknown>.
Never invent figures. Flag missing data and judgment calls.
Produce docx + html + schema-validated ITR-3 e-filing JSON draft.
```

---

## Repo layout

```
itr3-workpaper/
├── README.md                          ← this guide
├── LICENSE
├── requirements.txt
├── ACCEPTANCE_TESTS.md
├── LINKEDIN_POST.md
├── itr3-workpaper-skill.zip           ← uploadable skill package
├── .claude-plugin/
│   └── plugin.json                    ← Claude Code plugin manifest
└── skills/
    └── itr3-workpaper/
        ├── SKILL.md                   ← agent entry point (workflow)
        ├── references/
        │   ├── form-applicability-and-cover.md
        │   ├── schedules-income-heads.md
        │   ├── schedules-business-bs-pl.md
        │   ├── schedules-deductions-and-ti.md
        │   ├── schedules-tds-tcs-taxes-paid.md
        │   ├── schedules-special.md
        │   ├── thresholds-ay2026-27.md      ← numeric authority
        │   ├── workpaper_schema.md
        │   ├── reconciliation-rules.md
        │   └── schema/
        │       ├── schema_ITR3.json         ← official Main V1.1 (verbatim)
        │       ├── ITR3_structure.txt       ← flattened field dump
        │       ├── efiling_json_shape.md
        │       ├── validation_rules_notes.md
        │       └── minimal_valid_itr3_skeleton.json
        ├── scripts/
        │   ├── extract_text.py
        │   ├── render_output.py
        │   └── dump_schema_structure.py
        ├── assets/demo-client/              ← synthetic Rohan Mehta pack
        └── examples/                        ← sample workpaper + efiling draft
```

---

## Architecture (how the pieces fit)

```
 Client PDFs/XLSX/JSON
          │
          ▼
   Agent + SKILL.md + references/*
          │
          ├── workpaper.json   (sections + reconciliations — free-form review)
          └── efiling.json     (ITR.ITR3.* — official keys only)
          │
          ▼
   scripts/render_output.py
          │
          ├── docx + html always
          └── efiling upload JSON only if jsonschema passes
```

**Design principles (non-negotiable):**

1. Never invent facts → `missing` + notes.  
2. Judgment allowed → best guess + amber flag.  
3. N/A is affirmative, not default.  
4. Workpaper: every **canonical section id** present (even N/A).  
5. E-filing: only schema keys; omit optional schedules when N/A.  
6. Schema is law for the third file (`additionalProperties: false`).  
7. Thresholds file is numeric authority for this AY.  
8. Renderer is dumb (layout + validation only).  
9. AIS/26AS/Form 16 reconciliation is first-class.  
10. Tax regime must be explicit — never assume.

### Canonical workpaper section ids

Cover, PartA_GEN1/GEN2, PARTA_BS, Manufacturing/Trading, PARTA_PL/OI/QD, ScheduleS, ScheduleHP, ITR3ScheduleBP, depreciation family (DPM/DOA/DEP/DCG/ESR), CG/112A/115AD/VDA, OS, CYLA/BFLA/CFL, ICDS/UD, VIA_and_80s, AMT/AMTC, SI/SPI/IF/EI/PTI, IT/TDS1/TDS2/TDS3/TCS, FSI/TR/FA/AL/GST/ESOP/5A, PartB-TI, PartB_TTI, Verification.

See `references/workpaper_schema.md` and `CANONICAL_SECTIONS` in `scripts/render_output.py`.

### E-filing envelope

```json
{
  "ITR": {
    "ITR3": {
      "CreationInfo": { },
      "Form_ITR3": {
        "FormName": "ITR-3",
        "AssessmentYear": "2026",
        "SchemaVer": "Ver1.0",
        "FormVer": "Ver1.0"
      },
      "PartA_GEN1": { },
      "PartA_GEN2": { },
      "PARTA_BS": { },
      "PARTA_PL": { },
      "ITR3ScheduleBP": { },
      "ScheduleCYLA": { },
      "ScheduleBFLA": { },
      "PartB-TI": { },
      "PartB_TTI": { },
      "Verification": { }
    }
  }
}
```

Optional schedules (Salary, HP, CG, TDS, FA, …) are included only when applicable.  
Starter structure: `references/schema/minimal_valid_itr3_skeleton.json` (replace zeros with real facts — do not ship skeleton figures as client numbers).

---

## Scripts reference

### `extract_text.py`

```bash
python3 scripts/extract_text.py <file.xlsx|.xls|.docx|.csv|.txt> [more files...]
```

Dumps Excel/Word/CSV/text to stdout for the LLM. Prefer the Read tool for PDF/images.

### `render_output.py`

```bash
python3 scripts/render_output.py <workpaper.json> <output_dir> [efiling.json]
```

- Always writes docx + html.  
- If `efiling.json` is given: validates against `references/schema/schema_ITR3.json`.  
  - **Pass** → writes `<slug>_itr3_efiling_upload.json`.  
  - **Fail** → prints every JSON-path error to stderr; **does not** write e-filing file; docx/html still written.

### `dump_schema_structure.py`

```bash
python3 scripts/dump_schema_structure.py
```

Regenerates `references/schema/ITR3_structure.txt` after a schema upgrade.

---

## Official schema & validation

- **Bundled schema:** `skills/itr3-workpaper/references/schema/schema_ITR3.json`  
  Copy of ITD **ITR-3 Main V1.1** for AY 2026-27 (do not hand-author field names).
- **Hard gate for third file:** JSON Schema (Draft-04) via `jsonschema`.
- **Soft layer:** CBDT ITR-3 validation rules themes in `validation_rules_notes.md`  
  (Category A may still block a schema-valid JSON on the portal).

---

## Keeping this skill current

| When | Action |
|------|--------|
| Each Finance Act / Budget | Refresh `references/thresholds-ay2026-27.md` (slabs, TDS, limits) |
| New ITD ITR-3 schema version | Replace `schema_ITR3.json`, run `dump_schema_structure.py`, re-check every **Schema mapping:** in schedule guides |
| New CBDT validation PDF | Update `validation_rules_notes.md` |
| Regime / form decision tree changes | Update `form-applicability-and-cover.md` |

---

## Known limitations (v0.1)

- **AY hard-coded to 2026-27** — not a multi-year engine.  
- **Schema-valid ≠ portal-accepted** (Category A rules, software importers).  
- Deep BS/PL/BP e-filing trees may be incomplete-but-valid zeros when books mapping is partial — finish in official utility.  
- Demo Form 16 / financial “PDFs” are **text placeholders** for workflow tests, not binary portal downloads.  
- Rare schedules: canonical completeness + schema correctness first; prose depth can grow over time.  
- **No** password storage, portal login, or auto-filing.  
- Not a substitute for professional advice or the reviewing CA’s responsibility.

---

## Acceptance tests

See [`ACCEPTANCE_TESTS.md`](ACCEPTANCE_TESTS.md). Core checks include: structure, real ITD schema ship, renderer smoke, completeness warning, illegal e-filing key rejected, extract_text, zip layout.

---

## Professional use & disclaimer

Outputs are **workpapers and draft data-entry guides** for licensed professionals and taxpayers. The reviewing CA / authorized signatory remains fully responsible for:

- Form selection and regime election  
- Completeness and accuracy of disclosures  
- Tax computation and credits  
- Verification, authentication, and filing  

Use only with the taxpayer’s consent. Do not store client passwords in prompts, repos, or outputs.

---

## License

MIT — see [`LICENSE`](LICENSE).

The bundled **ITD JSON Schema** remains subject to the Income Tax Department’s terms for e-filing schemas. It is included for offline validation of drafts only.

---

## Author

**CA Shailesh S Wadhawaniya**  
Related work: tax-audit workpaper skill (Form 3CA/3CB-3CD), ITR CA report generator, and other CA-practice AI tools.

Issues and improvements welcome via GitHub Issues on this repository.

---

## Changelog

### 0.1.0

- Initial public release: ITR-3 AY 2026-27 workpaper skill  
- Word + HTML renderer with status + reconciliation dashboards  
- Official schema validation for e-filing draft JSON  
- Demo client (Rohan Mehta) + answer key (human QA only)  
- Schedule reference pack + thresholds + reconciliation playbook  
