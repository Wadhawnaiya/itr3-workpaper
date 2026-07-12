# LinkedIn Post — ITR-3 Workpaper Skill

Copy everything below the line and paste directly into LinkedIn.

---

🚀 I just built a complete professional ITR-3 Workpaper skill for AI tools — for Assessment Year 2026-27.

If you're a CA or tax professional doing first-pass drafting for business individuals / HUFs (proprietor, partner, books + Form 16 + AIS), this can save your junior team a lot of first-pass data entry time.

What it does:
→ Takes the client's raw source documents (Form 16, AIS/TIS, Form 26AS, trial balance, financials, capital gains, house property, deduction proofs, GST summary, bank interest, etc.)
→ Automatically creates a review-ready package containing:
   • Schedule-by-schedule ITR-3 workpaper (Word)
   • Color-coded HTML review dashboard (filled / judgment / missing / N/A)
   • AIS–26AS–Form 16–books reconciliation dashboard
   • Schema-validated ITR-3 e-filing draft JSON (ITD Main V1.1)

Important: it never invents figures, never files on the portal, and never replaces CA judgment. Every output is labeled draft — for CA / taxpayer review before filing.

Works excellently with:
• Claude (Claude Code / Claude Desktop Skills)
• Grok
• Other AI coding agents that support Agent Skills

How easy is it?

1. Clone the repo:
   git clone https://github.com/Wadhawnaiya/itr3-workpaper.git

2. Install dependency:
   pip install -r requirements.txt

3. Install the skill (zip upload in Claude Skills, or copy `skills/itr3-workpaper` into `.claude/skills/`), then point the AI at the client folder and say:
   "Prepare an ITR-3 workpaper for this client for AY 2026-27."

Or try the built-in demo client (Rohan Mehta — synthetic proprietor pack with planted mismatches) and run:

```
cd skills/itr3-workpaper
python3 scripts/render_output.py assets/demo-client/demo_workpaper.json ./output examples/rohan_mehta_efiling_draft.json
```

You get three files:
• `*_itr3_workpaper.docx`
• `*_itr3_workpaper.html`
• `*_itr3_efiling_upload.json` (only if it passes the official schema)

🔗 GitHub: https://github.com/Wadhawnaiya/itr3-workpaper

Completely free and open source (MIT license).

This is the same architecture as my tax-audit workpaper skill (Form 3CA/3CB-3CD) — now for pre-filing ITR-3.

Fellow Chartered Accountants — are you already using Claude / Cursor / Grok skills for ITR first-pass workpapers in your firm?

Would love to know your experience.

#CA #CharteredAccountant #ITR #ITR3 #Tax #IncomeTax #TaxSeason #ClaudeAI #Grok #AItools #Automation #Productivity #eFiling

---

## Short Alternative Version:

🚀 Just built an ITR-3 Workpaper skill for AY 2026-27.

Give it the client's Form 16 + AIS + 26AS + TB + CG + HP + proofs → it generates a schedule-by-schedule Word + HTML workpaper, an AIS reconciliation dashboard, and a schema-validated ITR-3 e-filing draft JSON.

Does not file. Does not invent numbers. Built for CA-firm first pass + CA review.

Works with Claude Code / Claude Desktop Skills, Grok, and similar AI agents.

Useful for CAs handling business returns this season?

#CA #ITR3 #ClaudeAI #Automation #Tax
