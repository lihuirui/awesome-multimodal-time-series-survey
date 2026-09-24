# 多模态时间序列模型前沿综述与展望 (中文概要)

**项目名称：** Multimodal Time Series Models: A Survey and Outlook  
**当前迭代：** Iteration 1 (Phase P0 $\to$ P1)  
**更新日期：** 2026-09-24  

---

## 1. 引言与研究背景 (Introduction & Motivation)

### 1.1 现实痛点与多模态动机
时间序列数据广泛存在于气象预测、智能电网、金融风控、医疗生命体征监测和智能交通等关键领域。长期以来，学术界与工业界主要依赖单模态时序模型（如统计学ARIMA、状态空间模型或基于Transformer的时序架构如Informer、PatchTST）。然而，现实世界的动态系统具有高度的复杂性：
1. **纯数值信号缺乏语义解释性：** 孤立的数值波形无法说明“为什么发生突变”或“外部突发事件（如政策出台、极端气候警报、突发事故）对系统的具体冲击”。
2. **跨域泛化瓶颈：** 仅依赖特定传感器的时序历史训练的模型，在新设备或新环境中面临显著的分布漂移（Distribution Shift）。
3. **自然交互与分析壁垒：** 业务分析师、医生或调度员难以通过自然语言直接下达复杂的分析、归因与假设验证指令。

近年来，以大语言模型（LLM）和视觉-语言模型（VLM）为代表的基础模型在文本与视觉领域取得了通用常识推理能力的巨大突破。将**时间序列与多模态信息（文本、视觉图像、拓扑图、表格事件）**联合建模，已成为打通跨模态表征瓶颈、实现鲁棒零样本外推与自主时序推理的核心路径。

### 1.2 本综述的核心贡献
1. **全面系统性调研（PRISMA 2020）：** 覆盖 2021 年至今的所有主流多模态时序研究，杜绝虚假文献，所有入选工作均通过学术 API（arXiv, DBLP, Crossref）实测核验。
2. **多维正交分类法（Taxonomy）：** 从**模态配对（Modality Pairing）**、**融合架构（Fusion Architecture）**、**非时序模态角色（Role of Non-TS Modality）**及**下游任务/领域（Tasks & Domains）**四个正交维度系统解构现有模型。
3. **深入的方法机制剖析：** 详细梳理时序重编程（Reprogramming）、跨模态对齐（Contrastive Alignment）、视觉化映射（Visual Transcoding）、统一指令微调与神经符号推理等关键范式。
4. **多模态基准与未来挑战：** 总结 Time-MMD、Fidel-TS、MTBench 等最新基准，并指明模态鸿沟（Modality Gap）、高频语义失真、测试集污染及因果可信度等核心开放课题。

---

## 2. 形式化定义与技术基础 (Formal Preliminaries)

设时间序列为多元时变张量 $\mathbf{X}_{1:T} = [\mathbf{x}_1, \dots, \mathbf{x}_T]^\top \in \mathbb{R}^{T \times C}$，其中 $T$ 为时间步长，$C$ 为变量通道数。

在多模态时序设定下，模型同时接收相关的异构模态上下文 $\mathcal{M} = \{\mathbf{M}_{\text{text}}, \mathbf{M}_{\text{vis}}, \mathbf{M}_{\text{graph}}\}$。
多模态联合表征目标在于学习映射函数 $f_\Theta(\mathbf{X}_{1:T}, \mathcal{M})$，最大化互信息或最小化下游任务经验风险：
$$\min_\Theta \mathbb{E}_{(\mathbf{X}, \mathcal{M}, \mathbf{Y})} \left[ \mathcal{L}_{\text{task}}(f_\Theta(\mathbf{X}_{1:T}, \mathcal{M}), \mathbf{Y}) + \lambda \mathcal{L}_{\text{align}}(\mathbf{X}_{1:T}, \mathcal{M}) \right]$$

### 2.1 时序 Patch 化与重编程投影
为了将连续高频数值映射到离散语义空间，主流方法采用 Patching 机制，将长度为 $P$ 的非重叠或步长为 $S$ 的时序片段线性映射为 Token 嵌入：
$$\mathbf{H}_i = \text{LinearProj}(\mathbf{x}_{(i-1)S : (i-1)S + P}) + \mathbf{E}_{\text{pos}}$$
随后通过可学习重编程层（Reprogramming Layer）将 $\mathbf{H}_i$ 映射至预训练语言模型（如 LLaMA、GPT-2）的文本嵌入空间。

---

## 3. 分类法框架解析 (Taxonomy Framework)

