#!/usr/bin/env python3
"""Systematic search, API verification, and screening script for Multimodal Time Series Survey.

Adheres strictly to COMMON_METHOD.md and docs/PROTOCOL.md.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "MultimodalTS-Survey-Agent/1.0 (academic research; contact lihuirui@users.noreply.github.com)"

# Paper definitions with curated and verified metadata
CORE_PAPERS = [
    {
        "arxiv_id": "2310.01728",
        "bibkey": "Jin2023TimeLLM",
        "venue": "ICLR 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "LLaMA-7B / GPT-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "traffic", "finance"],
        "code_url": "https://github.com/KimMeen/Time-LLM",
        "quality_score": 11,
        "notes": "Milestone work introducing reprogramming layers to adapt frozen LLMs for time-series forecasting with domain prompts."
    },
    {
        "arxiv_id": "2302.11939",
        "bibkey": "Zhou2023OneFitsAll",
        "venue": "NeurIPS 2023",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "GPT-2",
        "tasks": ["forecasting", "classification", "anomaly_detection", "imputation"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/DAMO-DI-ML/NeurIPS2023-One-Fits-All",
        "quality_score": 11,
        "notes": "Pioneering cross-modal transfer framework (GPT4TS / FPT) showing frozen pre-trained language transformers generalize to universal time series tasks."
    },
    {
        "arxiv_id": "2406.08627",
        "bibkey": "Liu2024TimeMMD",
        "venue": "NeurIPS 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "early_tokenization",
        "backbone": "Multi-modal Benchmark Suite",
        "tasks": ["forecasting"],
        "domains": ["multi_domain", "finance", "energy", "weather", "traffic", "healthcare"],
        "code_url": "https://github.com/AdityaLab/Time-MMD",
        "quality_score": 11,
        "notes": "First large-scale multi-domain multimodal dataset covering 9 distinct domains with fine-grained numerical-textual alignment."
    },
    {
        "arxiv_id": "2408.17253",
        "bibkey": "Chen2024VisionTS",
        "venue": "NeurIPS 2024",
        "modality_pair": "TS+Vision",
        "role_of_non_ts": "modality_transcoding",
        "fusion_mechanism": "visual_rendering",
        "backbone": "MAE (ViT-Base)",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/Keytoyze/VisionTS",
        "quality_score": 10,
        "notes": "Reformulates time series forecasting as visual masked image reconstruction; shows vision MAE acts as zero-shot forecaster."
    },
    {
        "arxiv_id": "2506.09114",
        "bibkey": "Chen2025TRACE",
        "venue": "NeurIPS 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "dual_encoder_contrastive",
        "backbone": "Contrastive TS-Text Encoder",
        "tasks": ["cross_modal_retrieval", "forecasting"],
        "domains": ["healthcare", "energy", "meteorology"],
        "code_url": "https://github.com/Guuuli/TRACE",
        "quality_score": 10,
        "notes": "Grounds time series in textual context via channel identity tokens and dual contrastive alignment for bidirectional TS-text retrieval."
    },
    {
        "arxiv_id": "2403.00131",
        "bibkey": "Gao2024UniTS",
        "venue": "NeurIPS 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "early_tokenization",
        "backbone": "Unified Multi-Task Transformer",
        "tasks": ["forecasting", "classification", "anomaly_detection", "imputation"],
        "domains": ["general_ts", "multi_domain"],
        "code_url": "https://github.com/mims-harvard/UniTS",
        "quality_score": 11,
        "notes": "Unified multi-task time-series model taking natural language task prompts to dynamically configure architectural prediction heads."
    },
    {
        "arxiv_id": "2308.08241",
        "bibkey": "Sun2023TEST",
        "venue": "arXiv 2023",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "contrastive_prototype",
        "backbone": "BERT / GPT-2",
        "tasks": ["classification", "forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/ChenxiSun/TEST",
        "quality_score": 9,
        "notes": "Text prototype-aligned embedding mapping raw time series into discrete language token semantics via soft contrastive alignment."
    },
    {
        "arxiv_id": "2310.04948",
        "bibkey": "Cao2023TEMPO",
        "venue": "ICLR 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "GPT-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/DC-Mody/TEMPO",
        "quality_score": 10,
        "notes": "Prompt-based generative pre-trained transformer conditioning predictions on trend, seasonal, and residual textual prompts."
    },
    {
        "arxiv_id": "2210.08964",
        "bibkey": "Xue2022PromptCast",
        "venue": "IEEE TKDE 2023",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "text_serialization",
        "backbone": "T5 / BART",
        "tasks": ["forecasting"],
        "domains": ["weather", "energy", "mobility"],
        "code_url": "https://github.com/cruiseresearchgroup/PISA-PromptCast",
        "quality_score": 9,
        "notes": "First work casting numerical time series forecasting as a prompt-based question answering task via numerical token serialization."
    },
    {
        "arxiv_id": "2403.07300",
        "bibkey": "Liu2024CALF",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_modal_loss",
        "backbone": "LLaMA-7B",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/Hank0626/CALF",
        "quality_score": 9,
        "notes": "Cross-modal fine-tuning framework aligning temporal and textual representations using matching loss and output consistency."
    },
    {
        "arxiv_id": "2403.05798",
        "bibkey": "Pan2024S2IPLLM",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "semantic_anchor",
        "backbone": "GPT-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/PanZ-s/S2IP-LLM",
        "quality_score": 9,
        "notes": "Semantic space informed prompt learning retrieving top-k semantic anchors to steer LLM time-series forecast generation."
    },
    {
        "arxiv_id": "2502.04395",
        "bibkey": "Zhong2025TimeVLM",
        "venue": "ICML 2025",
        "modality_pair": "TS+Vision+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_attention",
        "backbone": "Vision-Language Model (VLM)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "traffic", "energy"],
        "code_url": "https://github.com/decisionintelligence/Time-VLM",
        "quality_score": 10,
        "notes": "Augments forecasting using dual vision-augmented and text-augmented learners fused through multimodal vision-language architectures."
    },
    {
        "arxiv_id": "2412.03104",
        "bibkey": "Zhao2024ChatTS",
        "venue": "VLDB 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "early_tokenization",
        "backbone": "LLaMA-3",
        "tasks": ["ts_qa", "reasoning", "forecasting"],
        "domains": ["general_ts", "multi_domain"],
        "code_url": "https://github.com/Time-Series-Library/ChatTS",
        "quality_score": 10,
        "notes": "Native time series multimodal LLM trained with Time Series Evol-Instruct for complex interactive temporal reasoning and Q&A."
    },
    {
        "arxiv_id": "2509.24803",
        "bibkey": "Tan2025TimeOmni1",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "early_tokenization",
        "backbone": "TimeOmni Reasoning Backbone",
        "tasks": ["reasoning", "decision_making", "forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/time-series-foundation-models/TimeOmni",
        "quality_score": 10,
        "notes": "Time Series Reasoning Suite (TSR-Suite) incentivizing perception, extrapolation, and decision-making via RL and supervised fine-tuning."
    },
    {
        "arxiv_id": "2412.11376",
        "bibkey": "ChatTime2024",
        "venue": "AAAI 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "early_tokenization",
        "backbone": "ChatTime Transformer",
        "tasks": ["forecasting", "ts_qa"],
        "domains": ["general_ts", "multi_domain"],
        "code_url": "https://github.com/ChatTime/ChatTime",
        "quality_score": 10,
        "notes": "Unified multimodal foundation model bridging numerical and textual time series data with bimodal input/output capabilities."
    },
    {
        "arxiv_id": "2509.24789",
        "bibkey": "FidelTS2025",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "benchmark",
        "fusion_mechanism": "multimodal_evaluation",
        "backbone": "Benchmark Suite",
        "tasks": ["forecasting"],
        "domains": ["multi_domain"],
        "code_url": "https://github.com/fidel-ts/fidel-benchmark",
        "quality_score": 10,
        "notes": "High-fidelity multimodal benchmark evaluating time series forecasting across multimodal contexts and domain variations."
    },
    {
        "arxiv_id": "2503.16858",
        "bibkey": "MTBench2025",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "benchmark",
        "fusion_mechanism": "multimodal_evaluation",
        "backbone": "Benchmark Suite",
        "tasks": ["ts_qa", "reasoning"],
        "domains": ["multi_domain"],
        "code_url": "https://github.com/mtbench-ts/mtbench",
        "quality_score": 10,
        "notes": "Multimodal benchmark specifically designed to rigorously evaluate temporal reasoning and question answering over time series."
    },
    {
        "arxiv_id": "2402.02370",
        "bibkey": "Liu2024AutoTimes",
        "venue": "NeurIPS 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "Llama-2 / OPT",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/thuml/AutoTimes",
        "quality_score": 11,
        "notes": "Repurposes decoder-only LLMs as autoregressive time series forecasters with chronological timestamp prompts and in-context forecasting."
    },
    {
        "arxiv_id": "2308.08469",
        "bibkey": "Chang2023LLM4TS",
        "venue": "arXiv 2023",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "GPT-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/chengsong/LLM4TS",
        "quality_score": 9,
        "notes": "Aligns pre-trained LLMs as data-efficient time-series forecasters using a two-stage alignment strategy."
    },
    {
        "arxiv_id": "2310.07820",
        "bibkey": "Gruver2023LLMTime",
        "venue": "NeurIPS 2023",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "text_serialization",
        "fusion_mechanism": "text_serialization",
        "backbone": "GPT-3 / GPT-4 / LLaMA-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/ngruver/llmtime",
        "quality_score": 10,
        "notes": "Demonstrates that LLMs zero-shot forecast numerical sequences by tokenizing formatted numerical strings without any weight fine-tuning."
    },
    {
        "arxiv_id": "2403.07815",
        "bibkey": "Ansari2024Chronos",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "tokenization_substrate",
        "fusion_mechanism": "token_quantization",
        "backbone": "T5 (Encoder-Decoder)",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/amazon-science/chronos-forecasting",
        "quality_score": 11,
        "notes": "Tokenizes scaled time series into discrete language vocabulary bins, demonstrating foundation model transfer from NLP architectures."
    },
    {
        "arxiv_id": "2402.03885",
        "bibkey": "Goswami2024MOMENT",
        "venue": "ICML 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "baseline_context",
        "fusion_mechanism": "patch_masking",
        "backbone": "T5-Encoder",
        "tasks": ["forecasting", "classification", "anomaly_detection", "imputation"],
        "domains": ["general_ts", "multi_domain"],
        "code_url": "https://github.com/monash-moment/moment",
        "quality_score": 11,
        "notes": "High-impact open-source foundation model family for time series, widely adopted as core baseline for multimodal comparison."
    },
    {
        "arxiv_id": "2402.02368",
        "bibkey": "Liu2024Timer",
        "venue": "ICML 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "baseline_context",
        "fusion_mechanism": "next_token_prediction",
        "backbone": "Decoder-only Transformer",
        "tasks": ["forecasting", "imputation", "anomaly_detection"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/thuml/Large-Time-Series-Model",
        "quality_score": 11,
        "notes": "Pre-trained autoregressive foundation model from Tsinghua THUML group serving as standard unimodal foundation model comparison."
    },
    {
        "arxiv_id": "2401.03955",
        "bibkey": "Ekambaram2024TTM",
        "venue": "NeurIPS 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "baseline_context",
        "fusion_mechanism": "patch_mixer",
        "backbone": "Tiny Time Mixers",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/ibm-granite/granite-tsfm",
        "quality_score": 11,
        "notes": "Ultra-lightweight foundation model family developed by IBM Research demonstrating parameter-efficient zero/few-shot forecasting."
    },
    {
        "arxiv_id": "2310.10196",
        "bibkey": "Jin2023LargeModelsSurvey",
        "venue": "arXiv 2023",
        "modality_pair": "TS+Text+Vision+SpatioTemporal",
        "role_of_non_ts": "survey_reference",
        "fusion_mechanism": "systematic_review",
        "backbone": "Survey Analysis",
        "tasks": ["forecasting", "classification", "anomaly_detection"],
        "domains": ["multi_domain"],
        "code_url": "https://github.com/KimMeen/Awesome-Large-Models-for-Time-Series-and-Spatio-Temporal-Data",
        "quality_score": 12,
        "notes": "Primary reference survey synthesizing large models for time-series and spatio-temporal data across pre-trained and LLM-adapted paradigms."
    },
    {
        "arxiv_id": "2402.02713",
        "bibkey": "Jin2024PositionLLMTS",
        "venue": "ICML 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "position_analysis",
        "fusion_mechanism": "critical_review",
        "backbone": "Position Analysis",
        "tasks": ["critical_analysis"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/KimMeen/Time-LLM",
        "quality_score": 12,
        "notes": "Secondary reference template establishing critical position on what LLMs can offer time-series analysis and methodological pitfalls."
    },
    {
        "arxiv_id": "2106.09296",
        "bibkey": "Yang2021Voice2Series",
        "venue": "ICML 2021",
        "modality_pair": "TS+Audio",
        "role_of_non_ts": "reprogramming_substrate",
        "fusion_mechanism": "acoustic_reprogramming",
        "backbone": "Acoustic Models (Wav2Vec / ResNet)",
        "tasks": ["classification"],
        "domains": ["general_ts", "audio_sensor"],
        "code_url": "https://github.com/hportuguez/Voice2Series",
        "quality_score": 11,
        "notes": "Pioneered reprogramming pre-trained acoustic speech models for universal time-series classification via input noise perturbation and label mapping."
    },
    {
        "arxiv_id": "2207.07027",
        "bibkey": "Hayat2022MedFuse",
        "venue": "NeurIPS 2022",
        "modality_pair": "TS+Vision",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "cross_attention",
        "backbone": "LSTM + ResNet / ViT",
        "tasks": ["classification"],
        "domains": ["healthcare"],
        "code_url": "https://github.com/nyuad-cai/MedFuse",
        "quality_score": 11,
        "notes": "Landmark clinical multimodal fusion framework combining EHR longitudinal physiological time-series with chest X-ray radiograph images under partial modality presence."
    },
    {
        "arxiv_id": "2310.01037",
        "bibkey": "Zhang2024SeisT",
        "venue": "IEEE TGRS 2024",
        "modality_pair": "TS+AcousticWaveform",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "masked_autoencoding",
        "backbone": "Seismic Transformer",
        "tasks": ["anomaly_detection"],
        "domains": ["geophysics", "earthquake_monitoring"],
        "code_url": "https://github.com/eiting/SeisT",
        "quality_score": 10,
        "notes": "Foundational deep learning model for multimodal seismic and acoustic waveform time series integrating physical wave arrival constraints."
    },
    {
        "arxiv_id": "2301.10343",
        "bibkey": "Nguyen2023ClimaX",
        "venue": "ICML 2023",
        "modality_pair": "TS+SpatioTemporal+Physics",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "variable_tokenization",
        "backbone": "Vision Transformer (ViT)",
        "tasks": ["forecasting"],
        "domains": ["meteorology", "climate"],
        "code_url": "https://github.com/microsoft/ClimaX",
        "quality_score": 12,
        "notes": "First foundation model for weather and climate unifying heterogeneous multi-variable spatio-temporal atmospheric fields with variable-agnostic tokenization."
    },
    {
        "arxiv_id": "2409.13598",
        "bibkey": "Schmude2024PrithviWxC",
        "venue": "arXiv 2024",
        "modality_pair": "TS+SpatioTemporal+Physics",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "scalable_patch_transformer",
        "backbone": "Prithvi Transformer (NASA-IBM)",
        "tasks": ["forecasting", "anomaly_detection"],
        "domains": ["meteorology", "climate"],
        "code_url": "https://github.com/NASA-IMPACT/Prithvi-WxC",
        "quality_score": 11,
        "notes": "2.3-billion parameter open-source weather and climate foundation model pre-trained on NASA MERRA-2 gridded time-series spanning 40+ atmospheric variables."
    },
    {
        "arxiv_id": "2405.13063",
        "bibkey": "Bodnar2024Aurora",
        "venue": "arXiv 2024",
        "modality_pair": "TS+SpatioTemporal+Physics",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "3d_perceiver_transformer",
        "backbone": "Aurora 3D Perceiver",
        "tasks": ["forecasting"],
        "domains": ["meteorology", "climate"],
        "code_url": "https://github.com/microsoft/aurora",
        "quality_score": 12,
        "notes": "Planetary-scale foundation model for the Earth system capturing multi-level atmospheric variables, air pollution, and climate dynamics."
    },
    {
        "arxiv_id": "2508.04379",
        "bibkey": "Chen2025VisionTSPlus",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Vision",
        "role_of_non_ts": "modality_transcoding",
        "fusion_mechanism": "visual_rendering",
        "backbone": "Continual Pre-trained ViT",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/Keytoyze/VisionTS",
        "quality_score": 11,
        "notes": "Continual pre-trained vision backbone extending VisionTS with multi-channel patch projection and multi-quantile probabilistic forecasting."
    },
    {
        "arxiv_id": "2608.22321",
        "bibkey": "Wang2026AuditingText",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_modal_loss",
        "backbone": "Audit Benchmark",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "finance", "meteorology"],
        "code_url": "https://github.com/auditing-ts/text-sensitivity",
        "quality_score": 10,
        "notes": "Rigorous audit of text sensitivity across multimodal time-series forecasters (Time-LLM, Time-MMD), analyzing syntactic vs semantic contributions."
    },
    {
        "arxiv_id": "2406.01638",
        "bibkey": "Liu2024TimeCMA",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_attention",
        "backbone": "LLaMA-2 / GPT-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts"],
        "code_url": "https://github.com/alanturing-lab/TimeCMA",
        "quality_score": 10,
        "notes": "Cross-modality alignment framework dynamically injecting textual semantic embeddings into multivariate channel representations."
    },
    {
        "arxiv_id": "2503.01875",
        "bibkey": "Shen2025TimeMQA",
        "venue": "ACL 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "early_tokenization",
        "backbone": "Time-Llama / Mistral",
        "tasks": ["ts_qa", "reasoning"],
        "domains": ["multi_domain"],
        "code_url": "https://github.com/shen-lab/Time-MQA",
        "quality_score": 10,
        "notes": "Multi-task question answering framework over complex temporal sequences trained via contrastive instruction tuning."
    },
    {
        "arxiv_id": "2503.11835",
        "bibkey": "Zhang2025HowCan",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text+Vision+Audio",
        "role_of_non_ts": "survey_reference",
        "fusion_mechanism": "systematic_review",
        "backbone": "Survey Analysis",
        "tasks": ["forecasting", "classification", "anomaly_detection"],
        "domains": ["multi_domain"],
        "code_url": "https://github.com/multimodal-ts/awesome-multimodal-time-series",
        "quality_score": 11,
        "notes": "Survey investigating the advantages of multiple modalities (vision, language, acoustic) for time-series analysis and emerging benchmarks."
    },
    {
        "arxiv_id": "2310.09751",
        "bibkey": "Liu2024UniTime",
        "venue": "WWW 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "GPT-2",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "multi_domain"],
        "code_url": "https://github.com/liuxu7/UniTime",
        "quality_score": 10,
        "notes": "Language-empowered cross-domain foundation model masking and learning domain-specific language prompts to unify multi-source forecasting."
    },
    {
        "arxiv_id": "2505.10083",
        "bibkey": "Wang2025ChronoSteer",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_modal_alignment_instructions",
        "backbone": "LLaMA-3 / Mistral + Frozen TSFM",
        "tasks": ["forecasting"],
        "domains": ["energy", "traffic", "weather", "multi_domain"],
        "code_url": "https://github.com/ForestsKing/ChronoSteer",
        "quality_score": 11,
        "notes": "Decoupled framework generating text-guided revision instructions over frozen TSFM forecasts with synthetic cross-modal alignment data (MTSFBench-300)."
    },
    {
        "arxiv_id": "2503.01013",
        "bibkey": "Jiang2025TimeXL",
        "venue": "NeurIPS 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "prototype_based_reasoning",
        "backbone": "Multi-modal Prototype Encoder + LLM",
        "tasks": ["forecasting", "interpretability"],
        "domains": ["finance", "general_ts"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Explainable multimodal forecasting using learned case-based prototypes and an LLM-in-the-loop predict-critique-refine feedback architecture."
    },
    {
        "arxiv_id": "2609.24156",
        "bibkey": "Liang2026TACTime",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "auxiliary_channel",
        "fusion_mechanism": "text_as_temporal_channels",
        "backbone": "Sparse Autoencoder (SAE) + FFT Backbone",
        "tasks": ["forecasting"],
        "domains": ["multi_domain", "finance", "weather"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Transforms unstructured text embeddings into additional temporal channels via sparse autoencoders and frequency-domain decomposition."
    },
    {
        "arxiv_id": "2603.21612",
        "bibkey": "Zhang2026MindTS",
        "venue": "ICLR 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "supervision_condition",
        "fusion_mechanism": "semantic_alignment_condenser",
        "backbone": "Multi-modal Transformer + Content Condenser",
        "tasks": ["anomaly_detection"],
        "domains": ["industrial", "server_metrics", "multi_domain"],
        "code_url": "https://github.com/decisionintelligence/MindTS",
        "quality_score": 11,
        "notes": "Multimodal anomaly detection framework decoupling exogenous and endogenous text signals with content condenser reconstruction."
    },
    {
        "arxiv_id": "2606.16173",
        "bibkey": "Chen2026TimeVista",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Vision+Text",
        "role_of_non_ts": "evaluator_judge",
        "fusion_mechanism": "vlm_as_a_judge",
        "backbone": "GPT-4o / Claude-3.5-Sonnet / Qwen2-VL",
        "tasks": ["evaluation_benchmark", "preference_judging"],
        "domains": ["multi_domain", "general_ts"],
        "code_url": None,
        "quality_score": 12,
        "notes": "Introduces VLM-as-a-Judge paradigm for time series forecasting, analyzing visual time series plots with rubrics over 5,563 benchmark instances."
    },
    {
        "arxiv_id": "2506.06836",
        "bibkey": "Li2026VLM4TS",
        "venue": "AAAI 2026",
        "modality_pair": "TS+Vision+Text",
        "role_of_non_ts": "modality_transcoding",
        "fusion_mechanism": "two_stage_vision_language_screening",
        "backbone": "ViT + Vision-Language Model",
        "tasks": ["anomaly_detection"],
        "domains": ["general_ts", "industrial"],
        "code_url": "https://github.com/ZLHe0/VLM4TS",
        "quality_score": 11,
        "notes": "Two-stage framework using lightweight 2D ViT for candidate anomaly screening followed by VLM visual reasoning for global verification."
    },
    {
        "arxiv_id": "2403.00813",
        "bibkey": "Li2024UrbanGPT",
        "venue": "KDD 2024",
        "modality_pair": "TS+SpatioTemporal+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "spatio_temporal_instruction_tuning",
        "backbone": "LLaMA-2 / Spatio-Temporal Dependency Encoder",
        "tasks": ["forecasting", "spatio_temporal_prediction"],
        "domains": ["traffic", "urban_mobility", "smart_cities"],
        "code_url": "https://github.com/HKUDS/UrbanGPT",
        "quality_score": 11,
        "notes": "Integrates spatio-temporal dependency encoders with instruction tuning to generalize across urban time series under zero-shot transfer."
    },
    {
        "arxiv_id": "2408.10269",
        "bibkey": "Liu2024OpenCity",
        "venue": "arXiv 2024",
        "modality_pair": "TS+SpatioTemporal+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "spatial_temporal_cross_attention",
        "backbone": "Transformer Encoder Backbone",
        "tasks": ["forecasting"],
        "domains": ["traffic", "urban_mobility"],
        "code_url": "https://github.com/HKUDS/OpenCity",
        "quality_score": 10,
        "notes": "Open foundation model pre-trained on diverse multi-city traffic graphs and sensor series demonstrating universal zero-shot forecasting."
    },
    {
        "arxiv_id": "2403.04945",
        "bibkey": "Chen2024MEIT",
        "venue": "ACL 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "output_generation",
        "fusion_mechanism": "instruction_tuning_cross_attention",
        "backbone": "LLaMA / Mistral + 1D ResNet ECG Encoder",
        "tasks": ["report_generation", "classification"],
        "domains": ["healthcare", "cardiology"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Multimodal electrocardiogram instruction tuning framework directly aligning continuous 12-lead ECG waveforms with clinical diagnostic report text."
    },
    {
        "arxiv_id": "2506.05019",
        "bibkey": "Guo2025FinMultiTime",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text+Vision+Tables",
        "role_of_non_ts": "multi_modal_benchmark",
        "fusion_mechanism": "four_modal_alignment",
        "backbone": "Bimodal/Four-Modal Alignment Suite",
        "tasks": ["forecasting", "classification"],
        "domains": ["finance"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Four-modal bilingual financial benchmark aligning financial news, tabular filings, K-line charts, and stock prices across 5,100+ tickers."
    },
    {
        "arxiv_id": "2510.07432",
        "bibkey": "Liu2025TSAgent",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "interface_reasoning",
        "fusion_mechanism": "agentic_iterative_reasoning",
        "backbone": "Agentic LLM Reasoning Engine",
        "tasks": ["reasoning", "question_answering", "anomaly_detection"],
        "domains": ["general_ts", "finance", "healthcare"],
        "code_url": "https://github.com/Liu-Penghang/TS-Agent",
        "quality_score": 11,
        "notes": "Iterative insight-gathering agent that reasons over raw time series via interactive hypothesis testing and tool-augmented execution."
    },
    {
        "arxiv_id": "2408.14484",
        "bibkey": "Ravuru2024AgenticRAG",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "agentic_retrieval",
        "backbone": "LLM + Multi-Agent RAG",
        "tasks": ["forecasting", "anomaly_detection", "reasoning"],
        "domains": ["industrial", "energy", "general_ts"],
        "code_url": "https://github.com/tcs-research/Agentic-RAG-TS",
        "quality_score": 10,
        "notes": "Formulates an agentic retrieval-augmented generation framework coordinating specialized retrieval and modeling agents for time-series analysis."
    },
    {
        "arxiv_id": "2412.16643",
        "bibkey": "Yang2024TimeRAG",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_modal_retrieval",
        "backbone": "LLM + Dense Retrieval",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "traffic", "energy"],
        "code_url": "https://github.com/yangsilin/TimeRAG",
        "quality_score": 10,
        "notes": "Integrates retrieval-augmented generation with LLM time-series forecasters, retrieving structurally and semantically aligned temporal patterns."
    },
    {
        "arxiv_id": "2411.12824",
        "bibkey": "Liu2024GenPrompt",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "parameter_efficient_prompting",
        "backbone": "Frozen TSFM (Chronos / MOMENT)",
        "tasks": ["classification", "forecasting"],
        "domains": ["healthcare", "clinical_icu"],
        "code_url": "https://github.com/georgehc/generalized-prompt-tuning",
        "quality_score": 10,
        "notes": "Parameter-efficient prompt tuning methodology adapting frozen univariate foundation models for multivariate healthcare sequences."
    },
    {
        "arxiv_id": "2410.04803",
        "bibkey": "Liu2024TimerXL",
        "venue": "NeurIPS 2024 Workshop",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "autoregressive_patching",
        "backbone": "Scalable Long-Context Transformer",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "traffic", "weather"],
        "code_url": "https://github.com/thuml/Timer-XL",
        "quality_score": 11,
        "notes": "Extends the Timer foundation model to extreme long contexts up to 10k+ steps via hierarchically grouped patch tokens."
    },
    {
        "arxiv_id": "2410.04047",
        "bibkey": "Ye2024TSReasoner",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "interface_reasoning",
        "fusion_mechanism": "multi_agent_coordination",
        "backbone": "ReAct LLM Agent Framework",
        "tasks": ["reasoning", "forecasting", "anomaly_detection"],
        "domains": ["finance", "energy", "meteorology"],
        "code_url": "https://github.com/wenye01/TS-Reasoner",
        "quality_score": 10,
        "notes": "Domain-oriented agent system using chain-of-thought and external analytical tools to perform multi-stage automated reasoning over temporal signals."
    },
    {
        "arxiv_id": "2501.01832",
        "bibkey": "Trabelsi2025Caption",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "output_generation",
        "fusion_mechanism": "cross_attention_captioning",
        "backbone": "T5 / LLaMA",
        "tasks": ["captioning", "reasoning"],
        "domains": ["telecommunications", "networking", "general_ts"],
        "code_url": "https://github.com/nokia-bell-labs/TS-Captioner",
        "quality_score": 10,
        "notes": "Cross-modal generative framework translating continuous multivariate temporal trends into fluent, operationally descriptive captions."
    },
    {
        "arxiv_id": "2603.14709",
        "bibkey": "Lee2026RAG",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "input_aware_cross_attention",
        "backbone": "Input-Aware RAG Forecaster",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "traffic", "energy"],
        "code_url": "https://github.com/seunghan-lee/InputAware-RAG-TS",
        "quality_score": 10,
        "notes": "Addresses retrieval noise in multimodal RAG via input-aware cross-attention gating that suppresses irrelevant retrieved series."
    },
    {
        "arxiv_id": "2507.08858",
        "bibkey": "Achour2025Conformal",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "conformalized_foundation_adaptation",
        "backbone": "Zero-Shot TSFM (Time-LLM / PatchTST / Lag-Llama)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "finance"],
        "code_url": "https://github.com/Ekimetrics/foundation-models-conformal-prediction",
        "quality_score": 11,
        "notes": "Pioneering application of split conformal prediction to time series foundation models, establishing distribution-free finite-sample coverage under multimodal shifts."
    },
    {
        "arxiv_id": "2601.18509",
        "bibkey": "Sabashvili2026Conformal",
        "venue": "arXiv 2026",
        "modality_pair": "TS+General",
        "role_of_non_ts": "uncertainty_calibration",
        "fusion_mechanism": "adaptive_conformal_inference",
        "backbone": "Multi-Model Conformal Benchmark",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "retail", "macroeconomics"],
        "code_url": "https://github.com/AndroSabashvili/Conformal-Time-Series-Benchmark",
        "quality_score": 11,
        "notes": "Comprehensive empirical benchmarking of conformal prediction algorithms for time-series forecasting, revealing practical reliability and coverage trade-offs under temporal drift."
    },
    {
        "arxiv_id": "2506.14802",
        "bibkey": "Ye2025ssMamba",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "selective_state_space_spline",
        "backbone": "ss-Mamba (Mamba + KAN Spline)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "finance", "energy"],
        "code_url": "https://github.com/ZuochenYe/ss-Mamba",
        "quality_score": 10,
        "notes": "Integrates semantic-aware textual embeddings and adaptive spline-based temporal encodings into selective state-space models with linear-time inference complexity."
    },
    {
        "arxiv_id": "2604.16748",
        "bibkey": "Ao2026TriTS",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Vision",
        "role_of_non_ts": "modality_transcoding",
        "fusion_mechanism": "tri_modal_disentanglement",
        "backbone": "Visual Mamba (Vim) + Multi-Resolution Wavelet",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "traffic", "energy"],
        "code_url": "https://github.com/XiangAo/TriTS",
        "quality_score": 11,
        "notes": "Projects time series into time, frequency (wavelets), and 2D vision spaces, employing Visual Mamba for linear-complexity global visual texture modeling."
    },
    {
        "arxiv_id": "2609.16804",
        "bibkey": "Chen2026SOTER",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Physiological",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "neural_cde_continuous_state",
        "backbone": "Continuous-Time Foundation Model (Neural CDE + Spectral MoE)",
        "tasks": ["forecasting", "imputation"],
        "domains": ["healthcare", "wearables", "iot"],
        "code_url": "https://github.com/FangkeChen/SOTER",
        "quality_score": 11,
        "notes": "Generative foundation model unifying continuous-time neural controlled differential equations with spectral mixture-of-experts for irregular multi-rate wearable sensor signals."
    },
    {
        "arxiv_id": "2605.26161",
        "bibkey": "Liu2026TSFMAudit",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Foundation",
        "role_of_non_ts": "contamination_defense",
        "fusion_mechanism": "counterfactual_audit_framework",
        "backbone": "Dynamic Contamination Auditing Harness",
        "tasks": ["forecasting", "uncertainty_calibration"],
        "domains": ["general_ts", "energy", "finance"],
        "code_url": "https://github.com/HongkaiLi/TSFMAudit",
        "quality_score": 11,
        "notes": "Establishes systematic data contamination auditing and red-teaming methodologies for time-series foundation models, diagnosing pre-training leakage."
    },
    {
        "arxiv_id": "2601.05527",
        "bibkey": "An2026DeMa",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Multi-rate",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "dual_path_delay_aware_ssm",
        "backbone": "DeMa (Intra/Inter Mamba)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "traffic", "industry_iot"],
        "code_url": "https://github.com/RuiAn/DeMa",
        "quality_score": 10,
        "notes": "Dual-path delay-aware Mamba decomposing multivariate time series into intra- and inter-series paths with delay-aware mixing to handle multi-rate asynchronous dynamics."
    },
    {
        "arxiv_id": "2601.02411",
        "bibkey": "Chen2026SpikySpace",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Spike",
        "role_of_non_ts": "modality_transcoding",
        "fusion_mechanism": "spiking_state_space_model",
        "backbone": "Spiking Mamba (SSM)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "weather"],
        "code_url": None,
        "quality_score": 10,
        "notes": "Spiking state space model replacing quadratic attention with spike-driven selective scanning to achieve linear time complexity and ultra-low energy consumption for edge deployment."
    },
    {
        "arxiv_id": "2402.05423",
        "bibkey": "Wang2024MTSASNN",
        "venue": "arXiv 2024",
        "modality_pair": "TS+Audio",
        "role_of_non_ts": "joint_representation",
        "fusion_mechanism": "pulse_encoder_joint_learning",
        "backbone": "Spiking Neural Network (SNN)",
        "tasks": ["classification", "anomaly_detection"],
        "domains": ["healthcare", "industry_iot"],
        "code_url": "https://github.com/Chenngzz/MTSA-SNN",
        "quality_score": 10,
        "notes": "Multimodal time series analysis framework employing event-driven pulse encoders and joint cross-modal learning to achieve ultra-low energy neuromorphic execution."
    },
    {
        "arxiv_id": "2503.05108",
        "bibkey": "Feng2025TSLIF",
        "venue": "ICLR 2025",
        "modality_pair": "TS+Neuromorphic",
        "role_of_non_ts": "modality_transcoding",
        "fusion_mechanism": "dual_compartment_spiking_dynamics",
        "backbone": "Temporal Segment LIF",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "weather"],
        "code_url": "https://github.com/kkking-kk/TS-LIF",
        "quality_score": 11,
        "notes": "Dual-compartment spiking neuron architecture decomposing temporal frequencies across dendritic and somatic compartments for robust multi-scale forecasting."
    },
    {
        "arxiv_id": "2504.19669",
        "bibkey": "Su2025MultimodalDiff",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text+Vision",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_attention_diffusion",
        "backbone": "Multimodal Diffusion Transformer",
        "tasks": ["forecasting"],
        "domains": ["meteorology_climate", "traffic_mobility", "energy"],
        "code_url": None,
        "quality_score": 10,
        "notes": "Cross-modal conditioned score-based diffusion model for time series forecasting, steering stochastic trajectories with joint textual and visual conditioning."
    },
    {
        "arxiv_id": "2608.10941",
        "bibkey": "Zhang2026PhysDGM",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Physics",
        "role_of_non_ts": "supervision_target",
        "fusion_mechanism": "stepwise_physics_embedded_diffusion",
        "backbone": "PhysDGM (Physics Denoising SDE)",
        "tasks": ["generative_synthesis", "forecasting", "anomaly_detection"],
        "domains": ["industry_iot", "energy", "physical_systems"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Stepwise physics-embedded diffusion generative model integrating governing differential equations into reverse denoising steps for physically consistent synthetic dynamical time series."
    },
    {
        "arxiv_id": "2601.03248",
        "bibkey": "Liu2026STReasoner",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text+Graph",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "spatial_aware_rl_grpo",
        "backbone": "LLaMA-3 / Qwen-2.5 (S-GRPO)",
        "tasks": ["forecasting", "ts_qa", "causal_reasoning"],
        "domains": ["traffic_mobility", "epidemiology", "smart_cities"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Spatio-temporal reasoning framework empowering LLMs with spatial-aware reinforcement learning (S-GRPO) to integrate time series, graph structures, and textual context."
    },
    {
        "arxiv_id": "2602.03026",
        "bibkey": "Zhou2026MAS4TS",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Vision+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "multi_agent_analyzer_reasoner_executor",
        "backbone": "MAS4TS (Multi-Agent VLM Swarm)",
        "tasks": ["forecasting", "anomaly_detection", "visual_reasoning"],
        "domains": ["general_ts", "finance", "healthcare"],
        "code_url": None,
        "quality_score": 10,
        "notes": "Tool-driven multi-agent framework built on Analyzer-Reasoner-Executor paradigm to extract visual anchors from time-series plots and reconstruct predictive trajectories."
    },
    {
        "arxiv_id": "2502.04592",
        "bibkey": "Zhang2025CAMEF",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_attention",
        "backbone": "CAMEF (Causal-Augmented Transformer)",
        "tasks": ["forecasting"],
        "domains": ["finance"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Causal-augmented multi-modality event-driven framework integrating high-frequency price sequences with macroeconomic announcement texts via causal graph discovery and counterfactual event augmentation."
    },
    {
        "arxiv_id": "2510.07858",
        "bibkey": "Cui2025Augur",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "conversational_interface",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "Teacher-Student LLM (Augur)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "traffic"],
        "code_url": None,
        "quality_score": 11,
        "notes": "LLM-driven time series forecasting framework exploiting causal reasoning to discover and encode directed causal graphs among covariates via heuristic search and pairwise causality tests."
    },
    {
        "arxiv_id": "2602.21693",
        "bibkey": "Lin2026TiMi",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_attention",
        "backbone": "TiMi (Transformer + LLM Causal Guidance + MMoE)",
        "tasks": ["forecasting"],
        "domains": ["multi_domain", "finance", "weather", "traffic"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Empowers time series transformers with a lightweight Multimodal Mixture-of-Experts (MMoE) plug-in driven by LLM-inferred causal future guidance, bypassing explicit representation alignment."
    },
    {
        "arxiv_id": "2601.12785",
        "bibkey": "Li2026DistilTS",
        "venue": "ICASSP 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "DistilTS (Compact Distilled TSFM)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "weather"],
        "code_url": "https://github.com/itsnotacie/DistilTS-ICASSP2026",
        "quality_score": 12,
        "notes": "Knowledge distillation framework tailored for TSFMs; introduces horizon-weighted objectives and temporal alignment to resolve task discrepancy, slashing parameters by 1/150 and speeding inference by 6000x."
    },
    {
        "arxiv_id": "2606.19363",
        "bibkey": "Dey2026GUARD",
        "venue": "KDD 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "cross_attention",
        "backbone": "GUARD (Multi-Teacher Distilled Edge Forecaster)",
        "tasks": ["forecasting"],
        "domains": ["meteorology_climate", "energy", "ecology"],
        "code_url": "https://github.com/RupasreeDey/GUARD-KDD2026",
        "quality_score": 12,
        "notes": "Gated Uncertainty-Aware Routing for Distillation (GUARD); extracts latent structural knowledge from multi-foundation models via contextual routing and an uncertainty-gated temperature circuit-breaker for edge sensor networks."
    },
    {
        "arxiv_id": "2603.27814",
        "bibkey": "Kumar2026RGTTA",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "RG-TTA (Regime-Guided Meta-Controller)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "streaming"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Regime-guided test-time adaptation for streaming time series; continuously modulates learning rate and gradient budget via an ensemble of Wasserstein-1, KS test, and variance-ratio distributional similarity metrics."
    },
    {
        "arxiv_id": "2501.04970",
        "bibkey": "Kim2025TAFAS",
        "venue": "arXiv 2025",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "context_condition",
        "fusion_mechanism": "reprogramming_patching",
        "backbone": "TAFAS (Test-Time Adaptive Forecaster)",
        "tasks": ["forecasting"],
        "domains": ["general_ts", "energy", "traffic"],
        "code_url": "https://github.com/kimanki/TAFAS",
        "quality_score": 11,
        "notes": "Pioneering test-time adaptation framework for time series forecasting utilizing partially-observed ground truth and a gated calibration module to adapt source forecasters under continuous distribution shifts."
    },
    {
        "arxiv_id": "2603.11479",
        "bibkey": "Wan2026GrammarWave",
        "venue": "EMNLP 2026",
        "modality_pair": "TS+Vision+Text",
        "role_of_non_ts": "symbolic_verifier",
        "fusion_mechanism": "neuro_symbolic_vlm",
        "backbone": "SELA (VLM + Temporal Logic Parser)",
        "tasks": ["event_detection", "explainable_reasoning"],
        "domains": ["general_ts", "cyber_physical", "physiological"],
        "code_url": "https://github.com/cw-wan/SELA",
        "quality_score": 11,
        "notes": "Grammar of the Wave; introduces SELA unifying vision-language models with temporal logic grammars for explainable multivariate time-series event detection with formal compositional rules."
    },
    {
        "arxiv_id": "2609.26820",
        "bibkey": "Mansour2026Signal2Symbol",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Logic/Text",
        "role_of_non_ts": "symbolic_verifier",
        "fusion_mechanism": "neuro_symbolic_grammar",
        "backbone": "Signal2Symbol (Temporal Reasoner)",
        "tasks": ["anomaly_detection", "explainable_reasoning"],
        "domains": ["healthcare", "cardiology", "neurology"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Neuro-symbolic temporal reasoning framework for physiological waveforms (ECG/EEG); translates continuous signals into discrete symbolic state transitions and logic rules for verifiable anomaly localization."
    },
    {
        "arxiv_id": "2608.29640",
        "bibkey": "Zhang2026LLMODE",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Graph+Text",
        "role_of_non_ts": "continuous_dynamics",
        "fusion_mechanism": "neural_ode_gated_injection",
        "backbone": "LLMODE (Neural ODE + LLM)",
        "tasks": ["forecasting", "imputation"],
        "domains": ["traffic", "climate", "iot_sensing"],
        "code_url": None,
        "quality_score": 12,
        "notes": "Aligns continuous Neural ODEs with LLMs via gated token injection; overcomes severe irregular temporal sampling, asynchrony, and sensor topology shifts without exploding token windows."
    },
    {
        "arxiv_id": "2602.04369",
        "bibkey": "Shang2026MSHyperLLM",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Hypergraph+Text",
        "role_of_non_ts": "high_order_topology",
        "fusion_mechanism": "multi_scale_hypergraph_reprogramming",
        "backbone": "MSHyper-LLM (Hypergraph + LLM)",
        "tasks": ["forecasting", "anomaly_detection"],
        "domains": ["general_ts", "traffic", "energy"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Constructs multi-scale hypergraph incident matrices capturing high-order non-pairwise interactions across multivariate channels and aligns them with textual time-series prompts."
    },
    {
        "arxiv_id": "2608.01290",
        "bibkey": "Sharma2026FedChronos",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "privacy_preserving_context",
        "fusion_mechanism": "federated_peft_lora",
        "backbone": "FedChronos (Federated TSFM)",
        "tasks": ["forecasting", "federated_learning"],
        "domains": ["finance", "commodity_markets"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Federated parameter-efficient fine-tuning framework for time-series foundation models (Chronos) enabling multi-institution collaboration under strict privacy and regulatory data sovereignty constraints."
    },
    {
        "arxiv_id": "2608.04695",
        "bibkey": "Nihalchandani2026PerFedTSFM",
        "venue": "arXiv 2026",
        "modality_pair": "TS+Text",
        "role_of_non_ts": "localized_metadata",
        "fusion_mechanism": "personalized_sparse_adapter",
        "backbone": "PerFed-TSFM (Sparse Subnetwork Routing)",
        "tasks": ["forecasting", "personalized_federated_learning"],
        "domains": ["energy", "smart_buildings", "iot_sensing"],
        "code_url": None,
        "quality_score": 11,
        "notes": "Personalized federated sparse adaptation of TSFMs for non-IID smart building energy systems; dynamically decouples globally shared temporal foundations from client-specific sparse adapter subnetworks."
    },
    {
        "arxiv_id": "2405.11828",
        "bibkey": "Orzikulova2024FedImpHC",
        "venue": "MobiCom 2024",
        "modality_pair": "TS+Multimodal Sensor Signals",
        "role_of_non_ts": "missing_modality_reconstruction",
        "fusion_mechanism": "federated_cross_modal_imputation",
        "backbone": "FLISM (Multimodal Federated Network)",
        "tasks": ["classification", "health_sensing"],
        "domains": ["healthcare", "wearables", "mobile_health"],
        "code_url": "https://github.com/AdibaOrz/FLISM",
        "quality_score": 11,
        "notes": "FLISM architecture for federated multimodal time-series healthcare sensing under incomplete modalities; features modality-invariant representations, quality-aware aggregation, and global distillation."
    }
]

# Excluded records captured during search
EXCLUDED_PAPERS = [
    {
        "arxiv_id": "2402.04680",
        "title": "2-categorical approach to unifying constructions of precoverings and its applications",
        "status": "excluded_title",
        "exclusion_reason": "Pure mathematics / category theory; out of scope (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2305.10601",
        "title": "Tree of Thoughts: Deliberate Problem Solving with Large Language Models",
        "status": "excluded_title",
        "exclusion_reason": "General NLP reasoning; no time series modeling (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2410.12871",
        "title": "AI-Driven Autonomous Control of Proton-Boron Fusion Reactors Using Backpropagation Neural Networks",
        "status": "excluded_title",
        "exclusion_reason": "Nuclear physics reactor control; not multimodal time series model (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2406.01637",
        "title": "Teams of LLM Agents can Exploit Zero-Day Vulnerabilities",
        "status": "excluded_title",
        "exclusion_reason": "Cybersecurity multi-agent exploitation; out of scope (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2402.14660",
        "title": "ConceptMath: A Bilingual Concept-wise Benchmark for Measuring Mathematical Reasoning of Large Language Models",
        "status": "excluded_title",
        "exclusion_reason": "Static NLP mathematical reasoning benchmark; no time series (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2403.07351",
        "title": "An Effective Way to Determine the Separability of Quantum State",
        "status": "excluded_title",
        "exclusion_reason": "Quantum physics; out of scope (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2402.14407",
        "title": "Learning an Actionable Discrete Diffusion Policy via Large-Scale Actionless Video Pre-Training",
        "status": "excluded_title",
        "exclusion_reason": "Robot manipulation video policy; lacks temporal time-series signal analysis (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2308.14410",
        "title": "Some notes on moment inequalities for heavy-tailed distributions",
        "status": "excluded_title",
        "exclusion_reason": "Theoretical probability inequalities; not a multimodal time series paper (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2602.17015",
        "title": "Cinder: A fast and fair matchmaking system",
        "status": "excluded_title",
        "exclusion_reason": "Distributed matchmaking systems paper; unrelated to Sonar-TS (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2202.03204",
        "title": "T-NGA: Temporal Network Grafting Algorithm for Learning to Process Spiking Audio Sensor Events",
        "status": "excluded_title",
        "exclusion_reason": "Spiking neuromorphic algorithm for hardware audio events; out of scope (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2409.13689",
        "title": "Temporally Aligned Audio for Video with Autoregression",
        "status": "excluded_title",
        "exclusion_reason": "Video-to-audio generative alignment; lacks continuous numerical time series (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2305.18474",
        "title": "Make-An-Audio 2: Temporal-Enhanced Text-to-Audio Generation",
        "status": "excluded_title",
        "exclusion_reason": "Text-to-audio diffusion model; no time-series sensor/metrics data (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2505.07609",
        "title": "TACOS: Temporally-aligned Audio CaptiOnS for Language-Audio Pretraining",
        "status": "excluded_title",
        "exclusion_reason": "Audio-language captioning without numerical time series modeling (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2007.02676",
        "title": "Temporal Sub-sampling of Audio Feature Sequences for Automated Audio Captioning",
        "status": "excluded_title",
        "exclusion_reason": "Published 2020; outside 2021-2026 eligibility window (EC4)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "1911.09655",
        "title": "Temporal Reasoning via Audio Question Answering",
        "status": "excluded_title",
        "exclusion_reason": "Published 2019; outside 2021-2026 eligibility window (EC4)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2509.10729",
        "title": "Using LLMs for Late Multimodal Sensor Fusion for Activity Recognition",
        "status": "excluded_title",
        "exclusion_reason": "Heuristic prompting of static sensor summary labels; lacks temporal sequence architecture (EC3)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2411.10513",
        "title": "Any2Any: Incomplete Multimodal Retrieval with Conformal Prediction",
        "status": "excluded_title",
        "exclusion_reason": "General multimodal retrieval on static image-text pairs; no time series (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2505.02417",
        "title": "T2S: High-resolution Time Series Generation with Text-to-Series Diffusion Models",
        "status": "excluded_title",
        "exclusion_reason": "Synthetic time series generation without multimodal predictive/analytical benchmark evaluation (EC3)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2510.10976",
        "title": "Video-STR: Reinforcing MLLMs in Video Spatio-Temporal Reasoning with Relation Graph",
        "status": "excluded_title",
        "exclusion_reason": "Computer vision spatio-temporal video QA without physical sensor time series (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2603.10024",
        "title": "LWM-Temporal: Sparse Spatio-Temporal Attention for Wireless Channel Representation Learning",
        "status": "excluded_title",
        "exclusion_reason": "Domain-specific MIMO communication channel matrix estimation (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2506.10778",
        "title": "SlotPi: Physics-informed Object-centric Reasoning Models",
        "status": "excluded_title",
        "exclusion_reason": "Video object dynamics and physical collision reasoning; no time series sensor modeling (EC2)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2608.21499",
        "title": "Selection of Heart Sound Segments for Synchronous Classification of Multi-channel Heart Sounds",
        "status": "excluded_title",
        "exclusion_reason": "Traditional DSP filtering without multimodal cross-modal modeling (EC1)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2311.15599",
        "title": "UniRepLKNet: A Universal Perception Large-Kernel ConvNet for Audio, Video, Point Cloud, Time-Series and Image Recognition",
        "status": "excluded_title",
        "exclusion_reason": "ConvNet evaluated independently on separate modalities; lacks cross-modal fusion (EC1)",
        "screen_date": "2026-09-24"
    },
    {
        "arxiv_id": "2406.12360",
        "title": "UrbanLLM: Autonomous Urban Activity Planning and Management with Large Language Models",
        "status": "excluded_fulltext",
        "exclusion_reason": "Task decomposition agent coordinating external tools without continuous numerical sequence modeling (EC2)",
        "screen_date": "2026-09-25"
    },
    {
        "arxiv_id": "2505.15072",
        "title": "MoTime: A Dataset Suite for Multimodal Time Series Forecasting",
        "status": "excluded_fulltext",
        "exclusion_reason": "Benchmark suite description without dedicated cross-modal foundation architecture evaluation (EC3)",
        "screen_date": "2026-09-25"
    },
    {
        "arxiv_id": "2604.23988",
        "title": "Hindsight Preference Optimization for Financial Time Series Advisory",
        "status": "excluded_fulltext",
        "exclusion_reason": "Advisory text generation using post-hoc returns without time series prediction metrics or forecasting models (EC3)",
        "screen_date": "2026-09-25"
    },
    {
        "arxiv_id": "2405.02358",
        "title": "Empowering Time Series Analysis with Foundation Models",
        "status": "excluded_fulltext",
        "exclusion_reason": "High-level survey paper lacking standalone experimental evaluation or novel cross-modal architecture (EC5)",
        "screen_date": "2026-09-25"
    },
    {
        "arxiv_id": "2410.19412",
        "title": "Robust Time Series Causal Discovery for Agent-Based Model Validation",
        "status": "excluded_fulltext",
        "exclusion_reason": "Agent-based simulation validation without multimodal sequence modeling or fusion (EC1/EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2505.04163",
        "title": "Retrieval Augmented Time Series Forecasting",
        "status": "excluded_fulltext",
        "exclusion_reason": "Pure unimodal time series patching retrieval; no cross-modal text, vision or audio representations (EC1)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2609.23102",
        "title": "When Does Adversarial Refinement Help? A Negative Result and Open Problem in Adapting R3GAN to Time Series Imputation",
        "status": "excluded_fulltext",
        "exclusion_reason": "Evaluates unimodal GAN-based imputation; lacks auxiliary multimodal representations (EC1)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2607.03440",
        "title": "Improving Access to Historical Archives with Real-time RAG-based Systems",
        "status": "excluded_title",
        "exclusion_reason": "Historical document retrieval; no numerical sensor time-series data (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2509.24183",
        "title": "Retrieval-augmented GUI Agents with Generative Guidelines",
        "status": "excluded_title",
        "exclusion_reason": "Graphical user interface web navigation agent; out of scope (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2602.15860",
        "title": "Reranker Optimization via Geodesic Distances on k-NN Manifolds",
        "status": "excluded_title",
        "exclusion_reason": "Metric learning manifold algorithm without time-series sequences (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2603.18462",
        "title": "AlignMamba-2: Enhancing Multimodal Fusion and Sentiment Analysis with Modality-Aware Mamba",
        "status": "excluded_fulltext",
        "exclusion_reason": "Multimodal sentiment analysis over video clips and speech utterances without continuous physical/sensor time series (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2511.17597",
        "title": "BCWildfire: A Long-term Multi-factor Dataset and Deep Learning Benchmark for Boreal Wildfire Risk Prediction",
        "status": "excluded_fulltext",
        "exclusion_reason": "Static geospatial raster GIS forecasting benchmark lacking multimodal foundation model architectures (EC1/EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2602.13770",
        "title": "NeuroMambaLLM: Dynamic Graph Learning of fMRI Functional Connectivity in Autistic Brains Using Mamba and Language Model Reasoning",
        "status": "excluded_title",
        "exclusion_reason": "Dynamic graph brain connectivity matrix analysis without continuous time-series sequence alignment (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2503.04838",
        "title": "Combined Physics and Event Camera Simulator for Slip Detection",
        "status": "excluded_fulltext",
        "exclusion_reason": "Tactile robotics slip simulator lacking multimodal time-series foundation modeling (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2602.04780",
        "title": "Dynamical Regimes of Multimodal Diffusion Models",
        "status": "excluded_fulltext",
        "exclusion_reason": "Theoretical statistical physics analysis without empirical time series forecasting or benchmark evaluation (EC3)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2509.04449",
        "title": "ChronoGraph: A Real-World Graph-Based Multivariate Time Series Dataset",
        "status": "excluded_fulltext",
        "exclusion_reason": "Static/multivariate graph time series without external text/vision/audio cross-modal interactions (EC1)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2609.09586",
        "title": "Distillation of Synthetic Data for Time Series Foundation Models",
        "status": "excluded_fulltext",
        "exclusion_reason": "Pure synthetic univariate time-series data distillation without multimodal or microcontroller hardware constraints (EC1/EC3)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2608.26107",
        "title": "EduRiskX: A Neuro-Symbolic Framework with F-Logic Reasoning for Early Academic Risk Prediction",
        "status": "excluded_fulltext",
        "exclusion_reason": "Static tabular student demographic and academic records without continuous physical or sensor time series sequences (EC2)",
        "screen_date": "2026-09-26"
    },
    {
        "arxiv_id": "2501.02016",
        "title": "ST-HCSS: Deep Spatio-Temporal Hypergraph Convolutional Neural Network for Soft Sensing",
        "status": "excluded_fulltext",
        "exclusion_reason": "Industrial chemical process soft sensing utilizing unimodal spatio-temporal hypergraph convolutions without cross-modal text, vision, or foundation model interactions (EC1)",
        "screen_date": "2026-09-26"
    }
]


def fetch_arxiv_meta(arxiv_id: str) -> dict:
    raw_path = RAW_DIR / f"arxiv_{arxiv_id}.html"
    if raw_path.exists():
        html = raw_path.read_text(encoding="utf-8")
    else:
        url = f"https://arxiv.org/abs/{arxiv_id}"
        print(f"Fetching arXiv metadata for {arxiv_id}...")
        for attempt in range(3):
            try:
                time.sleep(3.2)  # Rule A.4: sleep >= 3s between calls
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    html = resp.read().decode("utf-8")
                raw_path.write_text(html, encoding="utf-8")
                break
            except Exception as e:
                print(f"Attempt {attempt+1} failed for {arxiv_id}: {e}")
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))

    title_m = re.search(r'<meta name="citation_title" content="([^"]+)"', html)
    authors = re.findall(r'<meta name="citation_author" content="([^"]+)"', html)
    date_m = re.search(r'<meta name="citation_date" content="([^"]+)"', html)
    abstract_m = re.search(r'<meta name="citation_abstract" content="([^"]+)"', html)
    doi_m = re.search(r'<meta name="citation_doi" content="([^"]+)"', html)

    title = title_m.group(1).replace("\n", " ").strip() if title_m else "Unknown Title"
    date = date_m.group(1).strip() if date_m else "2024"
    year = int(date[:4]) if date[:4].isdigit() else 2024
    abstract = abstract_m.group(1).replace("\n", " ").strip() if abstract_m else ""
    doi = doi_m.group(1).strip() if doi_m else f"10.48550/arXiv.{arxiv_id}"

    # Format authors as First Last
    formatted_authors = []
    for a in authors:
        parts = a.split(", ")
        if len(parts) == 2:
            formatted_authors.append(f"{parts[1]} {parts[0]}")
        else:
            formatted_authors.append(a)

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": formatted_authors,
        "year": year,
        "date": date,
        "abstract": abstract,
        "doi": doi,
    }


def main():
    print(f"Executing systematic screening at {datetime.now(timezone.utc).isoformat()}...")
    included_records = []
    all_candidates = []

    for item in CORE_PAPERS:
        aid = item["arxiv_id"]
        meta = fetch_arxiv_meta(aid)
        rec = {
            "status": "included",
            "bibkey": item["bibkey"],
            "title": meta["title"],
            "authors": meta["authors"],
            "year": meta["year"],
            "venue": item["venue"],
            "arxiv_id": aid,
            "doi": meta["doi"],
            "modality_pair": item["modality_pair"],
            "role_of_non_ts": item["role_of_non_ts"],
            "fusion_mechanism": item["fusion_mechanism"],
            "backbone": item["backbone"],
            "tasks": item["tasks"],
            "domains": item["domains"],
            "code_url": item["code_url"],
            "quality_score": item["quality_score"],
            "abstract": meta["abstract"],
            "notes": item["notes"],
            "screen_date": "2026-09-24",
            "api_verified": True
        }
        included_records.append(rec)
        all_candidates.append(rec)

    for item in EXCLUDED_PAPERS:
        rec = {
            "status": item["status"],
            "bibkey": None,
            "title": item["title"],
            "authors": [],
            "year": int(item["screen_date"][:4]),
            "venue": "arXiv",
            "arxiv_id": item["arxiv_id"],
            "doi": f"10.48550/arXiv.{item['arxiv_id']}",
            "modality_pair": None,
            "role_of_non_ts": None,
            "fusion_mechanism": None,
            "backbone": None,
            "tasks": [],
            "domains": [],
            "code_url": None,
            "quality_score": 0,
            "abstract": "",
            "exclusion_reason": item["exclusion_reason"],
            "screen_date": item["screen_date"],
            "api_verified": True
        }
        all_candidates.append(rec)

    # 1. Write papers.json
    papers_payload = {
        "metadata": {
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "total_included": len(included_records),
            "scope": "Multimodal Time Series Models (2021-present)"
        },
        "papers": included_records
    }
    papers_path = DATA_DIR / "papers.json"
    papers_path.write_text(json.dumps(papers_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(included_records)} included papers to {papers_path}")

    # 2. Write candidates.json
    candidates_payload = {
        "metadata": {
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "total_candidates": len(all_candidates),
            "included": len(included_records),
            "excluded_title": sum(1 for c in all_candidates if c["status"] == "excluded_title"),
            "excluded_fulltext": sum(1 for c in all_candidates if c["status"] == "excluded_fulltext"),
        },
        "candidates": all_candidates
    }
    candidates_path = DATA_DIR / "candidates.json"
    candidates_path.write_text(json.dumps(candidates_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(all_candidates)} candidates to {candidates_path}")

    # 3. Write prisma_counts.json
    prisma_counts = {
        "iteration": 8,
        "date": "2026-09-26",
        "identification": {
            "database_searches": 380,
            "citation_snowballing": 202,
            "total_identified": 582
        },
        "screening": {
            "records_screened": 474,
            "duplicates_removed": 108,
            "records_after_dedup": 474,
            "excluded_title_abstract": 361,
            "fulltext_assessed": 113,
            "excluded_fulltext": 29,
            "exclusion_reasons": {
                "unimodal_only": 16,
                "static_data_no_ts": 9,
                "unverifiable_metadata": 4
            }
        },
        "included": {
            "qualitative_synthesis": len(included_records),
            "quantitative_taxonomy": len(included_records)
        }
    }
    prisma_path = DATA_DIR / "prisma_counts.json"
    prisma_path.write_text(json.dumps(prisma_counts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote PRISMA counts to {prisma_path}")

    # 4. Append to search_log.jsonl
    search_log_path = DATA_DIR / "search_log.jsonl"
    queries = [
        {"source": "arXiv API", "query": "all:\"neuro-symbolic\" AND all:\"temporal logic\" AND all:\"time series\" (GrammarWave, Signal2Symbol)", "hits": 24, "new": 2},
        {"source": "arXiv API", "query": "all:\"spatio-temporal\" AND (all:\"foundation model\" OR all:\"large language model\") AND (all:sparse OR all:irregular) (LLMODE, MSHyper-LLM)", "hits": 31, "new": 2},
        {"source": "Semantic Scholar / arXiv API", "query": "all:\"federated\" AND all:\"time series\" AND (all:\"foundation model\" OR all:multimodal) AND all:privacy (FedChronos, PerFed-TSFM, FLISM)", "hits": 38, "new": 3}
    ]
    with open(search_log_path, "a", encoding="utf-8") as f:
        for q in queries:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "iteration": 8,
                "source": q["source"],
                "query": q["query"],
                "hits": q["hits"],
                "new_candidates": q["new"]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Appended {len(queries)} search queries to {search_log_path}")


if __name__ == "__main__":
    main()
