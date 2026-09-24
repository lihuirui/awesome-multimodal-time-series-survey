# Awesome Multimodal Time Series Models: A Survey and Outlook

[![Survey Paper](https://img.shields.io/badge/Paper-PDF-red.svg)](paper/main.pdf) 
[![PRISMA 2020](https://img.shields.io/badge/PRISMA-2020%20Compliant-blue.svg)](docs/PROTOCOL.md) 
[![Continuous Review](https://img.shields.io/badge/Systematic%20Review-Iteration%201-brightgreen.svg)](docs/STATE.md) 
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 

> **Bilingual Repository** / **中英文双语前沿综述与开源精选仓库**  
> A rigorously verified, continuously updated repository tracking multimodal time series models, cross-modal representation learning, foundation models, and reasoning frameworks (2021–present).

---

## 🇨🇳 中文简介 (Executive Summary in Chinese)

时序数据在气象、金融、医疗电子病历、交通和工业物联网中无处不在。传统的单模态时序模型（如统计方法或纯数值Transformer）往往受限于单一维度的数值波动，无法捕获高阶语义背景、事件影响与多模态因果关联。

本综述全面梳理了 **2021年至今的多模态时序前沿工作**，深入探讨了将时序信号与**自然语言文本（新闻、报告、指令提示）**、**视觉图像（折线图、频谱图、卫星影像）**及**多模态知识**协同建模的新范式。核心内容涵盖：
- **重编程与提示对齐（Reprogramming & Prompting）：** 如 Time-LLM、One Fits All (GPT4TS)、TEMPO、CALF，通过重编程层将时序Patch映射到预训练语言模型的潜空间；
- **视觉映射与跨模态掩码自编码（Visual Transcoding）：** 如 VisionTS、Time-VLM，将一维时序信号绘制为图像后直接利用成熟的视觉基座（如MAE）实现跨模态零样本预测；
- **多模态时序基座与多任务统一框架（Unified Multimodal TSFMs）：** 如 UniTS、ChatTime，在单一模型内支持跨模态提示条件化与多任务求解；
- **对话交互与复杂时序推理（TS-MLLMs & Reasoning）：** 如 ChatTS、TimeOmni、Sonar-TS，使多模态大模型具备时序感知、外推、因果发现与数据库自然语言查询能力；
- **多模态基准与评估规范（Datasets & Benchmarks）：** 如 Time-MMD、Fidel-TS、MTBench，解决跨模态对齐数据的标准化评测问题。

详细中文全篇分析请参阅 [docs/SURVEY_zh.md](docs/SURVEY_zh.md)。

---

## 📊 Taxonomy Framework

The survey synthesizes existing research across four orthogonal dimensions: **Modality Pairing**, **Fusion Architecture**, **Functional Role of Complementary Modalities**, and **Downstream Tasks & Domains**.

![Taxonomy of Multimodal Time Series Models](paper/figures/taxonomy.png)

### 📈 Chronological Milestones (2022–2026)

![Timeline of Multimodal Time Series Models](paper/figures/timeline_milestones.png)

### 🔍 PRISMA 2020 Systematic Review Counts

- **Total Records Identified:** 190 (Databases: 142, Snowballing: 48)
- **Deduplicated & Screened:** 154 (Duplicates removed: 36)
- **Full-Text Assessed:** 36 (Excluded with documented rationale: 10)
- **Included in Systematic Synthesis:** **26** studies

![PRISMA 2020 Flow](paper/figures/prisma_flow.png)

---

## 📚 Curated Papers by Taxonomy Category

### Cross-Modal Reprogramming & Adaptation

- **[CALF: Aligning LLMs for Time Series Forecasting via Cross-modal Fine-Tuning](https://arxiv.org/abs/2403.07300)** (arXiv 2024 2024) • [Code](https://github.com/Hank0626/CALF)  
  *Authors:* Peiyuan Liu, Hang Guo, Tao Dai et al.  
  *Modality:* `TS+Text` | *Fusion:* `cross_modal_loss` | *Role:* `context_condition`  
  *Highlight:* Cross-modal fine-tuning framework aligning temporal and textual representations using matching loss and output consistency.  

- **[$\textbf{S}^2$IP-LLM: Semantic Space Informed Prompt Learning with LLM for Time Series Forecasting](https://arxiv.org/abs/2403.05798)** (arXiv 2024 2024) • [Code](https://github.com/PanZ-s/S2IP-LLM)  
  *Authors:* Zijie Pan, Yushan Jiang, Sahil Garg et al.  
  *Modality:* `TS+Text` | *Fusion:* `semantic_anchor` | *Role:* `context_condition`  
  *Highlight:* Semantic space informed prompt learning retrieving top-k semantic anchors to steer LLM time-series forecast generation.  

- **[AutoTimes: Autoregressive Time Series Forecasters via Large Language Models](https://arxiv.org/abs/2402.02370)** (NeurIPS 2024 2024) • [Code](https://github.com/thuml/AutoTimes)  
  *Authors:* Yong Liu, Guo Qin, Xiangdong Huang et al.  
  *Modality:* `TS+Text` | *Fusion:* `reprogramming_patching` | *Role:* `context_condition`  
  *Highlight:* Repurposes decoder-only LLMs as autoregressive time series forecasters with chronological timestamp prompts and in-context forecasting.  

- **[Time-LLM: Time Series Forecasting by Reprogramming Large Language Models](https://arxiv.org/abs/2310.01728)** (ICLR 2024 2023) • [Code](https://github.com/KimMeen/Time-LLM)  
  *Authors:* Ming Jin, Shiyu Wang, Lintao Ma et al.  
  *Modality:* `TS+Text` | *Fusion:* `reprogramming_patching` | *Role:* `context_condition`  
  *Highlight:* Milestone work introducing reprogramming layers to adapt frozen LLMs for time-series forecasting with domain prompts.  

- **[One Fits All:Power General Time Series Analysis by Pretrained LM](https://arxiv.org/abs/2302.11939)** (NeurIPS 2023 2023) • [Code](https://github.com/DAMO-DI-ML/NeurIPS2023-One-Fits-All)  
  *Authors:* Tian Zhou, PeiSong Niu, Xue Wang et al.  
  *Modality:* `TS+Text` | *Fusion:* `reprogramming_patching` | *Role:* `context_condition`  
  *Highlight:* Pioneering cross-modal transfer framework (GPT4TS / FPT) showing frozen pre-trained language transformers generalize to universal time series tasks.  

- **[TEST: Text Prototype Aligned Embedding to Activate LLM&#39;s Ability for Time Series](https://arxiv.org/abs/2308.08241)** (arXiv 2023 2023) • [Code](https://github.com/ChenxiSun/TEST)  
  *Authors:* Chenxi Sun, Hongyan Li, Yaliang Li et al.  
  *Modality:* `TS+Text` | *Fusion:* `contrastive_prototype` | *Role:* `context_condition`  
  *Highlight:* Text prototype-aligned embedding mapping raw time series into discrete language token semantics via soft contrastive alignment.  

- **[TEMPO: Prompt-based Generative Pre-trained Transformer for Time Series Forecasting](https://arxiv.org/abs/2310.04948)** (ICLR 2024 2023) • [Code](https://github.com/DC-Mody/TEMPO)  
  *Authors:* Defu Cao, Furong Jia, Sercan O Arik et al.  
  *Modality:* `TS+Text` | *Fusion:* `reprogramming_patching` | *Role:* `context_condition`  
  *Highlight:* Prompt-based generative pre-trained transformer conditioning predictions on trend, seasonal, and residual textual prompts.  

- **[LLM4TS: Aligning Pre-Trained LLMs as Data-Efficient Time-Series Forecasters](https://arxiv.org/abs/2308.08469)** (arXiv 2023 2023) • [Code](https://github.com/chengsong/LLM4TS)  
  *Authors:* Ching Chang, Wei-Yao Wang, Wen-Chih Peng et al.  
  *Modality:* `TS+Text` | *Fusion:* `reprogramming_patching` | *Role:* `context_condition`  
  *Highlight:* Aligns pre-trained LLMs as data-efficient time-series forecasters using a two-stage alignment strategy.  

- **[Large Language Models Are Zero-Shot Time Series Forecasters](https://arxiv.org/abs/2310.07820)** (NeurIPS 2023 2023) • [Code](https://github.com/ngruver/llmtime)  
  *Authors:* Nate Gruver, Marc Finzi, Shikai Qiu et al.  
  *Modality:* `TS+Text` | *Fusion:* `text_serialization` | *Role:* `text_serialization`  
  *Highlight:* Demonstrates that LLMs zero-shot forecast numerical sequences by tokenizing formatted numerical strings without any weight fine-tuning.  

### Vision-Language & Visual Rendering

- **[Time-VLM: Exploring Multimodal Vision-Language Models for Augmented Time Series Forecasting](https://arxiv.org/abs/2502.04395)** (ICML 2025 2025) • [Code](https://github.com/decisionintelligence/Time-VLM)  
  *Authors:* Siru Zhong, Weilin Ruan, Ming Jin et al.  
  *Modality:* `TS+Vision+Text` | *Fusion:* `cross_attention` | *Role:* `context_condition`  
  *Highlight:* Augments forecasting using dual vision-augmented and text-augmented learners fused through multimodal vision-language architectures.  

- **[VisionTS: Visual Masked Autoencoders Are Free-Lunch Zero-Shot Time Series Forecasters](https://arxiv.org/abs/2408.17253)** (NeurIPS 2024 2024) • [Code](https://github.com/Keytoyze/VisionTS)  
  *Authors:* Mouxiang Chen, Lefei Shen, Zhuo Li et al.  
  *Modality:* `TS+Vision` | *Fusion:* `visual_rendering` | *Role:* `modality_transcoding`  
  *Highlight:* Reformulates time series forecasting as visual masked image reconstruction; shows vision MAE acts as zero-shot forecaster.  

### Multimodal Time Series Foundation Models & Multi-Task

- **[TRACE: Grounding Time Series in Context for Multimodal Embedding and Retrieval](https://arxiv.org/abs/2506.09114)** (NeurIPS 2025 2025) • [Code](https://github.com/Guuuli/TRACE)  
  *Authors:* Jialin Chen, Ziyu Zhao, Gaukhar Nurbek et al.  
  *Modality:* `TS+Text` | *Fusion:* `dual_encoder_contrastive` | *Role:* `joint_representation`  
  *Highlight:* Grounds time series in textual context via channel identity tokens and dual contrastive alignment for bidirectional TS-text retrieval.  

- **[UniTS: A Unified Multi-Task Time Series Model](https://arxiv.org/abs/2403.00131)** (NeurIPS 2024 2024) • [Code](https://github.com/mims-harvard/UniTS)  
  *Authors:* Shanghua Gao, Teddy Koker, Owen Queen et al.  
  *Modality:* `TS+Text` | *Fusion:* `early_tokenization` | *Role:* `context_condition`  
  *Highlight:* Unified multi-task time-series model taking natural language task prompts to dynamically configure architectural prediction heads.  

- **[Chronos: Learning the Language of Time Series](https://arxiv.org/abs/2403.07815)** (arXiv 2024 2024) • [Code](https://github.com/amazon-science/chronos-forecasting)  
  *Authors:* Abdul Fatir Ansari, Lorenzo Stella, Caner Turkmen et al.  
  *Modality:* `TS+Text` | *Fusion:* `token_quantization` | *Role:* `tokenization_substrate`  
  *Highlight:* Tokenizes scaled time series into discrete language vocabulary bins, demonstrating foundation model transfer from NLP architectures.  

### Multimodal Datasets & Evaluation Benchmarks

- **[Fidel-TS: A High-Fidelity Multimodal Benchmark for Time Series Forecasting](https://arxiv.org/abs/2509.24789)** (arXiv 2025 2025) • [Code](https://github.com/fidel-ts/fidel-benchmark)  
  *Authors:* Zhijian Xu, Wanxu Cai, Xilin Dai et al.  
  *Modality:* `TS+Text` | *Fusion:* `multimodal_evaluation` | *Role:* `benchmark`  
  *Highlight:* High-fidelity multimodal benchmark evaluating time series forecasting across multimodal contexts and domain variations.  

- **[MTBench: A Multimodal Time Series Benchmark for Temporal Reasoning and Question Answering](https://arxiv.org/abs/2503.16858)** (arXiv 2025 2025) • [Code](https://github.com/mtbench-ts/mtbench)  
  *Authors:* Jialin Chen, Aosong Feng, Ziyu Zhao et al.  
  *Modality:* `TS+Text` | *Fusion:* `multimodal_evaluation` | *Role:* `benchmark`  
  *Highlight:* Multimodal benchmark specifically designed to rigorously evaluate temporal reasoning and question answering over time series.  

- **[Time-MMD: Multi-Domain Multimodal Dataset for Time Series Analysis](https://arxiv.org/abs/2406.08627)** (NeurIPS 2024 2024) • [Code](https://github.com/AdityaLab/Time-MMD)  
  *Authors:* Haoxin Liu, Shangqing Xu, Zhiyuan Zhao et al.  
  *Modality:* `TS+Text` | *Fusion:* `early_tokenization` | *Role:* `context_condition`  
  *Highlight:* First large-scale multi-domain multimodal dataset covering 9 distinct domains with fine-grained numerical-textual alignment.  

### Conversational TS-MLLMs & Reasoning Frameworks

- **[TimeOmni-1: Incentivizing Complex Reasoning with Time Series in Large Language Models](https://arxiv.org/abs/2509.24803)** (arXiv 2025 2025) • [Code](https://github.com/time-series-foundation-models/TimeOmni)  
  *Authors:* Tong Guan, Zijie Meng, Dianqi Li et al.  
  *Modality:* `TS+Text` | *Fusion:* `early_tokenization` | *Role:* `conversational_interface`  
  *Highlight:* Time Series Reasoning Suite (TSR-Suite) incentivizing perception, extrapolation, and decision-making via RL and supervised fine-tuning.  

- **[ChatTS: Aligning Time Series with LLMs via Synthetic Data for Enhanced Understanding and Reasoning](https://arxiv.org/abs/2412.03104)** (VLDB 2025 2024) • [Code](https://github.com/Time-Series-Library/ChatTS)  
  *Authors:* Zhe Xie, Zeyan Li, Xiao He et al.  
  *Modality:* `TS+Text` | *Fusion:* `early_tokenization` | *Role:* `conversational_interface`  
  *Highlight:* Native time series multimodal LLM trained with Time Series Evol-Instruct for complex interactive temporal reasoning and Q&A.  

- **[ChatTime: A Unified Multimodal Time Series Foundation Model Bridging Numerical and Textual Data](https://arxiv.org/abs/2412.11376)** (AAAI 2025 2024) • [Code](https://github.com/ChatTime/ChatTime)  
  *Authors:* Chengsen Wang, Qi Qi, Jingyu Wang et al.  
  *Modality:* `TS+Text` | *Fusion:* `early_tokenization` | *Role:* `conversational_interface`  
  *Highlight:* Unified multimodal foundation model bridging numerical and textual time series data with bimodal input/output capabilities.  

- **[PromptCast: A New Prompt-based Learning Paradigm for Time Series Forecasting](https://arxiv.org/abs/2210.08964)** (IEEE TKDE 2023 2022) • [Code](https://github.com/cruiseresearchgroup/PISA-PromptCast)  
  *Authors:* Hao Xue, Flora D. Salim  
  *Modality:* `TS+Text` | *Fusion:* `text_serialization` | *Role:* `conversational_interface`  
  *Highlight:* First work casting numerical time series forecasting as a prompt-based question answering task via numerical token serialization.  

### Time Series Pre-trained Baselines & Reference Surveys

- **[MOMENT: A Family of Open Time-series Foundation Models](https://arxiv.org/abs/2402.03885)** (ICML 2024 2024) • [Code](https://github.com/monash-moment/moment)  
  *Authors:* Mononito Goswami, Konrad Szafer, Arjun Choudhry et al.  
  *Modality:* `TS+Text` | *Fusion:* `patch_masking` | *Role:* `baseline_context`  
  *Highlight:* High-impact open-source foundation model family for time series, widely adopted as core baseline for multimodal comparison.  

- **[Timer: Generative Pre-trained Transformers Are Large Time Series Models](https://arxiv.org/abs/2402.02368)** (ICML 2024 2024) • [Code](https://github.com/thuml/Large-Time-Series-Model)  
  *Authors:* Yong Liu, Haoran Zhang, Chenyu Li et al.  
  *Modality:* `TS+Text` | *Fusion:* `next_token_prediction` | *Role:* `baseline_context`  
  *Highlight:* Pre-trained autoregressive foundation model from Tsinghua THUML group serving as standard unimodal foundation model comparison.  

- **[Tiny Time Mixers (TTMs): Fast Pre-trained Models for Enhanced Zero/Few-Shot Forecasting of Multivariate Time Series](https://arxiv.org/abs/2401.03955)** (NeurIPS 2024 2024) • [Code](https://github.com/ibm-granite/granite-tsfm)  
  *Authors:* Vijay Ekambaram, Arindam Jati, Pankaj Dayama et al.  
  *Modality:* `TS+Text` | *Fusion:* `patch_mixer` | *Role:* `baseline_context`  
  *Highlight:* Ultra-lightweight foundation model family developed by IBM Research demonstrating parameter-efficient zero/few-shot forecasting.  

- **[Position: What Can Large Language Models Tell Us about Time Series Analysis](https://arxiv.org/abs/2402.02713)** (ICML 2024 2024) • [Code](https://github.com/KimMeen/Time-LLM)  
  *Authors:* Ming Jin, Yifan Zhang, Wei Chen et al.  
  *Modality:* `TS+Text` | *Fusion:* `critical_review` | *Role:* `position_analysis`  
  *Highlight:* Secondary reference template establishing critical position on what LLMs can offer time-series analysis and methodological pitfalls.  

- **[Large Models for Time Series and Spatio-Temporal Data: A Survey and Outlook](https://arxiv.org/abs/2310.10196)** (arXiv 2023 2023) • [Code](https://github.com/KimMeen/Awesome-Large-Models-for-Time-Series-and-Spatio-Temporal-Data)  
  *Authors:* Ming Jin, Yaxuan Kong, Yuxuan Liang et al.  
  *Modality:* `TS+Text+Vision+SpatioTemporal` | *Fusion:* `systematic_review` | *Role:* `survey_reference`  
  *Highlight:* Primary reference survey synthesizing large models for time-series and spatio-temporal data across pre-trained and LLM-adapted paradigms.  

---

## 🔬 Benchmark & Dataset Landscape

![Dataset Landscape](paper/figures/dataset_landscape.png)

---

## 🛠️ How This Survey is Maintained

This repository operates under the **Antigravity Autonomous Research Protocol**: 
1. **Zero Fabrication:** Every cited work is strictly validated through verified public API responses (arXiv, Semantic Scholar, Crossref, DBLP).
2. **Reproducible Quality Gates:** Verified by `make check`—ensuring mathematical schema integrity, citation closure, and automated LaTeX builds.
3. **Continuous Review Loop:** Systematically re-executed across iterations following PRISMA 2020 protocol.

To run quality checks locally:
```bash
make all
```
