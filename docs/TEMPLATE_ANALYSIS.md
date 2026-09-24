# Template Analysis: Structural & Methodological Dissection

This document analyzes the reference template papers:
1. **Primary Template:** Ming Jin et al., *"Large Models for Time Series and Spatio-Temporal Data: A Survey and Outlook"*, arXiv:2310.10196 (2023).
2. **Secondary Template:** Ming Jin et al., *"Position: What Can Large Language Models Tell Us about Time Series Analysis"*, arXiv:2402.02713 (2024).

---

## 1. Primary Template Architecture (arXiv:2310.10196)

### 1.1 Section Hierarchy & Organization
- **Abstract:** Concise statement of the transition from task-specific deep models to large foundation/pre-trained models; core scope; categorization principle; summary of resources and future outlook.
- **Section 1: Introduction:**
  - Contextual rise of foundation models (NLP/CV) and time-series/spatio-temporal motivation.
  - Identification of distinct challenges: continuous numerical distributions, irregular temporal spacing, high dimensionality, non-stationary dynamics.
  - **Table 1 (Survey Comparison Table):** Direct comparison of the survey with preceding reviews along dimensions: scope (general vs. domain-specific), data modalities covered (univariate, multivariate, spatio-temporal, multimodal), methodology coverage (pre-trained TSFMs, LLM fine-tuning/reprogramming, cross-modal alignment), and publication date.
  - Summary of contributions (4 structured bullet points).
- **Section 2: Background & Preliminaries:**
  - Mathematical formalization of univariate, multivariate, and spatio-temporal series.
  - Task formulations with explicit notation: forecasting (point & probabilistic), classification, imputation, anomaly detection.
  - Fundamental learning paradigms: Masked Autoencoding (MAE), Contrastive Learning (InfoNCE), Generative Next-Token Prediction.
- **Section 3: Overview & Categorization (Taxonomy):**
  - Conceptual framing of taxonomy along orthogonal axes:
    1. *Data perspective:* single-modal vs. multimodal vs. spatio-temporal.
    2. *Model perspective:* Pre-trained from scratch (TSFMs) vs. LLM adaptation (Direct prompting, Fine-tuning, Reprogramming/Prefix-tuning).
    3. *Task perspective:* discriminative vs. generative vs. analytical/reasoning.
  - High-resolution, multi-tier taxonomy figure synthesizing the ecosystem.
- **Section 4 & 5: Core Methodological Sections:**
  - Detailed model breakdown with rigorous design comparison tables:
    - Backbone architecture (Transformer encoder, decoder-only, MoE, GNN).
    - Tokenization / Patching strategy.
    - Pre-training objective and dataset size.
    - Adaptability / zero-shot capability.
- **Section 6: Resources, Applications & Benchmarks:**
  - Curated summary tables of public datasets, benchmark suites (e.g., GIFT-Eval, Monash, WeatherBench), open-source repositories.
  - Practical domains: finance, energy, weather/climate, healthcare, IoT/transportation.
- **Section 7: Open Challenges & Future Directions:**
  - Systematic discussion of current bottlenecks: cross-modal semantics alignment, long-sequence context scaling, computational efficiency, evaluation fairness / data contamination, inductive bias vs. generalizability.
- **Section 8: Conclusion:** Synthesis and call to action.

---

## 2. Secondary Template Architecture (arXiv:2402.02713)

### 2.1 Critical Arguments and Philosophical Lens
- **The "Why LLM for Time Series" Debate:**
  - Can text-pretrained transformers encode numerical and temporal dynamics without domain collapse?
  - Modality alignment vs. superficial feature projection.
- **Methodological Taxonomy:**
  - *Direct Prompting:* serializing numerical series as textual tokens.
  - *Time-Series Reprogramming:* keeping the LLM frozen while learning linear/cross-attention patch adapters (e.g., Time-LLM, GPT4TS).
  - *Unified Multimodal Tokenization:* mapping TS patches and text/visual tokens into a joint representation space.
  - *Agentic & Tool-Using Frameworks:* using LLMs as controllers, analysts, and reasoning agents over analytical tools.
