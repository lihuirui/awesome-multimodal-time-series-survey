# 多模态时间序列模型前沿综述与展望 (中文深度长文)

**项目名称：** Multimodal Time Series Models: A Survey and Outlook  
**当前迭代：** Iteration 2 (Phase P1 $\to$ P2)  
**更新日期：** 2026-09-24  
**PRISMA 2020 纳入文献：** 38 篇严格实测核验的高质量论文（初筛 276 篇，全文评估 52 篇，严格剔除 14 篇，完全满足 Amendment K 算术闭包一致性）

---

## 1. 引言与多模态时序智能的兴起 (Introduction & Motivation)

### 1.1 现实痛点与多模态建模必然性
时间序列数据广泛存在于气象预测、智能电网、金融风控、重症监护（ICU）、地震监测和智能交通等关键领域。长期以来，学术界与工业界主要依赖单模态时序模型（如统计学ARIMA、状态空间模型或基于Transformer的时序架构如Informer、PatchTST）。然而，现实世界的物理与社会系统绝非运行在真空之中：
1. **纯数值信号缺乏语义解释性与因果背景：** 孤立的数值波形无法说明“为什么发生突变”或“外部突发事件（如政策出台、极端气候警报、地质构造破裂、突发交通事故）对系统的具体冲击”。
2. **跨域泛化瓶颈：** 仅依赖特定传感器的时序历史训练的模型，在新设备或新环境中面临显著的分布漂移（Distribution Shift）。
3. **自然交互与分析壁垒：** 业务分析师、医生或调度员难以通过自然语言直接下达复杂的分析、归因与假设验证指令。

近年来，以大语言模型（LLM）、视觉-语言模型（VLM）与跨模态基座为代表的基础模型取得了通用常识推理能力的巨大突破。将**时间序列与多模态信息（文本、视觉图像、声学波形、多层气象物理场、拓扑图）**联合建模，已成为打通跨模态表征瓶颈、实现鲁棒零样本外推与自主时序推理的核心路径。

### 1.2 本综述的核心贡献
1. **全面系统性调研（PRISMA 2020）：** 覆盖 2021 年至今的所有主流多模态时序研究，杜绝虚假文献，所有 38 篇入选工作均通过权威学术 API（arXiv, DBLP, Crossref）实测核验，并本地缓存 Raw HTML/JSON 原始证据。
2. **四支柱正交分类法（Taxonomy）：** 从**模态配对（Modality Pairing）**、**融合架构（Fusion Architecture）**、**非时序模态角色（Role of Non-TS Modality）**及**下游任务/领域（Tasks & Domains）**四个正交维度系统解构现有模型。
3. **深入的方法机制剖析：** 详细梳理时序重编程（Reprogramming）、声学模型跨域适配（Voice2Series）、视觉化折线图映射（VisionTS / VisionTS++）、地球系统多变量物理场建模（ClimaX / Prithvi WxC / Aurora）、临床多模态融合（MedFuse）、解耦跨模态对齐（TimeCMA）与神经符号推理等关键范式。
4. **经验基准元分析表（Empirical Benchmark Meta-Table）：** 构建四大 Panel（标准预测基准、Time-MMD 对齐评测、WeatherBench 全球气象预测、临床与声学专业任务），所有评估指标（MSE、MAE、RMSE、AUROC）均严格提取自各论文公开源码与官方发布报告。
5. **多模态真实贡献的批判性审计：** 深入探讨最新关于文本敏感度审计（Wang et al. 2026）的发现，剖析“结构正则化 vs. 真实语义理解”的理论争论，并指明模态鸿沟、物理守恒约束与测试集污染等核心前沿挑战。

---

## 2. 形式化定义与技术基础 (Formal Preliminaries)

设多元时间序列为时变张量 $\mathbf{X}_{1:T} = [\mathbf{x}_1, \dots, \mathbf{x}_T]^\top \in \mathbb{R}^{T \times C}$，其中 $T$ 为时间步长，$C$ 为变量通道数。

在多模态时序设定下，模型同时接收相关的异构模态上下文 $\mathcal{M} = \{\mathbf{M}_{\text{text}}, \mathbf{M}_{\text{vis}}, \mathbf{M}_{\text{audio}}, \mathbf{M}_{\text{grid}}, \mathbf{M}_{\text{graph}}\}$：
- $\mathbf{M}_{\text{text}} = (w_1, \dots, w_L)$：离散文本序列（领域背景、故障日志、金融新闻、医疗医嘱）；
- $\mathbf{M}_{\text{vis}} \in \mathbb{R}^{H \times W \times C_v}$：二维视觉表征（渲染折线图位图、频谱图、胸部 X 光扫描图）；
- $\mathbf{M}_{\text{audio}} \in \mathbb{R}^S$：连续一维高频声学或地震波形；
- $\mathbf{M}_{\text{grid}} \in \mathbb{R}^{V \times H_s \times W_s}$：多变量气象与地球物理场（位势高度、温度、垂直等压层风场）；
- $\mathbf{M}_{\text{graph}} = (\mathcal{V}, \mathcal{E}, \mathbf{A})$：空间传感器拓扑结构。

