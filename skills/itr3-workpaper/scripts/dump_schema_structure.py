#!/usr/bin/env python3
"""
Flatten schema_ITR3.json into a human-readable ITR3_structure.txt.

Usage:
    python3 dump_schema_structure.py [schema_path] [out_path]
"""
import json
import sys
import os

DEFAULT_SCHEMA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "references",
    "schema",
    "schema_ITR3.json",
)
DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "references",
    "schema",
    "ITR3_structure.txt",
)

MAJOR = [
    "CreationInfo",
    "Form_ITR3",
    "PartA_GEN1",
    "PartA_GEN2",
    "PARTA_BS",
    "PARTA_PL",
    "ITR3ScheduleBP",
    "ScheduleCYLA",
    "ScheduleBFLA",
    "PartB-TI",
    "PartB_TTI",
    "Verification",
    "ScheduleS",
    "ScheduleHP",
    "ScheduleCGFor23",
    "ScheduleOS",
    "ScheduleVIA",
    "ScheduleIT",
    "ScheduleTDS1",
    "ScheduleTDS2",
    "ScheduleTDS3",
    "ScheduleTCS",
    "ScheduleFA",
    "ScheduleAL",
    "ScheduleGST",
]


def dump_def(defs, name, out, indent=0, seen=None, max_depth=2):
    if seen is None:
        seen = set()
    if name not in defs or indent > max_depth:
        return
    if name in seen and indent > 0:
        return
    seen.add(name)
    n = defs[name]
    if not isinstance(n, dict):
        return
    props = n.get("properties", {})
    req = set(n.get("required", []))
    out.append("  " * indent + f"[{name}] required={sorted(req)}")
    for pk, pv in props.items():
        mark = "*" if pk in req else " "
        ref = None
        t = ""
        pat = ""
        if isinstance(pv, dict):
            if "$ref" in pv:
                ref = pv["$ref"].split("/")[-1]
            elif "items" in pv and isinstance(pv["items"], dict) and "$ref" in pv["items"]:
                ref = pv["items"]["$ref"].split("/")[-1] + "[]"
            t = pv.get("type") or (
                "enum:" + str(pv.get("enum")) if "enum" in pv else ""
            )
            pat = pv.get("pattern", "")
        out.append(
            "  " * (indent + 1)
            + f"{mark} {pk}: {t or ref or '?'} {('pattern=' + pat) if pat else ''}"
        )
        if ref and not ref.endswith("[]") and indent < max_depth:
            dump_def(defs, ref, out, indent + 2, seen, max_depth)


def main():
    schema_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SCHEMA
    out_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    defs = schema["definitions"]
    lines = [
        "ITR-3 Main V1.1 — flattened structure dump (major nodes)",
        f"Source: {os.path.basename(schema_path)}",
        "=" * 72,
        "",
        "## Root",
        "properties.ITR -> definitions.ITR -> ITR3",
    ]
    dump_def(defs, "ITR3", lines, 0, set(), 2)
    for major in MAJOR:
        lines.append(f"\n## {major}")
        dump_def(defs, major, lines, 0, set(), 2)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
