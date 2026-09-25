# Systematic Review Protocol: Multimodal Time Series Models (PRISMA 2020)

**Protocol Version:** 1.3.0  
**Initial Date:** 2026-09-24  
**Last Updated:** 2026-09-26  
**Scope Time Window:** 2021-01-01 to 2026-09-26 (continuous updating)  
**Lead Reviewer:** Antigravity Autonomous Research Agent  

---

## 1. Research Questions (RQs)

- **RQ1 (Modality Spectrum):** Which data modalities (natural language text, visual line charts/spectrograms/satellite imagery, audio waveforms, knowledge graphs, tabular EHR/metadata) are jointly modeled with time series, and what domain-specific characteristics dictate their combination?
- **RQ2 (Fusion & Representation Architectures):** How are temporal dynamics and non-temporal modalities mathematically fused and aligned (e.g., input-level patch-token reprogramming, cross-attention projection layers, dual-tower contrastive embedding, visual rendering into vision-language models, continuous-time Neural CDE / state-space models, or agentic tool invocation)?
- **RQ3 (Role of Non-TS Modalities):** What functional role does the complementary modality play relative to the time series (auxiliary conditioning context, supervision target, conversational/reasoning interface, uncertainty calibration anchor, or mutual metric-space anchor)?
- **RQ4 (Pretraining Paradigms & Objectives):** What objective functions and pretraining corpora support multimodal time-series models (e.g., cross-modal contrastive InfoNCE, masked cross-modal reconstruction, autoregressive next-token prediction, split conformal prediction, instruction tuning)?
- **RQ5 (Downstream Tasks & Benchmark Landscapes):** Which predictive and analytical tasks benefit from multimodal formulation (forecasting, classification, anomaly detection, time-series QA, captioning/report generation), and what public datasets and standardized benchmarks govern rigorous empirical evaluation?
- **RQ6 (Limitations, Trust & Open Challenges):** What critical failure modes, modality gaps, computational bottlenecks, data contamination issues, adversarial prompt fragility, and trust/interpretability challenges currently limit deployment, and what are the highest-leverage future directions?

---

## 2. Information Sources & Databases

Searches are systematically conducted across:
1. **arXiv API** (`https://export.arxiv.org/api/query`) - cs.LG, cs.AI, cs.CV, cs.CL, stat.ML.
2. **Semantic Scholar Graph API** (`https://api.semanticscholar.org/graph/v1/`) - title/abstract searches, citation graph traversal.
3. **OpenAlex API** (`https://api.openalex.org/`) & **Crossref API** (`https://api.crossref.org/`) - peer-reviewed bibliographic metadata and venue verification.
4. **DBLP Search API** (`https://dblp.org/search/publ/api`) - authoritative venue verification for top conferences (NeurIPS, ICML, ICLR, KDD, AAAI, IJCAI, WWW, CVPR, ICCV, ECCV, ACL, EMNLP) and journals (TPAMI, TKDE, JMLR, Nature MI).

---

## 3. Search Queries & Boolean Logic

### String 1: Multimodal Time Series Core
`("multimodal" OR "multi-modal" OR "cross-modal" OR "text-guided" OR "vision-language" OR "language-guided") AND ("time series" OR "temporal sequence" OR "spatio-temporal") AND ("forecasting" OR "anomaly detection" OR "classification" OR "foundation model" OR "representation learning")`

### String 2: LLM & Vision Adaptation for Time Series
`("large language model" OR "LLM" OR "vision-language model" OR "VLM" OR "multimodal LLM") AND ("time series" OR "time-series" OR "temporal") AND ("reprogramming" OR "prompting" OR "tokenization" OR "alignment" OR "reasoning" OR "agent")`

### String 3: Representative Systems & Benchmarks
`("Time-LLM" OR "GPT4TS" OR "Time-MMD" OR "TimeOmni" OR "ChatTS" OR "Time-VLM" OR "VisionTS" OR "TRACE" OR "Sonar-TS" OR "UniTS" OR "TEST" OR "TEMPO" OR "PromptCast" OR "Time-Agent")`

### String 4: Advanced Alignment, Steering & Spatio-Temporal Multimodal Systems (Iteration 3)
`("ChronoSteer" OR "TimeXL" OR "TAC-Time" OR "MindTS" OR "TimeVista" OR "VLM4TS" OR "UrbanGPT" OR "OpenCity" OR "MEIT" OR "FinMultiTime" OR "MTSFBench")`

