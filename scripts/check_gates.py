#!/usr/bin/env python3
"""Quality gates validation script for Multimodal Time Series Survey.

Enforces Section G of COMMON_METHOD.md:
1. JSON schemas valid
2. No duplicate papers
3. Every included paper verified with a logged API response in data/raw/
4. Bib keys cited ⊆ bib ⊆ included papers
5. All figures referenced exist
6. README up to date
7. LaTeX paper/main.pdf exists and non-empty
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PAPERS_PATH = DATA_DIR / "papers.json"
CANDIDATES_PATH = DATA_DIR / "candidates.json"
PRISMA_PATH = DATA_DIR / "prisma_counts.json"
RAW_DIR = DATA_DIR / "raw"
PAPER_DIR = ROOT / "paper"
BIB_PATH = PAPER_DIR / "references.bib"
MAIN_PDF = PAPER_DIR / "main.pdf"
README_PATH = ROOT / "README.md"


def check_gate(name: str, passed: bool, detail: str = ""):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"[{status}] {name}")
    if detail:
        print(f"       -> {detail}")
    if not passed:
        sys.exit(1)


def main():
    print("==================================================")
    print(" Running Quality Gates Check (COMMON_METHOD.md G) ")
    print("==================================================")

    # 1. JSON Schemas Valid
    try:
        papers_data = json.loads(PAPERS_PATH.read_text(encoding="utf-8"))
        candidates_data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
        prisma_data = json.loads(PRISMA_PATH.read_text(encoding="utf-8"))
        assert "papers" in papers_data and isinstance(papers_data["papers"], list)
        assert "candidates" in candidates_data and isinstance(candidates_data["candidates"], list)
        assert "included" in prisma_data and "screening" in prisma_data
        check_gate("JSON Schemas Valid", True, f"{len(papers_data['papers'])} papers, {len(candidates_data['candidates'])} candidates")
    except Exception as e:
        check_gate("JSON Schemas Valid", False, str(e))

    # 1b. PRISMA Arithmetic Consistency (COMMON_METHOD.md Amendment K)
    try:
        ident = prisma_data["identification"]["total_identified"]
        dups = prisma_data["screening"]["duplicates_removed"]
        screened = prisma_data["screening"]["records_after_dedup"]
        excl_title = prisma_data["screening"]["excluded_title_abstract"]
        assessed = prisma_data["screening"]["fulltext_assessed"]
        excl_full = prisma_data["screening"]["excluded_fulltext"]
        incl = prisma_data["included"]["qualitative_synthesis"]

        assert ident - dups == screened, f"PRISMA error: identified ({ident}) - duplicates ({dups}) != screened ({screened})"
        assert screened - excl_title == assessed, f"PRISMA error: screened ({screened}) - excluded_title ({excl_title}) != assessed ({assessed})"
        assert assessed - excl_full == incl, f"PRISMA error: assessed ({assessed}) - excluded_fulltext ({excl_full}) != included ({incl})"
        assert incl == len(papers_data["papers"]), f"PRISMA error: included ({incl}) != papers.json count ({len(papers_data['papers'])})"
        check_gate("PRISMA Arithmetic Consistency (Amendment K)", True,
                   f"{ident} - {dups} = {screened} | {screened} - {excl_title} = {assessed} | {assessed} - {excl_full} = {incl} = {len(papers_data['papers'])}")
    except Exception as e:
        check_gate("PRISMA Arithmetic Consistency (Amendment K)", False, str(e))

    papers = papers_data["papers"]

    # 2. No Duplicate Papers
    seen_ids = set()
    seen_keys = set()
    duplicates = []
    for p in papers:
        aid = p.get("arxiv_id")
        key = p.get("bibkey")
        if aid and aid in seen_ids:
            duplicates.append(f"Duplicate arxiv_id: {aid}")
        if key and key in seen_keys:
            duplicates.append(f"Duplicate bibkey: {key}")
        if aid:
            seen_ids.add(aid)
        if key:
            seen_keys.add(key)
    check_gate("No Duplicate Papers", len(duplicates) == 0, ", ".join(duplicates) if duplicates else "All IDs and bibkeys unique")

    # 3. Every Included Paper Verified with Logged API Response
    unverified = []
    missing_raw = []
    for p in papers:
        if not p.get("api_verified"):
            unverified.append(p.get("bibkey", "unknown"))
        aid = p.get("arxiv_id")
        raw_file = RAW_DIR / f"arxiv_{aid}.html"
        if not raw_file.exists():
            missing_raw.append(aid)
    check_gate("Included Papers API-Verified", len(unverified) == 0 and len(missing_raw) == 0,
               f"Unverified: {len(unverified)}, Missing Raw Cache: {len(missing_raw)}")

    # 4. Parse BibTeX Keys
    bib_content = BIB_PATH.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@(?:article|inproceedings|misc)\{([^,]+),", bib_content))
    included_bibkeys = {p["bibkey"] for p in papers if p.get("bibkey")}

    # bib ⊆ included papers
    bib_in_included = bib_keys.issubset(included_bibkeys)
    check_gate("Bib Keys Subset of Included Papers (bib ⊆ included)", bib_in_included,
               f"Bib keys: {len(bib_keys)}, Included keys: {len(included_bibkeys)}")

    # 5. Parse Cited Keys in LaTeX
    tex_files = list(PAPER_DIR.glob("*.tex")) + list((PAPER_DIR / "sections").glob("*.tex"))
    cited_keys = set()
    for tf in tex_files:
        content = tf.read_text(encoding="utf-8")
        # Extract \cite{k1,k2}
        citations = re.findall(r"\\cite\{([^}]+)\}", content)
        for c in citations:
            for k in c.split(","):
                k = k.strip()
                if k:
                    cited_keys.add(k)

    # cited ⊆ bib
    cited_in_bib = cited_keys.issubset(bib_keys)
    missing_cited = cited_keys - bib_keys
    check_gate("Cited Keys in LaTeX Subset of Bib (cited ⊆ bib)", cited_in_bib,
               f"Missing in bib: {missing_cited}" if missing_cited else f"{len(cited_keys)} cited keys all resolved")

    # 6. Referenced Figures Exist
    referenced_figs = set()
    for tf in tex_files:
        content = tf.read_text(encoding="utf-8")
        figs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", content)
        for f in figs:
            referenced_figs.add(f.strip())

    missing_figs = []
    for rf in referenced_figs:
        # Check relative to paper/
        fig_path = PAPER_DIR / rf
        if not fig_path.exists():
            # Check with extensions
            found = False
            for ext in [".png", ".pdf", ".jpg"]:
                if (PAPER_DIR / f"{rf}{ext}").exists():
                    found = True
                    break
            if not found:
                missing_figs.append(rf)
    check_gate("Referenced Figures Exist", len(missing_figs) == 0,
               f"Missing figures: {missing_figs}" if missing_figs else f"{len(referenced_figs)} figures all exist")

    # 7. README Regenerated & Formatted
    readme_text = README_PATH.read_text(encoding="utf-8")
    assert "Taxonomy of Multimodal Time Series Models" in readme_text
    assert "PRISMA 2020 Systematic Review Counts" in readme_text
    assert "How This Survey is Maintained" in readme_text
    check_gate("README.md Valid and Formatted", True, f"Length: {len(readme_text)} chars")

    # 8. LaTeX Compiled PDF Exists
    pdf_exists = MAIN_PDF.exists() and MAIN_PDF.stat().st_size > 100000
    check_gate("LaTeX PDF Build (paper/main.pdf)", pdf_exists,
               f"Size: {MAIN_PDF.stat().st_size / 1024 / 1024:.2f} MB" if pdf_exists else "PDF missing or too small")

    print("==================================================")
    print(" ALL QUALITY GATES PASSED SUCCESSFULLY!           ")
    print("==================================================")


if __name__ == "__main__":
    main()