| 分类维度 | 核心类别 | 代表工作 |
| :--- | :--- | :--- |
| **模态配对 (Modality Pairing)** | 时序 + 文本 (TS + Text) | Time-LLM, One Fits All, TEMPO, CALF, ChatTS, TimeOmni |
| | 时序 + 视觉 (TS + Vision) | VisionTS, Time-VLM |
| | 时序 + 视觉 + 文本 (Tri-modal) | Time-VLM (Augmented Learner) |
| | 全模态基准 (Omnimodal Benchmark) | Time-MMD, Fidel-TS, MTBench |
| **融合架构 (Fusion Mechanism)** | Patch 重编程 (Patch Reprogramming) | Time-LLM, GPT4TS, AutoTimes |
| | 视觉渲染 (Visual Rendering & MAE) | VisionTS |
| | 早期统一 Token 化 (Early Tokenization) | UniTS, ChatTS, ChatTime |
| | 双塔对比对齐 (Dual-Tower Contrastive) | TRACE, TEST |
| | 纯文本提示序列化 (Text Serialization) | PromptCast, LLMTime |
| **非时序模态角色 (Role of Non-TS)** | 辅助上下文条件 (Auxiliary Context) | Time-LLM, TEMPO, S2IP-LLM |
| | 冻结特征提取基座 (Frozen Substrate) | One Fits All (GPT4TS) |
| | 对话与交互推理接口 (Conversational Interface) | ChatTS, TimeOmni-1, Sonar-TS |
| | 跨模态检索与对齐锚点 (Metric Anchor) | TRACE |

---

## 4. 关键模型机制深度剖析 (Core Methodologies)

### 4.1 时序 Patch 重编程与前缀微调 (Reprogramming Paradigms)
- **Time-LLM (Jin et al., ICLR 2024):** 保持基础语言模型（LLaMA/GPT-2）参数完全冻结，设计可学习的时序重编程层，将 Patch 序列转换为重编程文本 Token，同时在输入端前缀拼接数据集描述与先验提示（Prompt-as-Prefix），显著降低了调优开销并实现了优异的跨域少样本预测。
- **One Fits All / GPT4TS (Zhou et al., NeurIPS 2023):** 证明了即便不对语言模型做大规模微调，只微调轻量级的线性 Patch 输入输出映射层和 LayerNorm，预训练的 GPT-2 就能在预测、分类、异常检测和插补等所有时序下游任务上全面超越从零训练的专用深度模型。
- **AutoTimes (Liu et al., NeurIPS 2024):** 引入文本时间戳嵌入，将自回归 LLM 直接转化为因果时序预测器，仅微调 0.1% 参数量即可实现任意长度的上下文预测。

### 4.2 视觉映射与无监督图像掩码（Visual Transcoding）
- **VisionTS (Chen et al., NeurIPS 2024):** 提出了“视觉免费午餐”假说：将数值时序信号绘制为高保真折线图后，直接喂入在自然图像（ImageNet）上预训练的视觉掩码自编码器（MAE）。实验发现，视觉注意力天然擅长捕捉周期性、趋势与局部异常，甚至无需时序域数据微调即可取得强大的零样本预测性能。
- **Time-VLM (Zhong et al., ICML 2025):** 联合时间、视觉和文本三模态，构建双分支增强学习器，在频域和多尺度卷积空间内与 VLM 协同学习。

### 4.3 对话式时序大模型与复杂推理（TS-MLLMs & Reasoning）
- **ChatTS (Zhao et al., VLDB 2025):** 针对多模态时序问答数据匮乏的痛点，构建了“Time Series Evol-Instruct”合成微调体系，使模型具备了原生理解多元数值与多轮深度推理的能力。
- **TimeOmni-1 (Tan et al., 2025):** 建立感知（Perception）、外推（Extrapolation）和决策（Decision-making）三阶段课程训练体系，引入强化学习以激发因果反事实推断。
- **Sonar-TS (Tan et al., ICML 2026):** 面向超大规模时序数据库（TSDB），提出“搜索-验证”（Search-Then-Verify）神经符号框架，打破了传统 Text-to-SQL 难以处理复杂时序波形意图的技术瓶颈。

---

## 5. 数据集与基准评测态势 (Benchmark Landscape)

1. **Time-MMD (Liu et al., NeurIPS 2024):** 涵盖金融、交通、气象、健康、电力等 9 大领域，提供数值序列与事件文本新闻的高质量细粒度对齐，成为目前最为公认的多模态预测基准。
2. **Fidel-TS (2025):** 针对现实中存在的多模态噪声和模态缺失问题，提出了高保真度抗干扰评测标准。
3. **MTBench (2025):** 专门评估多模态大模型在时序因果问答、时序推理逻辑与反事实分析上的评测套件。

---

## 6. 开放挑战与前沿展望 (Challenges & Future Outlook)

1. **高频数值与离散语义的本质鸿沟（Modality Gap）：** 连续数值对微小扰动极度敏感，而语言模型词表离散化往往平滑了高频极端事件，如何实现保真量化仍是未解难题。
2. **模态缺失与异步采样（Asynchronous & Incomplete Modalities）：** 实际场景中文本或图像通常是非周期的（如只有发生突发新闻时才有文本），如何在文本缺失时自适应退化并保持预测稳定性至关重要。
3. **评测基准泄漏与虚假泛化风险（Data Leakage & Evaluation Pitfalls）：** 很多 LLM 预训练语料库中已包含常见公开时序数据集的统计描述，严格的零样本划分与污染检测机制亟待统一。
4. **边缘计算与部署开销（Compute & Latency Bottlenecks）：** 7B/13B 大模型在毫秒级时序控制（如电网秒级调度）中延迟过高，开发轻量化参数高效模型（如 TTM）是产业落地的关键。