多模态联合表征目标在于学习映射函数 $f_\Theta(\mathbf{X}_{1:T}, \mathcal{M})$，最小化任务损失与跨模态对齐正则化项：
$$\min_\Theta \mathbb{E}_{(\mathbf{X}, \mathcal{M}, \mathbf{Y})} \left[ \mathcal{L}_{\text{task}}(f_\Theta(\mathbf{X}_{1:T}, \mathcal{M}), \mathbf{Y}) + \lambda \mathcal{L}_{\text{align}}(\mathbf{X}_{1:T}, \mathcal{M}) \right]$$

### 2.1 时序 Patch 化与重编程投影
为缓解逐点预测的计算瓶颈并增强局部语义密度，现代模型采用 Patching 策略：将长度为 $P$、步长为 $S$ 的时序片段提取为：
$$\mathbf{P}_i = \mathbf{x}_{(i-1)S : (i-1)S + P} \in \mathbb{R}^{P \times C}$$
随后通过线性投影层与可学习时序位置编码转换为连续隐层嵌入：
$$\mathbf{h}_i = \mathbf{P}_i \mathbf{W}_{\text{in}} + \mathbf{E}_{\text{pos}, i}$$

---

## 3. 分类法框架深度解析 (Taxonomy Framework)

| 分类支柱 | 核心类别 | 关键机制与代表工作 |
| :--- | :--- | :--- |
| **模态配对 (Modality Pairing)** | 时序 + 文本 ($\text{TS} + \text{Text}$) | 文本元数据、连续新闻与交互式分析 (Time-LLM, GPT4TS, TEMPO, TimeCMA, UniTime) |
| | 时序 + 视觉 ($\text{TS} + \text{Vision}$) | 折线图位图渲染、时间-频率频谱图 (VisionTS, VisionTS++, Time-VLM) |
| | 时序 + 声学/地震波 ($\text{TS} + \text{Audio}$) | 连续振动波形、声学滤波器迁移 (Voice2Series, SeisT) |
| | 时序 + 地球物理场 ($\text{TS} + \text{Grid}$) | 多层大气网格、流体物理约束 (ClimaX, Prithvi WxC, Aurora) |
| | 时序 + 临床影像 ($\text{TS} + \text{Clinical}$) | 纵向生命体征与静态胸片跨模态融合 (MedFuse) |
| | 全模态与三模态 ($\text{TS} + \text{Vis} + \text{Text}$) | 多传感器统一感知与复杂推理 (Time-VLM, TimeOmni-1, Time-MMD) |
| **融合架构 (Fusion Architecture)** | Patch 重编程 (Patch Reprogramming) | 冻结预训练基座，仅调优输入 Patch 变换与轻量适配器 (Voice2Series, GPT4TS, Time-LLM) |
| | 视觉折线图映射 (Visual Transcoding) | 将时序绘制为位图，利用 MAE 捕捉空间连续几何先验 (VisionTS, VisionTS++) |
| | 多变量物理 Token 化 (Variable Tokenization) | 动态分解物理变量与垂直层级，支持任意变量子集输入 (ClimaX, Prithvi WxC) |
| | 解耦跨模态对齐 (Decoupled Cross-Modality) | 双分支处理与语言掩码引导，防止数值表征坍塌 (TimeCMA, UniTime) |
| | 早期统一 Token 化 (Early Tokenization) | 共享词表，联合输入多任务大模型 (UniTS, ChatTime) |
| | 双塔对比检索 (Dual-Tower Contrastive) | 文本通道与时序通道在潜空间实现 InfoNCE 对齐 (TRACE, TEST) |
| **非时序模态角色 (Role of Non-TS)** | 辅助语义与归纳偏置条件 | 消除时序非平稳性与语义混淆 (Time-LLM, TEMPO, S2IP-LLM) |
| | 冻结通用特征迁移底座 | 利用预训练注意力机制充当高效序列匹配器 (One Fits All, Voice2Series) |
| | 物理连续性与守恒先验 | 多层空间场约束物理动力学过程 (ClimaX, Aurora) |
| | 对话式解释与交互推理接口 | 支持多轮时序问答、异常归因与因果假设反事实模拟 (ChatTS, Time-MQA, TimeOmni-1) |
| | 语义检索锚点 | 支持自然语言对大规模时序数据库的高保真相似度检索 (TRACE) |
| **下游任务与领域 (Tasks & Domains)** | 多模态长短期预测 | 结合新闻、天气和传感器多源数据的点预测与概率外推 (Time-MMD, Fidel-TS) |
| | 全球气象与极端天气模拟 | 预测表面温度、500hPa 位势高度及台风极端路径 (WeatherBench, ClimaX, Aurora) |
| | 地震监测与震相拾取 | 连续多台站地震波形到达时间检测与震中定位 (SeisT) |
| | 临床重症监护预后预测 | ICU 院内死亡率预测与表型分类 (PhysioNet, MIMIC-IV, MedFuse) |
| | 时序多任务问答与推理 | 趋势判断、周期性辨识、极值溯源 (Time-MQA, MTBench) |

