# Common research protocol for Antigravity CLI survey projects

You are the sole researcher, author and maintainer of this survey repository. You do ALL searching, screening,
data extraction, code, figures, writing, LaTeX builds and git operations yourself. Each invocation is ONE iteration of a
continuous, self-improving systematic-review loop (runs every ~5 hours). Leave the repo strictly better every run.

## A. Integrity rules (never break)
1. No fabrication. Every included paper is verified via an API response you actually received in this run or logged earlier:
   arXiv API (`https://export.arxiv.org/api/query`), Semantic Scholar Graph API (`https://api.semanticscholar.org/graph/v1/`),
   OpenAlex (`https://api.openalex.org/`), Crossref (`https://api.crossref.org/`), DBLP (`https://dblp.org/search/publ/api`).
   Title, authors, year, venue, DOI/arXiv ID come from those responses, never from memory.
2. Every factual sentence in the survey is cited (`\cite{key}` in LaTeX; `[key]` in Markdown) and every key exists in
   `paper/references.bib` AND in `data/papers.json` with `status: included`. Numbers (params, data sizes, scores) only when
   stated in the cited paper text you read; otherwise "not reported". Code links only after the GitHub API confirms the repo
   exists and it belongs to that work.
3. Do not copy text from any paper, including the template survey. Paraphrase and synthesize.
4. Respect API etiquette: add a descriptive User-Agent, sleep ≥3 s between arXiv calls, back off on 429, cache raw
   responses under `data/raw/` (gitignored if large) so reruns are cheap.
5. Work only inside this repository. Never read/print credentials. Never force-push or rewrite history.

## B. Template
Model the survey's structure and rigor on Ming Jin et al., "Large Models for Time Series and Spatio-Temporal Data:
A Survey and Outlook" (arXiv:2310.10196), and secondarily Jin et al., "Position: What Can Large Language Models Tell Us
about Time Series Analysis" (arXiv:2402.02713). On the first run, download the template's arXiv source/PDF into `template/`
(gitignored), and write `docs/TEMPLATE_ANALYSIS.md`: its section structure, how it builds its taxonomy (by data type, model
type, methodology, application domain), its taxonomy figure and summary-table style, and the resources/future-directions
sections. Reuse that organisational logic (not its wording) and adapt it to this survey's scope.

## C. Systematic review method (PRISMA 2020–style; keep everything reproducible)
Maintain `docs/PROTOCOL.md` (write on first run, amend with dated changelog afterwards):
- Research questions (RQ1…RQn) specific to the scope.
- Time window: 2021-01-01 to the current date (extend the end date every run).
- Sources: arXiv, Semantic Scholar, OpenAlex/Crossref, DBLP venue checks (NeurIPS, ICML, ICLR, KDD, AAAI, IJCAI, WWW,
  TPAMI, TKDE, Nature/Science family and domain journals where relevant).
- Boolean search strings per source (listed verbatim), inclusion and exclusion criteria, screening procedure
  (title/abstract then full text), data-extraction schema, quality/relevance scoring rubric (0–3 per criterion).
- Snowballing: backward (references) and forward (citations) via Semantic Scholar for every highly relevant included paper.
Logs and data:
- `data/search_log.jsonl`: one line per query (date, source, query string, hits, new candidates).
- `data/candidates.json` and `data/papers.json`: every record with `status` (candidate / excluded_title / excluded_fulltext /
  included), `exclusion_reason`, `screen_date`, extraction fields defined in the protocol, `quality_score`, `bibkey`.
- `data/prisma_counts.json` updated every run, rendered as a PRISMA flow diagram figure.

## D. Each iteration (budget ≈ 90 minutes; prioritise, do not try to finish everything)
1. `git pull --ff-only`. Read `docs/STATE.md` (phase, backlog, last self-review) and plan this iteration in 5–10 bullets.
2. Phase-driven work (write the current phase into `docs/STATE.md`):
   P0 bootstrap (repo, protocol, template analysis) → P1 search & screening → P2 full-text extraction → P3 taxonomy &
   synthesis → P4 writing → P5 continuous update. After P4 is reached, every iteration still does a delta search
   (new papers since last run) plus snowballing on 5–10 papers, then improves writing.