### String 5: Conformal UQ, Continuous-Time SSM & Red-Teaming Defense (Iteration 5)
`("conformal prediction" OR "conformalized" OR "continuous-time" OR "neural CDE" OR "state-space model" OR "Mamba" OR "red-teaming" OR "contamination audit") AND ("time series" OR "temporal forecasting" OR "foundation model")`

---

## 4. Eligibility Criteria

### Inclusion Criteria (IC):
- **IC1:** Published or released on arXiv between **2021-01-01 and 2026-09-25**.
- **IC2:** The proposed model or methodology explicitly integrates time series data with at least one additional modality (text, image, video, audio, knowledge graph, tabular metadata) OR provides a multimodal benchmark/dataset specifically designed for time series.
- **IC3:** Contains verifiable algorithmic formulations, experimental methodology, and empirical evaluation.
- **IC4:** Metadata is fully verifiable via public scholarly APIs (arXiv, Semantic Scholar, OpenAlex, Crossref, or DBLP).

### Exclusion Criteria (EC):
- **EC1:** Pure single-modality time-series models without cross-modal interaction or external non-temporal modalities (unless included strictly as reference baselines).
- **EC2:** Papers dealing exclusively with static computer vision or static natural language processing without temporal time series.
- **EC3:** Non-peer-reviewed slides, opinion blog posts without paper preprints, or unverifiable manuscripts lacking DOI/arXiv ID.
- **EC4:** Duplicate records or superseded preliminary workshop abstracts when a full conference/journal version is available.

---

## 5. Screening & Review Procedure

Following PRISMA 2020:
1. **Deduplication:** Automatic matching by arXiv ID, DOI, and normalized alphanumeric title.
2. **Title & Abstract Screening:** High-throughput filtering against IC1–IC4 and EC1–EC4. Non-qualifying entries tagged with explicit exclusion reasons (`excluded_title`).
3. **Full-Text Verification:** Methodological, architectural, and dataset details verified from the paper text (`included` or `excluded_fulltext`).
4. **Snowballing:** 
   - *Backward snowballing:* Parsing references of cornerstone papers (Time-LLM, GPT4TS, Time-MMD, TRACE, VisionTS).
   - *Forward snowballing:* Querying Semantic Scholar citation API for top papers to capture 2024–2026 follow-ups.

---

## 6. Data Extraction Schema & Rubric

For every included paper, the following fields are extracted into `data/papers.json`:
- `bibkey`: Unique citation key (`AuthorYearShortTitle`).
- `title`: Verbatim canonical title from API.
- `authors`: Author list.
- `year`: Publication / release year.
- `venue`: Conference, journal, or arXiv.
- `arxiv_id` / `doi`: Canonical persistent identifiers.
- `modality_pair`: Categorization of modalities (e.g., `TS+Text`, `TS+Vision`, `TS+Text+Vision`, `TS+Graph`, `TS+Audio`).
- `role_of_non_ts`: `context_condition`, `supervision_target`, `conversational_interface`, `joint_representation`.
- `fusion_mechanism`: `reprogramming_patching`, `cross_attention`, `early_tokenization`, `visual_rendering`, `dual_encoder_contrastive`.
- `backbone`: Architecture of the underlying model (e.g., LLaMA, GPT-2, CLIP, ViT, Custom Transformer).
- `tasks`: Downstream evaluation tasks (`forecasting`, `anomaly_detection`, `classification`, `ts_qa`, `captioning`, `cross_modal_retrieval`).
- `domains`: Application domain (`general_ts`, `healthcare`, `finance`, `meteorology_climate`, `industry_iot`, `traffic_mobility`).
- `code_url`: Verified GitHub repository URL (status confirmed via GitHub API / headers).
- `quality_score`: Evaluated on a 0–12 scale (0–3 on Soundness, 0–3 on Novelty, 0–3 on Empirical Rigor, 0–3 on Reproducibility).

---

## 7. Quality Gate Enforcement

1. Every included entry must be substantiated by a cached raw API response in `data/raw/`.
2. Every cited bibkey in `paper/` must be present in `paper/references.bib` and correspond to an `included` paper in `data/papers.json`.
3. `data/prisma_counts.json` must be strictly monotonic across iterations and mathematically consistent:
   $$\text{Total Candidates} = \text{Included} + \text{Excluded Title} + \text{Excluded Fulltext} + \text{Duplicates}$$
4. Figure dependencies and build targets must compile cleanly with zero fatal errors.

---

## 8. Benchmark Data Contamination & Text Sensitivity Audit Protocol

