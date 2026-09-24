#!/usr/bin/env python3
"""Generate paper/references.bib from data/papers.json.
Ensures bibkeys match perfectly with cited keys in LaTeX.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "papers.json"
BIB_PATH = ROOT / "paper" / "references.bib"
BIB_PATH.parent.mkdir(parents=True, exist_ok=True)


def escape_bib(text: str) -> str:
    if not text:
        return ""
    # Clean mathjax and xml escapes if present
    text = text.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    # Replace special characters for bibtex
    text = text.replace("&", r"\&").replace("%", r"\%")
    return text


def main():
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    papers = payload["papers"]

    entries = []
    for p in papers:
        bibkey = p.get("bibkey")
        if not bibkey:
            continue
        title = escape_bib(p.get("title", ""))
        authors = " and ".join(p.get("authors", ["Anonymous"]))
        year = p.get("year", 2024)
        venue = p.get("venue", "arXiv")
        aid = p.get("arxiv_id", "")
        doi = p.get("doi", "")

        entry_type = "article"
        if "arXiv" in venue or not venue:
            entry = f"""@article{{{bibkey},
  title = {{{{{title}}}}},
  author = {{{authors}}},
  journal = {{arXiv preprint arXiv:{aid}}},
  year = {{{year}}},
  doi = {{{doi}}},
  eprint = {{{aid}}},
  archivePrefix = {{arXiv}},
  primaryClass = {{cs.LG}}
}}"""
        else:
            entry = f"""@inproceedings{{{bibkey},
  title = {{{{{title}}}}},
  author = {{{authors}}},
  booktitle = {{{venue}}},
  year = {{{year}}},
  doi = {{{doi}}},
  eprint = {{{aid}}},
  archivePrefix = {{arXiv}}
}}"""
        entries.append(entry)

    BIB_PATH.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    print(f"Generated {len(entries)} BibTeX entries in {BIB_PATH}")


if __name__ == "__main__":
    main()