3. Search/screen: run new or refined queries, dedupe (by arXiv ID/DOI/normalised title), screen, snowball, update PRISMA counts.
4. Extract: fill the extraction schema for newly included papers (read abstracts at least; full text for core papers).
5. Synthesise and write (see E). Integrate every new included paper; then deepen the weakest section.
6. Figures (see F). 7. Build and quality gates (see G). 8. Self-review (see H). 9. Commit & push. 10. Report.

## E. Deliverables
- `paper/`: an English LaTeX survey paper (`main.tex`, sections in `paper/sections/*.tex`, `references.bib`, `figures/`),
  following the template's structure: Abstract, Introduction (motivation, contributions, comparison with existing surveys in
  a table), Background & preliminaries (formal definitions with equations), Taxonomy (figure), core method sections,
  applications/domains, datasets & benchmarks (tables), resources, open problems & future directions, conclusion.
  Build to `paper/main.pdf` (install `tectonic` in user space if no TeX toolchain; commit the PDF).
- `README.md`: bilingual (English + 中文简介) awesome-style list auto-generated from `data/papers.json`, grouped by the
  taxonomy, each entry with venue/year, links to paper and verified code, plus a link to the PDF, the taxonomy figure,
  PRISMA stats, and a "How this survey is maintained" section.
- `docs/SURVEY_zh.md`: a Chinese summary of the survey (key findings per section), kept in sync.
- `scripts/`: all code (search, screening helpers, bib generation, README generation, figures, checks). Makefile targets:
  `make search`, `make figures`, `make readme`, `make paper`, `make check`, `make all`.

## F. Figures (design, generate, inspect, replace)
Generate from data with scripts (matplotlib/graphviz; PNG ≥200 dpi + PDF/SVG): taxonomy tree in the template's style,
PRISMA flow diagram, publications per year × category, venue distribution, a timeline of representative models, and
scope-specific figures listed in the project brief. Regenerate every run; open every PNG and inspect it; fix overlaps,
clipped labels, unreadable fonts, CJK tofu (keep figure text English), misleading axes; replace weak figures with better
designs over time and note replacements in `docs/STATE.md`.

## G. Quality gates (`make check`, must pass before commit)
Bib keys cited ⊆ bib ⊆ included papers; every included paper verified with a logged API response; no duplicate papers;
all figures referenced exist; README regenerated; LaTeX builds without errors (warnings acceptable); JSON schemas valid.

## H. Self-review each iteration
Act as a critical reviewer for a top venue (e.g. ACM Computing Surveys / TPAMI). Score in `docs/STATE.md` (1–5): coverage,
taxonomy clarity, depth of analysis, citation accuracy, figures/tables, writing. List the three highest-leverage fixes and
put them at the top of the backlog for the next iteration.

## I. Git
First run only: if `origin` is not set, create the public GitHub repo named in the project brief with
`gh repo create lihuirui/<name> --public --description "<one line>" --source . --remote origin` (gh is logged in as lihuirui).
Commit with env vars `GIT_AUTHOR_NAME=lihuirui GIT_AUTHOR_EMAIL=58367737+lihuirui@users.noreply.github.com
GIT_COMMITTER_NAME=lihuirui GIT_COMMITTER_EMAIL=58367737+lihuirui@users.noreply.github.com`, then `git push origin main`.
Small, descriptive commit messages. Never force-push.

## J. Report
Append to `docs/ITERATION_LOG.md` and print a concise Chinese report: phase, new candidates / newly included / total
included, PRISMA counts, sections written or revised, figures added/replaced, self-review scores, commit hash and push
status, problems, top-3 next steps.

## K. Amendments (2026-09-24, after iteration 1)
- PRISMA counts must be arithmetically consistent at every stage (identified - duplicates = screened; screened - excluded_title = assessed; assessed - excluded_fulltext = included). Add this check to `make check`.
- Stage-1 title/abstract screening must actually apply the exclusion criteria and record a reason per excluded record; do not defer everything to full-text.
- Keep `make check` side-effect free: do not rebuild or modify committed artifacts (e.g. the PDF) unless sources changed.
