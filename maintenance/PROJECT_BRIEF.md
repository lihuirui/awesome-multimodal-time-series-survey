# Project brief: Survey of Multimodal Time Series Models

- Local folder: `/workspace/survey-multimodal-ts` · GitHub repo: `lihuirui/awesome-multimodal-time-series-survey`
- Working title: "Multimodal Time Series Models: A Survey and Outlook"
- Scope: models and methods that jointly use time series with other modalities (text, images/vision, video, audio, tables,
  graphs, knowledge, events/news), 2021–present. Includes: text-guided forecasting and anomaly detection, time series as
  images / vision-language models for time series, time series–language alignment and captioning, time series QA and
  reasoning with LLMs/MLLMs, multimodal time series foundation models, agents over time series, multimodal datasets and
  benchmarks. Exclude pure single-modality time series models unless they are baselines discussed for context.
- Suggested RQs: How are modalities fused (early/late/cross-attention/tokenisation/prompting)? Which tasks and domains
  benefit? What alignment/pretraining objectives exist? What datasets/benchmarks and evaluation practices are used? What
  are the failure modes and open problems?
- Taxonomy seeds (refine from data): by modality pairing; by role of the non-TS modality (context, supervision, output,
  interface); by fusion/alignment method; by task; by application domain.
- Extra figures: modality-pair × task heatmap; fusion-strategy evolution timeline; dataset landscape (size vs. modalities).
- Must cover representative lines of work (verify each via API; do not include if unverifiable): Time-LLM, GPT4TS,
  Time-MMD, TimeOmni, ChatTS, Time-VLM, VisionTS, TRACE, Sonar-TS, and newer multimodal TSFMs and reasoning models.