- **Empirical Rigor & Sanity Checks:**
  - Addressing whether LLMs merely act as overparameterized linear feature extractors.
  - Highlighting benchmark leakage, zero-shot evaluation protocols, and standard reporting criteria.

---

## 3. Adaptation Strategy for Multimodal Time Series Survey

To adapt this framework to **"Multimodal Time Series Models: A Survey and Outlook"** (Scope: 2021–present), we implement the following core design choices:

### 3.1 Taxonomy Refinement (5 Orthogonal Dimensions)
1. **Modality Pairings:**
   - Time Series + Text (natural language context, domain reports, news, instructions).
   - Time Series + Vision / Images (spectral imagery, plotted TS as images, video/frames, spectrograms).
   - Time Series + Graphs / Spatial topology (sensor networks, traffic/climate grids).
   - Time Series + Tabular / Metadata (static entity attributes, relational context).
   - Multi-way Omnimodal (TS + Text + Vision + Audio + Sensors).
2. **Functional Role of the Non-TS Modality:**
   - *Context / Condition:* Text/metadata provides auxiliary conditioning for forecasting/anomaly detection.
   - *Supervision / Target:* Generating captions, summary reports, or question-answering explanations from TS.
   - *Interface / Reasoning:* LLM serves as an analytical agent interpreting time-series dynamics and formulating hypotheses.
   - *Joint Embedding / Mutual Alignment:* Metric learning and contrastive pairing (e.g., cross-modal retrieval, zero-shot classification).
3. **Fusion & Alignment Architecture:**
   - *Early Fusion (Input Tokenization):* Patch-to-token projections combined directly with text/visual tokens.
   - *Cross-Attention / Intermediate Fusion:* Specialized adapters querying TS representations via cross-attention layers.
   - *Late Fusion:* Separate modality encoders aggregated at final decision heads.
   - *Modality Transcoding:* Visual rendering (rendering time series as line plots for standard VLMs like GPT-4V, Claude, LLaVA).
   - *Reprogramming / Prefix Tuning:* Cross-modal reprogramming layers feeding into frozen LLM backbones.
4. **Pretraining & Learning Objectives:**
   - Cross-Modal Contrastive Learning (CLIP-style InfoNCE between TS and text/images).
   - Multimodal Masked Modeling (MIM / MLM over aligned tokens).
   - Autoregressive Next-Token Generation (joint text + TS autoregression).
   - Instruction Tuning & RLHF/DPO for temporal reasoning.
5. **Application Domains & Tasks:**
   - Domains: Healthcare & EHR, Finance & Markets, Meteorology & Earth Science, Industry 4.0 & IoT, Smart Grids & Energy.
   - Tasks: Multimodal Forecasting, Multimodal Anomaly Detection, Time-Series Question Answering (TS-QA), Time-Series Captioning & Report Generation, Cross-Modal Retrieval.

### 3.2 Visual & Tabular Artefacts to Implement
- **Taxonomy Figure:** Clear hierarchy mapping Modality Pairs $\times$ Fusion Paradigms $\times$ Downstream Roles $\times$ Domains.
- **Comparison Table 1:** Survey positioning against prior surveys (e.g., Jin et al. 2023, Zhang et al. 2024, Liu et al. 2024).
- **Core Summary Table (Methodological Landscape):** Every included model evaluated on: Modality Pair, Model Backbone, Fusion Mechanism, Pretraining Objective, Zero-shot Capability, Parameter Count, Code Verification.
- **PRISMA Flow Diagram:** Quantifying systematic screening from initial hits to included corpus.
- **Heatmap:** Modality Pair vs. Downstream Task cross-tabulation.
- **Chronological Timeline:** Evolution from early text-conditioned models (2021) to unified multimodal foundation models (2024–2026).