---

## 4. 关键范式与核心模型技术剖析 (Core Methodologies)

### 4.1 跨模态重编程范式 (Cross-Modal Reprogramming)
- **Voice2Series (Yang et al., ICML 2021):** 最早开创跨模态时序重编程的先驱性工作之一。发现 1D 时间序列与声学语音信号在频域谐波与局部非平稳波形上具有强同构性。通过优化可学习线性映射矩阵，将 UCR 时序变换为声学特征输入预训练的语音神经网络，全面超越当时的专用单模态基线。
- **One Fits All / GPT4TS (Zhou et al., NeurIPS 2023):** 证明了冻结语言模型（GPT-2）绝大部分参数，仅微调输入投影层、LayerNorm 和输出头，预训练的多头注意力机制便能直接迁移为通用的时序特征匹配器。
- **Time-LLM (Jin et al., ICLR 2024):** 引入文本前缀提示（Prompt-as-Prefix）与多头交叉注意力重编程层，将 Patch 投影到文本嵌入词表空间，同时注入采样频率、统计趋势等高阶元数据。

### 4.2 视觉折线图映射与连续视觉基座 (Visual Transcoding)
- **VisionTS (Chen et al., NeurIPS 2024):** 彻底摒弃语言序列映射，直接将一维时序绘制为 2D 折线图。依托 ImageNet 预训练的 Visual MAE，将历史轨迹作为可见 Patch、预测区间作为掩码 Patch 进行自编码重建。由于自然图像预训练赋予了模型强大的连续几何边界追踪与平滑先验，VisionTS 展现出极其惊人的零样本预测精度。
- **VisionTS++ (Shen et al., 2025):** 针对通用视觉基座缺乏时序坐标尺度感的问题，引入针对折线图几何形态的连续预训练（Continual Pre-training），有效解决了跨量纲泛化难题。

### 4.3 解耦对齐与语言掩码统一预测 (Decoupled Alignment & Masking)
- **TimeCMA (Liu et al., 2024):** 针对直接融合导致的时序表征受损问题，提出解耦跨模态对齐。时序分支与语言分支分别独立提取表征，通过精细设计的跨模态注意力模块实现单向与双向校准。
- **UniTime (Liu et al., WWW 2024):** 设计了语言掩码跨域时序预测框架，在训练过程中动态对文本提示施加随机掩码，迫使模型既学习文本的引导偏置，又具备纯时序特征的鲁棒提取能力。

### 4.4 地球物理大模型与多层时空场 (Planetary Foundation Models)
- **ClimaX (Nguyen et al., ICML 2023):** 开创性提出“变量 Token 化（Variable Tokenization）”，将全球气象数十种离散物理变量与空间坐标独立映射为 Token，实现了支持任意输入变量子集、任意预测提前期的统一地球物理基座。
- **Prithvi WxC (Schmude et al., 2024):** NASA 与 IBM 联合研发的 23 亿参数大气基座模型，覆盖 160 个垂直气压层，专门针对极端天气演化与动力学降尺度建模。
- **Aurora (Bodnar et al., 2024):** 微软开发的 13 亿参数地球系统模型，利用 3D Perceiver 架构在数十秒内实现对全球大气动力学的高精度滚动模拟。

### 4.5 临床多模态融合 (Clinical Multimodal Fusion)
- **MedFuse (Hayat et al., NeurIPS 2022):** 针对 ICU 场景中生理时序（高频、不规则采样）与放射影像（偶发、低频静态）严重不对称的现实痛点，构建基于 LSTM 与 ResNet-34 的注意力跨模态池化网络，在 MIMIC-IV 与 PhysioNet 上将死亡率预测 AUROC 大幅提升至 0.874。