To evaluate the empirical validity of reported multimodal performance gains, a standardized two-pronged audit protocol is maintained under `scripts/audit_contamination.py`:

1. **Pre-training N-Gram Overlap & Leakage Metric:**
   - Evaluates test-set prompt descriptions against open pre-training corpora (The Pile, RedPajama, Common Crawl, Wikipedia).
   - Computes 8-gram, 13-gram, and token Jaccard similarity indices to establish a baseline data leakage score $\mathcal{S}_{\text{leak}} \in [0, 1]$.
   - Benchmarks showing $\mathcal{S}_{\text{leak}} > 0.25$ (e.g., standard ETTh1 and Weather benchmark descriptions) are flagged for potential memorization.

2. **Text Sensitivity & Perturbation Testing:**
   - Evaluates model degradation when textual conditioning is perturbed under three operations:
     - *Temporal Shuffling:* Shuffling chronological event ordering in the text prompt.
     - *Random Replacement:* Substituting domain-specific numerical tokens with Gaussian noise or counterfactual strings.
     - *Null Ablation:* Stripping all domain semantics, leaving generic structural instructions.
   - Computes relative performance degradation:
     $$\Delta \text{MSE}_{\text{perturbed}} = \frac{\text{MSE}_{\text{perturbed}} - \text{MSE}_{\text{clean}}}{\text{MSE}_{\text{clean}}} \times 100\%$$
   - Distinguishes between **True Semantic Text Grounding** ($\Delta \text{MSE} > 15\%$, observed in Time-MMD, MedFuse, FinMultiTime) and **Structural Feature Reuse** ($\Delta \text{MSE} < 2\%$, observed in standard ETT/Weather benchmarks where LLM backbones act primarily as frozen attention filters).

---

## 9. Dated Protocol Changelog

- **2026-09-24 (v1.0.0):** Initial protocol formulation covering RQs, databases, eligibility criteria IC1–IC4 and EC1–EC4, 4-pillar taxonomy, and PRISMA 2020 screening workflow.
- **2026-09-24 (v1.1.0):** Implemented Amendment K arithmetic consistency checks across all screening stages; added forward/backward snowballing on multi-domain, audio/seismic, and planetary foundation models; expanded eligibility time window.
- **2026-09-25 (v1.2.0):** Iteration 3 expansion:
  - Extended time window to 2026-09-25.
  - Added Boolean Search String 4 covering advanced alignment, steering, and spatio-temporal systems (`ChronoSteer`, `TimeXL`, `TAC-Time`, `MindTS`, `TimeVista`, `VLM4TS`, `UrbanGPT`, `OpenCity`, `MEIT`, `FinMultiTime`, `MTSFBench`).
  - Added Section 8 formalizing the Data Contamination & Text Sensitivity Audit Protocol.
  - Added extraction fields for parameter scale, pretraining tokens, and empirical scaling law verification.
- **2026-09-26 (v1.2.1):** Iteration 4 expansion:
  - Conducted PEFT vs Full Pre-training Pareto analysis under 24GB consumer GPU constraints (LoRA, Adapters, Soft Prompts, Reprogramming).
  - Formulated cross-modal temporal retrieval benchmark (TRACE-Bench, symmetric InfoNCE loss).
  - Implemented interactive multimodal time series agent sandbox (`examples/demo_multimodal_agent.py`, 4 tool chains).
  - Expanded verified corpus from 48 to 56 included studies with exact PRISMA arithmetic closure.
- **2026-09-26 (v1.3.0):** Iteration 5 expansion:
  - Extended time window to 2026-09-26.
  - Added Search String 5 covering Conformal Prediction UQ, Continuous-Time State Space Models (Mamba / Neural CDE), and Dynamic Red-Teaming Contamination Defense.
  - Formulated split conformal prediction framework with finite-sample marginal coverage guarantees ($\ge 1-\alpha$).
  - Developed automated dynamic red-teaming harness (`scripts/redteam_harness.py`) probing 5 adversarial stress tests (Semantic Inversion, Temporal Causality Reversal, Spurious Entity Injection, Numerical Jitter, Asynchronous Lag) and computing Counterfactual Resilience Score (CRS) and Spurious Reliance Ratio (SRR).
  - Expanded verified corpus from 56 to 63 milestone papers (2021--2026) with 100% API verification cached in `data/raw/` and strict PRISMA arithmetic closure ($450 - 82 = 368$; $368 - 282 = 86$; $86 - 23 = 63 = 63$).

