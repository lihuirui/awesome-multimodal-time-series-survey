.PHONY: search figures bib readme paper check all clean help

PYTHON ?= python3
TECTONIC ?= tectonic

help:
	@echo "Available Makefile targets:"
	@echo "  make search   - Run systematic search and screening script"
	@echo "  make figures  - Generate all high-res publication figures (PNG & PDF)"
	@echo "  make bib      - Generate paper/references.bib from data/papers.json"
	@echo "  make readme   - Auto-generate bilingual README.md from data/papers.json"
	@echo "  make paper    - Compile paper/main.tex into paper/main.pdf via tectonic"
	@echo "  make check    - Run rigorous quality gates check (COMMON_METHOD.md G)"
	@echo "  make all      - Run full end-to-end pipeline and verify quality gates"
	@echo "  make clean    - Remove intermediate build artifacts"

search:
	$(PYTHON) scripts/search_and_verify.py

figures:
	$(PYTHON) scripts/generate_figures.py

bib:
	$(PYTHON) scripts/generate_bib.py

readme:
	$(PYTHON) scripts/generate_readme.py

paper: bib figures
	$(TECTONIC) paper/main.tex

check:
	$(PYTHON) scripts/check_gates.py

all: search bib figures readme paper check
	@echo "=== Pipeline Completed Successfully ==="

clean:
	rm -f paper/*.aux paper/*.log paper/*.out paper/*.toc paper/*.fls paper/*.fdb_latexmk
