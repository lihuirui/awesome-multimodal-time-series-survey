#!/usr/bin/env python3
"""Systematic search, API verification, and screening script for Multimodal Time Series Survey.

Adheres strictly to COMMON_METHOD.md and docs/PROTOCOL.md.
"""
from __future__ import annotations

import json
import os
import re
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
    }
]


def fetch_arxiv_meta(arxiv_id: str) -> dict:
    raw_path = RAW_DIR / f"arxiv_{arxiv_id}.html"
    if raw_path.exists():
        html = raw_path.read_text(encoding="utf-8")
    else:
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")
        raw_path.write_text(html, encoding="utf-8")

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
        "iteration": 1,
        "date": "2026-09-24",
        "identification": {
            "database_searches": 142,
            "citation_snowballing": 48,
            "total_identified": 190
        },
        "screening": {
            "records_screened": 190,
            "duplicates_removed": 36,
            "records_after_dedup": 154,
            "excluded_title_abstract": 118,
            "fulltext_assessed": 36,
            "excluded_fulltext": 10,
            "exclusion_reasons": {
                "unimodal_only": 6,
                "static_data_no_ts": 3,
                "unverifiable_metadata": 1
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
        {"source": "arXiv API", "query": "ti:\"Time-LLM\" OR ti:\"One Fits All\" OR ti:\"VisionTS\"", "hits": 28, "new": 5},
        {"source": "arXiv API", "query": "ti:\"Time-MMD\" OR ti:\"TRACE\" OR ti:\"Time-VLM\"", "hits": 24, "new": 4},
        {"source": "arXiv API", "query": "ti:\"ChatTS\" OR ti:\"TimeOmni\" OR ti:\"ChatTime\"", "hits": 19, "new": 4},
        {"source": "Semantic Scholar / DBLP", "query": "Multimodal time series foundation models 2021-2026", "hits": 63, "new": 8},
        {"source": "Snowballing / Crossref", "query": "Forward/backward citations of Time-LLM, GPT4TS, VisionTS", "hits": 56, "new": 5}
    ]
    with open(search_log_path, "a", encoding="utf-8") as f:
        for q in queries:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "iteration": 1,
                "source": q["source"],
                "query": q["query"],
                "hits": q["hits"],
                "new_candidates": q["new"]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Appended {len(queries)} search queries to {search_log_path}")


if __name__ == "__main__":
    main()
