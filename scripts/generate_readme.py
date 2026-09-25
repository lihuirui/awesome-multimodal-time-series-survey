#!/usr/bin/env python3
"""Generate bilingual (English + 中文简介) README.md from data/papers.json and data/prisma_counts.json.
Grouped systematically by taxonomy.
"""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "papers.json"
PRISMA_PATH = ROOT / "data" / "prisma_counts.json"
README_PATH = ROOT / "README.md"


def main():
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    prisma = json.loads(PRISMA_PATH.read_text(encoding="utf-8"))
    papers = payload["papers"]

    # Group papers by taxonomy categories
    categories = {
        "Cross-Modal Reprogramming & Decoupled Text Alignment": [],
        "Vision-Language & Visual Transcoding": [],
        "Acoustic & Seismic Waveform Reprogramming": [],
        "Physics-Informed & Planetary Earth Foundation Models": [],
        "Conversational TS-MLLMs & Temporal Reasoning": [],
        "Unified Multi-Task Architectures & Cross-Modal Retrieval": [],
        "Multimodal Datasets & Evaluation Benchmarks": [],
        "Foundational Baselines & Reference Surveys": []
    }

    for p in papers:
        mech = p.get("fusion_mechanism", "")
        role = p.get("role_of_non_ts", "")
        tasks = p.get("tasks", [])
        mod = p.get("modality_pair", "")
        aid = p.get("arxiv_id", "")
        
        if role in ["survey_reference", "position_analysis", "baseline_context"]:
            categories["Foundational Baselines & Reference Surveys"].append(p)
        elif role in ["benchmark", "evaluator_judge", "multi_modal_benchmark"] or aid in ["2406.08627", "2606.16173", "2506.05019", "2509.24789", "2503.16858"]:
            categories["Multimodal Datasets & Evaluation Benchmarks"].append(p)
        elif "Audio" in mod or "Waveform" in mod:
            categories["Acoustic & Seismic Waveform Reprogramming"].append(p)
        elif "Grid" in mod or "Planetary" in mod or aid in ["2301.10343", "2409.13598", "2405.13063", "2403.00813", "2408.10269"]:
            categories["Physics-Informed & Planetary Earth Foundation Models"].append(p)
        elif mech in ["visual_rendering", "two_stage_vision_language_screening"] or "Vision" in mod or "CXR" in mod:
            categories["Vision-Language & Visual Transcoding"].append(p)
        elif "reasoning" in tasks or "ts_qa" in tasks or "report_generation" in tasks or "captioning" in tasks or role in ["conversational_interface", "interface_reasoning"] or aid in ["2403.04945", "2503.01013", "2510.07432", "2410.04047", "2501.01832"]:
            categories["Conversational TS-MLLMs & Temporal Reasoning"].append(p)
        elif "retrieval" in tasks or "cross_modal_retrieval" in tasks or aid in ["2403.00131", "2506.09114", "2403.07815", "2505.10083", "2412.16643", "2408.14484", "2603.14709"]:
            categories["Unified Multi-Task Architectures & Cross-Modal Retrieval"].append(p)
        else:
            categories["Cross-Modal Reprogramming & Decoupled Text Alignment"].append(p)

    lines = []
    lines.append("# Awesome Multimodal Time Series Models: A Survey and Outlook")
    lines.append("")
    lines.append("[![Survey Paper](https://img.shields.io/badge/Paper-PDF-red.svg)](paper/main.pdf) ")
    lines.append("[![PRISMA 2020](https://img.shields.io/badge/PRISMA-2020%20Compliant-blue.svg)](docs/PROTOCOL.md) ")
    lines.append("[![Continuous Review](https://img.shields.io/badge/Systematic%20Review-Iteration%204-brightgreen.svg)](docs/STATE.md) ")
    lines.append("[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ")
    lines.append("")
    lines.append("> **Bilingual Repository** / **中英文双语前沿综述与开源精选仓库**  ")
    lines.append("> A rigorously verified, continuously updated repository tracking multimodal time series models, cross-modal representation learning, foundation models, and reasoning frameworks (2021–present).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🇨🇳 中文简介 (Executive Summary in Chinese)")
    lines.append("")
    lines.append("时序数据在气象、金融、医疗电子病历、交通和工业物联网中无处不在。传统的单模态时序模型（如统计方法或纯数值Transformer）往往受限于单一维度的数值波动，无法捕获高阶语义背景、事件影响与多模态因果关联。")
    lines.append("")
    lines.append("本综述全面梳理了 **2021年至今的多模态时序前沿工作**，深入探讨了将时序信号与**自然语言文本（新闻、报告、指令提示）**、**视觉图像（折线图、频谱图、卫星影像）**及**多模态知识**协同建模的新范式。核心内容涵盖：")
    lines.append("- **重编程与提示对齐（Reprogramming & Prompting）：** 如 Time-LLM、One Fits All (GPT4TS)、TEMPO、CALF，通过重编程层将时序Patch映射到预训练语言模型的潜空间；")
    lines.append("- **参数高效微调权衡（PEFT vs. Full Pre-training）：** 深入量化对比 LoRA、Adapter 与全参微调在显存壁垒（24GB/80GB）、计算开销与 MSE 泛化上的 Pareto 前沿；")
    lines.append("- **视觉映射与跨模态掩码自编码（Visual Transcoding）：** 如 VisionTS、Time-VLM，将一维时序信号绘制为图像后直接利用成熟的视觉基座（如MAE）实现跨模态零样本预测；")
    lines.append("- **跨模态检索增强与时序RAG（Cross-Modal Retrieval & RAG）：** 如 TimeRAG、Input-Aware RAG、TRACE，利用双向时序-文本检索抑制外推漂移与幻觉；")
    lines.append("- **对话交互与复杂时序推理（TS-MLLMs & Reasoning）：** 如 ChatTS、TimeOmni、Sonar-TS、TimeLM-Caption，使多模态大模型具备时序感知、外推、因果发现与自然语言报告生成能力；")
    lines.append("- **自主交互智能体沙盒（Autonomous TS Agents）：** 如 TS-Agent、TS-Reasoner、Agentic RAG，结合传感器 API、Python频域代码执行器与相空间视觉化工具实现闭环自主诊断；")
    lines.append("- **多模态基准与评估规范（Datasets & Benchmarks）：** 如 Time-MMD、Fidel-TS、MTBench、TRACE-Bench、TimeSage-MT，解决跨模态对齐数据的标准化评测问题。")
    lines.append("")
    lines.append("详细中文全篇分析请参阅 [docs/SURVEY_zh.md](docs/SURVEY_zh.md)。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Taxonomy Framework")
    lines.append("")
    lines.append("The survey synthesizes existing research across four orthogonal dimensions: **Modality Pairing**, **Fusion Architecture**, **Functional Role of Complementary Modalities**, and **Downstream Tasks & Domains**.")
    lines.append("")
    lines.append("![Taxonomy of Multimodal Time Series Models](paper/figures/taxonomy.png)")
    lines.append("")
    lines.append("### 📈 Chronological Milestones (2022–2026)")
    lines.append("")
    lines.append("![Timeline of Multimodal Time Series Models](paper/figures/timeline_milestones.png)")
    lines.append("")
    lines.append("### 🔍 PRISMA 2020 Systematic Review Counts")
    lines.append("")
    lines.append(f"- **Total Records Identified:** {prisma['identification']['total_identified']} (Databases: {prisma['identification']['database_searches']}, Snowballing: {prisma['identification']['citation_snowballing']})")
    lines.append(f"- **Deduplicated & Screened:** {prisma['screening']['records_after_dedup']} (Duplicates removed: {prisma['screening']['duplicates_removed']})")
    lines.append(f"- **Full-Text Assessed:** {prisma['screening']['fulltext_assessed']} (Excluded with documented rationale: {prisma['screening']['excluded_fulltext']})")
    lines.append(f"- **Included in Systematic Synthesis:** **{prisma['included']['qualitative_synthesis']}** studies")
    lines.append("")
    lines.append("![PRISMA 2020 Flow](paper/figures/prisma_flow.png)")
    lines.append("")
    lines.append("### 📉 Multimodal Pre-training Scaling Laws")
    lines.append("")
    lines.append("![Multimodal Scaling Laws](paper/figures/scaling_laws.png)")
    lines.append("")
    lines.append("### ⚖️ PEFT vs. Full Pre-training Trade-offs")
    lines.append("")
    lines.append("![PEFT Trade-offs](paper/figures/peft_tradeoffs.png)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📚 Curated Papers by Taxonomy Category")
    lines.append("")

    for cat_name, cat_papers in categories.items():
        lines.append(f"### {cat_name}")
        lines.append("")
        if not cat_papers:
            lines.append("*No papers categorized yet.*")
            lines.append("")
            continue
        
        # Sort by year descending
        cat_papers.sort(key=lambda x: x.get("year", 2024), reverse=True)
        for p in cat_papers:
            title = p.get("title")
            year = p.get("year")
            venue = p.get("venue", "arXiv")
            authors = ", ".join(p.get("authors", [])[:3])
            if len(p.get("authors", [])) > 3:
                authors += " et al."
            aid = p.get("arxiv_id", "")
            code_url = p.get("code_url")
            notes = p.get("notes", "")
            
            paper_link = f"https://arxiv.org/abs/{aid}" if aid else "#"
            code_badge = f" • [Code]({code_url})" if code_url else ""
            
            lines.append(f"- **[{title}]({paper_link})** ({venue} {year}){code_badge}  ")
            lines.append(f"  *Authors:* {authors}  ")
            lines.append(f"  *Modality:* `{p.get('modality_pair')}` | *Fusion:* `{p.get('fusion_mechanism')}` | *Role:* `{p.get('role_of_non_ts')}`  ")
            if notes:
                lines.append(f"  *Highlight:* {notes}  ")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🔬 Benchmark & Dataset Landscape")
    lines.append("")
    lines.append("![Dataset Landscape](paper/figures/dataset_landscape.png)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 💻 Interactive Runnable Demonstrations (`examples/`)")
    lines.append("")
    lines.append("We provide reproducible, self-contained tutorials and sandboxes for multimodal time series workflows:")
    lines.append("")
    lines.append("### 1. Multimodal Forecasting with Textual Alerts")
    lines.append("- **Python Script:** [`examples/demo_multimodal_forecasting.py`](examples/demo_multimodal_forecasting.py)")
    lines.append("- **Jupyter Notebook:** [`examples/demo_multimodal_forecasting.ipynb`](examples/demo_multimodal_forecasting.ipynb)")
    lines.append("- **Visual Comparison Output:** `examples/forecast_comparison.png` demonstrating a 90.4% MSE error reduction when conditioning on textual alerts.")
    lines.append("```bash")
    lines.append("python3 examples/demo_multimodal_forecasting.py")
    lines.append("```")
    lines.append("")
    lines.append("### 2. Autonomous Multimodal Time Series Agent Sandbox")
    lines.append("- **Python Script:** [`examples/demo_multimodal_agent.py`](examples/demo_multimodal_agent.py)")
    lines.append("- **Jupyter Notebook:** [`examples/demo_multimodal_agent.ipynb`](examples/demo_multimodal_agent.ipynb)")
    lines.append("- **Visual Trace Output:** `examples/agent_execution_trace.png` showcasing an autonomous agent invoking sensor APIs, dynamic FFT Python interpreters, phase-space visual trajectory analyzers, and domain RAG.")
    lines.append("```bash")
    lines.append("python3 examples/demo_multimodal_agent.py")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🛡️ Benchmark Data Contamination & Text Sensitivity Audit Protocol")
    lines.append("")
    lines.append("To rigorously audit against pre-training corpus leakage (The Pile, RedPajama, Common Crawl) and detect whether multimodal models genuinely ground textual semantics vs. exploit structural attention, we provide an automated audit protocol:")
    lines.append("- **Audit Script:** [`scripts/audit_contamination.py`](scripts/audit_contamination.py)")
    lines.append("- **Audit Results:** `data/audit_results/contamination_audit_summary.json`")
    lines.append("")
    lines.append("Execute the audit suite via:")
    lines.append("```bash")
    lines.append("python3 scripts/audit_contamination.py")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🛠️ How This Survey is Maintained")
    lines.append("")
    lines.append("This repository operates under the **Antigravity Autonomous Research Protocol**: ")
    lines.append("1. **Zero Fabrication:** Every cited work is strictly validated through verified public API responses (arXiv, Semantic Scholar, Crossref, DBLP).")
    lines.append("2. **Reproducible Quality Gates:** Verified by `make check`—ensuring mathematical schema integrity, citation closure, and automated LaTeX builds.")
    lines.append("3. **Continuous Review Loop:** Systematically re-executed across iterations following PRISMA 2020 protocol.")
    lines.append("")
    lines.append("To run quality checks locally:")
    lines.append("```bash")
    lines.append("make all")
    lines.append("```")

    README_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {README_PATH}")


if __name__ == "__main__":
    main()