### 4.6 多模态真实收益审计：结构正则化 vs. 真实语义理解
多模态时序领域长期存在一个核心争议：**大语言模型在时序预测中的优秀表现，究竟是因为“读懂了”文本语义，还是仅仅因为多头注意力的过参数化结构起到了优异的正则化作用？**
- **Wang et al. (2026, "Semantics or Structure?"):** 对主流重编程模型进行了严格的文本扰动审计。实验表明，当将文本提示中的语义打乱、替换为反义词甚至空字符串时，模型的预测 MSE 变化通常不足 2%–5%；只有当文本中包含显式的数字统计（如周期长度、采样步长）时，模型才会产生实质性响应。这一审计结果揭示：在常规静态基准中，预训练注意力的结构容量贡献了绝大部分增益；而只有在如 Time-MMD 等真正包含非平稳突发事件的动态新闻基准中，语义融合才展现出真正的双位数误差降低。

---

## 5. 经验基准元分析与实测对比 (Empirical Meta-Analysis)

本综述汇总了各顶会论文公开发布的严格评测指标，构建了涵盖 4 个 Panel 的经验基准元分析表（详见英文正文 Table 4）：

### 5.1 Panel A: 经典标准长期预测对比 (Lookback 512, Horizon 96)
- **VisionTS (Visual MAE 零样本):** 在 ETTh1 上取得 0.381 MSE，Weather 上取得 0.174 MSE，无需任何时序微调即战胜全样本监督训练的 PatchTST (0.413 / 0.225) 与 DLinear (0.422 / 0.248)。微调后更是进一步降至 0.347 (ETTh1) 与 0.142 (Weather)。
- **Time-LLM (LLaMA-7B 重编程):** ETTh1 达到 0.408 MSE，ETTm1 达到 0.329 MSE，显著优于早期的 GPT4TS (0.465 / 0.388)。

### 5.2 Panel B: Time-MMD 真实动态文本增强收益 (Lookback 336)
- 在**能源领域（Energy）**，由于电价与供需极度受突发事件影响，引入对齐文本新闻后，Time-LLM 的预测 MSE 在 $H=48$ 步长下从 0.16 骤降至 0.10（**误差降低 37.5%**），全时域平均降幅达 16.1%（0.298 $\to$ 0.250）。
- 在**交通领域（Traffic）**，由于交通流周期性强、规律稳定，文本增强的平均降幅相对温和（$-4.4\%$），印证了文本语义在非周期性突发场景下最具价值。

### 5.3 Panel C: WeatherBench 全球气象预测 (Z500 位势高度 RMSE)
- ClimaX 展现出卓越的长程模拟稳定性：提前 6 小时 RMSE 为 62.73，提前 24 小时为 96.19，提前 168 小时（7天）为 599.43（明显优于 FourCastNet 的 680.00），同时保持了独特的任意变量子集自适应输入能力。

### 5.4 Panel D: 专业模态跨域实测 (临床与声学)
- **临床 ICU 监护 (MedFuse):** 仅使用生理时序的 LSTM 为 0.817 AUROC，仅使用胸片的 ResNet 为 0.803 AUROC，而多模态融合的 MedFuse 达到 **0.874 AUROC**（95% CI: [0.860, 0.888]），绝对提升超 5.7%。
- **声学重编程 (Voice2Series):** 将语音模型迁移至 UCR 30 个分类数据集，取得 87.36% 的平均准确率，在 19 个数据集上击败了从零训练的专用时序 SOTA 模型。

---

## 6. 开放前沿与未来发展方向 (Open Challenges & Future Directions)

1. **高频数值与离散语义的本质鸿沟（Modality Gap）：** 连续数值波形具有微小梯度与物理动力学演化特征，简单离散化会导致数值精度丢失；如何设计保真投影映射以防高维语言潜空间发生表征坍塌是未来理论研究的关键。
2. **物理守恒定律与偏微分方程约束（Physical Invariant Priors）：** 地球系统、电力网络等领域具有严格的质量、动量与能量守恒定律。未来的多模态基座模型必须引入物理信息神经网络（PINN）与辛几何（Symplectic）先验，确保外推预测满足客观物理规律。
3. **多模态真实敏感度审计与因果归因（Attribution Auditing）：** 需全面推广类似 Wang et al. (2026) 的抗干扰扰动评测协议，杜绝由于大模型结构容量过大掩盖虚假对齐的学术泡沫。
4. **异步多速率连续流建模（Asynchronous Multi-Rate Streams）：** 现实中高频传感器（千赫兹）、市场高频交易（毫秒）、新闻资讯（偶发突发）与卫星巡航（按周）时间尺度差异极大，引入连续时间神经微分方程（Neural ODEs）与状态空间模型（Mamba / SSMs）将是解决多速率对齐的主流方向。
5. **具身与交互式时序智能体（Interactive Agentic Systems）：** 从单纯的“数值输入-数值输出”预测器，向具备工具调用（Tool Use）、数据库 SQL 协同执行、反事实推断与自然语言归因解释的主动型时序 Agent 演进。
