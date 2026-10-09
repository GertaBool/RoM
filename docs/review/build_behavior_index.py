#!/usr/bin/env python3
"""Extract this revision's unit-role dispatch links; no engine execution.

Usage: python3 build_behavior_index.py /path/to/rise-of-mankind
This intentionally small lexical extractor validates coverage against the enum.
It records candidate branch methods, not which branch runs in a given state.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

COMMIT = "1ab4f99a76adb530f86b278390ab8139ef41cc96"
BASE = "https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/"
NATIVE = "Assets/CvGameCoreDLL/"


def strip_comments(text):
    # Preserve strings and line positions while removing C++ comments.
    pattern = r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|/\*[\s\S]*?\*/|//[^\n]*'
    return re.sub(pattern, lambda m: "\n" * m[0].count("\n")
                  if m[0].startswith(("/*", "//")) else m[0], text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("unit-role-dispatch.json"))
    args = parser.parse_args()
    head = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", "HEAD"], text=True).strip()
    if head != COMMIT:
        parser.error("This extractor's reviewed scope is pinned to " + COMMIT)
    paths = [NATIVE + "CvUnitAI.cpp", NATIVE + "CvEnums.h"]
    for path in paths:
        committed = subprocess.check_output(["git", "-C", str(args.source), "show", COMMIT + ":" + path])
        if (args.source / path).read_bytes() != committed:
            parser.error("Source file differs from the pinned revision: " + path)
    raw = (args.source / paths[0]).read_text(encoding="latin1")
    text = strip_comments(raw)
    enums = strip_comments((args.source / paths[1]).read_text(encoding="latin1"))
    enum = re.search(r"enum UnitAITypes\s*\{(.*?)\};", enums, re.S)[1]
    roles = re.findall(r"\bUNITAI_[A-Z_]+\b", enum)
    start = text.index("switch (AI_getUnitAIType())", text.index("bool CvUnitAI::AI_update()"))
    end = text.index("default:", start)
    dispatch = text[start:end]
    methods = {m[1]: text.count("\n", 0, m.start()) + 1 for m in
               re.finditer(r"^\w+ CvUnitAI::(AI_\w+)\(", text, re.M)}
    cases = list(re.finditer(r"case (UNITAI_[A-Z_]+):", dispatch))
    records = []
    for case in cases:
        offset = start + case.start()
        block = dispatch[case.end():dispatch.index("break;", case.end())]
        called = list(dict.fromkeys(re.findall(r"\b(AI_\w+)\(", block)))
        line = text.count("\n", 0, offset) + 1
        records.append({"role": case[1], "dispatch_line": line,
                        "dispatch_url": BASE + COMMIT + "/" + paths[0] + "#L" + str(line),
                        "candidate_methods": [{"method": name, "line": methods[name],
                            "url": BASE + COMMIT + "/" + paths[0] + "#L" + str(methods[name])}
                            for name in called],
                        "direct_skip": "MISSION_SKIP" in block})
    if len(records) != len(roles) or {r["role"] for r in records} != set(roles):
        raise RuntimeError("Dispatch does not cover the UnitAITypes enum exactly")
    result = {"commit": COMMIT, "scope": "Static dispatch, including conditional alternatives and shared cases",
              "role_count": len(records), "roles": records}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("Validated and indexed", len(records), "unit roles")


if __name__ == "__main__":
    main()
