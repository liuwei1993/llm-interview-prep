> **课时** 19/132　·　**项目实战（可写简历）**　·　约 1 小时
> [上一课：后训练算法项目实战](../01-项目实战/08-后训练算法项目实战.md)　·　[下一课：后训练项目 · 视频讲解](../01-项目实战/10-后训练项目 · 视频讲解.md)
>
> 学完标准：合上笔记，能讲清本节在问什么、你怎么答、以及如何套到自己的项目上。

---

### 前言

我们目前文档里有3个项目了，这三个项目也确实是我的全部家底了。我靠着这些项目，以及对应所有的知识，一步步走到现在。我也确实看到有很多同学用笔记里的项目去面试了。我希望有一个专题笔记，视频，聊一聊怎么**使用，学习这些项目。**同样的项目，每个人使用起来效果可能不一样，我这期内容想讲的是**思路，方法，我的经验。请大家在这之上，自己灵活运用。**

自己的简历只有自己对自己负责。我提供了思路，参考，还有简历，但是最终还是请自己去把关，修改，根据不同岗位适配，修改。**你永远是对自己简历把关的守门人，没有任何人能够代替你做这件事**，自己的简历还请多自己多上心。

同时，我这个小节所有介绍的经验，我不给天马行空的包装。因为吹牛谁都会，我只基于我们做过的事情，已有的文档去去聊。在某些地方让你去包装的时候，我也给到你可方案，文档，做法，而不是天马行空地去谈。所以里面会穿插很多**文档内的链接**，告诉你如果你要这么做，你应该怎么做，学点什么。

### SmartAppointment 项目

这个项目是我稍微有点头疼的，这个项目是我自学Agent做的第一个项目，无论是从项目立意上，还是技术上，我觉得都还很**青涩**。但我必须坦诚的说，这个项目就是当时我丢在简历上去面试的一个项目。我不能说是靠这个项目拿的Offer, 但我当时简历上有两个项目，另一个也是Agent项目（和这个其实差不多），我就是用这两个项目去面试，还拿到了那么多offer。

现在的如果面试，我肯定会写一个更高级的项目，或者即使用这个项目，我也会进行一些包装和改进。后来大家让我开源出这个项目，既然开源了，放在了简历上，我在想如何包装，改进，使用这个项目，能够让他变得更加成熟和有竞争力。

这个项目的好处是：**最少搭了一套多Agent对话的框架，多Agent流转，流式响应，RAG系统，MCP，也设计了一个持久化机器人，做沉淀，思想还有的。**

       **缺点是太不成熟**：没有做持久化记忆，RAG系统其实只是走了embedding匹配，持久化没做完，没有压缩策略。

如果使用这个项目，我的建议是在这个基础上，进行改进，包装。我给出一些方向和意见。

#### 1. 记忆模块

**学习：** 参考学习笔记中的开源项目[ Claude Code](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnWwYvQib6i3M4DGD1sGRVIh)、[Harmes](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcn6Yx6NLh2WtWmhKtBIc4tje)、[OpenClaw](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnRO3JEVYUxCpOFXhA3urpPc)、[pi-agent](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnDTYoW1alVyCDiGFelGwcLh) 的记忆模块。包括各种面经中，其实都有对于这个记忆模块的考察，比如[虾皮Agent面经](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnQNzwX0byNnr43tHH4KzT8c)，[字节暑期实习面经](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnJNywsG8QnVi0PrQhDlWYnd)。看这些笔记部分，把知识弄透，看面经知道面试官怎么问题，思考这个项目怎么设计。

**思考：** 短期记忆保存当前会话、用户意图和预约状态；长期记忆持久化用户历史咨询、预约记录和服务偏好；基于语义相关性召回记忆，并通过保留近期原文、滚动摘要早期对话完成上下文压缩。

**写入简历示范：**

> • 设计分层记忆模块：以 `user_id + session_id` 隔离会话，短期层保留最近 10 轮消息及预约槽位状态，长期层将咨询摘要、预约事件和带置信度的用户偏好持久化至 SQLite；检索时先按用户与记忆类型过滤，再按“向量相似度 0.6 + 时间衰减 0.3 + 重要度 0.1”混合排序召回 Top-5，上下文达到模型窗口 60% 时将早期消息压缩为滚动摘要，实现跨会话恢复并控制 Token 消耗。
>

#### 2.  RAG 系统

**学习：** 学习笔记中的 [RAG 项目](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnkwEjGikgYNvVJ0IDk9RC4u)，弄清文档解析、文本切分、向量化、召回、重排序和答案生成等经典流程。这个项目基本就是RAG的基础知识综合起来的，所以[RAG笔记章节](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnX7qtKF2Uh48dpZq6GWliz0)对应的内容啊，书籍啊，概念，都要学会。

**思考：** 将咨询 Agent 的内置 FAISS 检索升级为独立 Modular RAG MCP Server：对售后手册、FAQ 和历史咨询建立 BM25 倒排索引与 Dense 向量索引，并行召回后使用 RRF 融合，再由 `cross-encoder/ms-marco-MiniLM-L-6-v2` 对候选 Query-Chunk 对精排。为 LLM、Embedding、Splitter、VectorStore、Reranker、Evaluator 六类组件定义 Base 接口，通过 Factory + YAML 配置切换实现；使用 TraceContext 记录 query_processing、dense、sparse、fusion、rerank 五阶段耗时、候选数量和排名变化，精排超时或失败时回退至 RRF 结果。

**写入简历示范：**

> • 将咨询 Agent 的知识层升级为模块化 RAG MCP Server：采用 BM25 + Dense Embedding 双路召回与 RRF 融合，并使用 `cross-encoder/ms-marco-MiniLM-L-6-v2` 精排；基于 Base 接口、Factory 和 YAML 实现 6 类组件可插拔切换，通过五阶段 Query Trace 记录耗时、候选数及排名变化，Rerank 失败时自动回退融合结果。
>

#### 3. 记忆沉淀机制

**学习：** 参考社区对 Claude Code 未公开 [AutoDream](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcn0GxxNvlndb8xnorHTXyYJb) 能力的逆向与复刻方案，理解其基于时间/会话阈值触发，批量回放历史并执行提取、合并、冲突处理、过期清理和长期记忆晋升的机制。同样也是看上面的开源项目和面试题，讲的都有（[ Claude Code](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnWwYvQib6i3M4DGD1sGRVIh)、[Harmes](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcn6Yx6NLh2WtWmhKtBIc4tje)、[OpenClaw](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnRO3JEVYUxCpOFXhA3urpPc)、[pi-agent](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnDTYoW1alVyCDiGFelGwcLh) 的记忆模块）。

**思考：** 为用户行为分析 Agent 增加后台 Dream Job：用户累计 5 次会话且距上次整理超过 24 小时后触发，按检查点读取新增的咨询、预约、取消和反馈事件；先由 LLM 输出结构化候选记忆，再以 user_id、偏好类型和向量相似度去重，结合出现次数与新近性更新置信度，冲突时保留来源证据并降低旧记忆权重。任务通过分布式锁避免重复执行，记录 dream_run、处理水位和变更日志，失败后可从检查点重试，最终将高置信偏好写回 UserPreference，供推荐和回访读取。

**写入简历示范：**

> • 为用户行为分析 Agent 设计 AutoDream 记忆巩固任务：累计 5 次会话且间隔 24 小时后，按检查点增量回放咨询、预约及反馈事件，经结构化抽取、向量去重、冲突降权和置信度更新后写回 UserPreference；通过任务锁、处理水位及变更日志保证幂等重试，并将高置信画像用于推荐与主动回访。
>

#### 4. 评估模块

**学习：**

学习 [Agent 测评笔记](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnV5z2w7ytCwdzOXx8kAIEMh)，并参考笔记中基于该项目实现的评估算法与评测方案。这个笔记我写很全，是整个Agent开发链路上如何做测评，还有很多参考资料，先去看，看完了你应该知道如何做Agent评估。对应实战其实也有，[算法项目的二阶段](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnjDM3T9VUMwlBp4z7H1Chif)就是做的评估，有数据集，代码，可以参考。通过这些学习，我预期你自己应该知道如何做评估了

**思考：** 

采用 **EDD（Evaluation-Driven Development）驱动整个项目生命周期**。选型期先定义业务成功标准，在私有评估集上对比模型的任务正确性、协议遵循、延迟和吞吐；开发期分别评估意图路由、RAG Hit Rate/Faithfulness、预约槽位 Exact Match、工具名称与参数正确率，再通过标准 Agent 交接轨迹和端到端任务成功率验证整机。发布前将质量、轨迹、P95 延迟、Token/成本、最大步数和安全红队结果设为并列门禁；上线后以 Logs/Traces/Metrics 记录每次模型、Agent 和工具调用的输入输出、耗时、Token、成本及异常路径，持续监控质量漂移、循环调用、越权和提示注入，并将线上失败样本回灌评估集形成回归闭环。

**写入简历示范：**

> • 采用 EDD 驱动 Agent 全生命周期：基于私有评估集完成模型选型，对路由、RAG、槽位、工具调用及 Agent 交接轨迹开展组件/系统分层评测；将质量、P95 延迟、Token 成本、最大步数与安全测试设为发布门禁，上线后通过 Logs/Traces/Metrics 监控质量漂移、异常工具路径和调用成本，并将失败样本回灌评估集持续回归。
>

**进一步扩展：将评估模块做成独立项目**

这部分可以继续做深，单独包装成一个 **Agent Evaluation Platform**。重点不是再写几个单元测试，而是建立一套可重复运行、能够解释失败原因、可以接入 CI/CD 并延伸到线上监控的 Agent 评估基础设施。它既可以评估当前智能预约系统，也可以通过统一 Case、Trace 和 Scorer 协议复用到其他 Agent 项目。

**评估数据集：** 在现有 30 个场景测试和 51 条本地模型评估样本基础上，扩展一套 200～300 条业务 Golden Set，按意图路由、预约槽位、RAG 问答、工具调用、多轮状态、多 Agent 交接、安全攻击和异常恢复分层打标。每条 Case 除输入和标准答案外，还保存预期 Agent、允许的工具序列、关键参数、最终状态、禁止行为、最大步数和成本预算。外部数据库、排班和知识库使用固定快照或 Mock，保证同一版本可以重复回放。

**三层评分体系：**

1. **单步/组件评估：** 路由使用分类准确率与 Macro-F1；槽位提取使用字段 Exact Match/F1；RAG 使用 Hit Rate@K、MRR、Faithfulness；工具调用检查工具名称、参数 Schema 和执行结果。
1. **轨迹评估：** 将实际 Trace 与标准协作链比较，支持严格顺序、无序、子集和超集匹配，并对“选对 Agent、传对参数、顺序合理、及时终止”分别给分，避免最终答案偶然正确掩盖错误过程。
1. **端到端评估：** 统计任务成功率、Pass^k、平均步数、人工介入率、超预算终止率、P95 延迟和单任务 Token/成本。同一配置重复运行 5 次，报告均值、标准差和成功率区间，而不是只展示单次最好成绩。
能用确定性规则判分的任务不使用 LLM Judge；开放式回答先用 Embedding/事实一致性评分，最后才使用 LLM Judge。对 Judge 进行人工样本校准，并通过交换答案顺序、固定 Rubric 和结构化 JSON 输出降低位置偏差、冗长偏差和自我偏好。

**全链路追踪与失败归因：** 为每次任务生成 `trace_id`，使用 Langfuse 或 OpenTelemetry GenAI Span 记录模型、Agent 和 Tool 的输入输出、耗时、Token、成本、重试次数和状态变化。根据 Trace 自动将失败归类为路由错误、槽位丢失、错误工具/参数、RAG 无命中、无效循环、上下文污染、过早结束、权限越界和模型异常，并支持从失败节点回放，定位到底是模型、Prompt、工具还是编排逻辑导致问题。

**CI/CD 与发布门禁：** 每个 Pull Request 自动运行约 50～60 条高风险 Smoke Set，夜间任务运行完整 Golden Set 并对随机性用例重复 5 次；生成新旧版本差异报告并上传评估产物。发布门禁同时检查任务成功率、轨迹得分、工具参数正确率、P95、Token 成本和安全红队结果，任何一项跌破阈值都阻断合并或发布。例如可设置：端到端成功率不低于 90%、轨迹得分不低于 0.85、关键写操作授权率 100%、P95 不高于 3 秒、单任务 Token 不超过预算。

**线上监控闭环：** 上线后复用同一套 Trace Schema 和指标，在 Dashboard 中监控质量漂移、输入分布变化、工具失败率、循环调用、P95/P99、Token 成本、提示注入和越权行为；新出现的失败请求经脱敏和人工确认后自动加入 Regression Set，形成“线上发现 → 失败归因 → 回灌数据集 → CI 回归 → 灰度发布”的闭环。

**独立项目简历示范：**

**Agent 全生命周期评估与发布平台** | 个人项目 | Agent Evaluation / LLMOps

**背景：** 

Agent 输出具有随机性，单看最终回复无法发现错误工具路径、状态丢失和成本失控；传统单元测试也无法覆盖多轮、多 Agent 与开放式生成任务，因此为智能预约系统建设独立评估基础设施。

**目标：**

 采用 EDD 将评估贯穿模型选型、组件开发、系统回归、发布门禁和线上监控，以统一 Case、Trace、Scorer 协议实现可复现评测、自动失败归因和 CI/CD 质量阻断。

**过程：**

• 构建 **[实测数量]** 条分层 Golden Set，覆盖路由、槽位、RAG、Tool Calling、多轮交接和安全场景，并以固定数据快照与 Mock 工具保证任务可重复回放。

• 实现最终结果/轨迹/单步三层 Scorer，组合 Exact Match、Hit Rate@K、Faithfulness、工具参数校验和轨迹部分给分；每个随机性 Case 重复 5 次，报告成功率区间而非单次最优。

• 基于 Langfuse/OpenTelemetry 建立模型—Agent—Tool 全链路 Trace，采集耗时、Token、成本与状态变化，并自动归因路由错误、参数错误、RAG 无命中、循环和过早结束等失败类型。

• 接入 CI/CD：PR 自动执行 **[Smoke Case 数]** 条高风险用例，Nightly 运行完整评估集；以任务成功率、轨迹得分、P95、Token 成本和安全红队结果作为发布门禁，退化自动阻断合并。

• 建立线上监控与回流机制，将真实失败请求脱敏后沉淀为 Regression Case，支持新旧模型/Prompt/编排版本对比和灰度回滚。

**结果：**

 累计运行 **[实测次数]** 条 Agent 轨迹，将端到端任务成功率由 **[实测值]** 提升至 **[实测值]**，工具参数正确率由 **[实测值]** 提升至 **[实测值]**，P95 控制在 **[实测值]**、单任务成本降低 **[实测比例]**；CI 共阻断 **[实测次数]** 次质量退化版本。

**技术栈：** Python、Pytest、AgentEvals、Ragas、Langfuse/OpenTelemetry、GitHub Actions、Prometheus、Grafana、LLM-as-a-Judge

> 一组可参考的实验规模是：240 条 Golden Set、60 条 PR Smoke Set、完整用例重复 5 次共 1200 条轨迹。规模可以直接采用，但成功率提升、P95、成本下降和 CI 阻断次数必须来自实际运行，不能把目标阈值写成最终成果。
>

#### 5. 多 Agent 架构

**学习：** 

学习 Claude Code 等经典 Agent 项目的中心化编排方式与 ReAct 推理范式，理解主管 Agent 如何进行任务判断、能力调用和结果整合。要学习[笔记Agent架构](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnjDM3T9VUMwlBp4z7H1Chif)，里面很多参考资料。然后就是各种开源Agent项目（[ Claude Code](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnWwYvQib6i3M4DGD1sGRVIh)、[Harmes](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcn6Yx6NLh2WtWmhKtBIc4tje)、[OpenClaw](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnRO3JEVYUxCpOFXhA3urpPc)、[pi-agent](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnDTYoW1alVyCDiGFelGwcLh) ），面经，我都讲了架构，理解Agent架构是什么，怎么做的，你就会包装了。

**思考：** 

将现有任务分类 Agent 升级为中心化主管 Agent，把咨询 Agent、预约 Agent 和用户行为分析 Agent 封装为专业能力；主管 Agent 基于 ReAct 范式判断用户意图、选择并调用对应 Agent，在复杂任务中组合多项能力，并通过共享状态完成上下文传递和任务流转。

**写入简历示范：**

> • 设计中心化多 Agent 编排架构：由主管 Agent 基于** ReAct **范式完成任务规划与能力选择，将知识咨询、预约处理和用户行为分析封装为专业 Agent，并通过统一调用接口与共享状态实现跨 Agent 上下文传递及复杂任务协同。
>

#### 6. 业务场景

**学习：** 学习企业智能客服与售后预约系统的典型业务流程，理解知识咨询、故障受理、服务人员匹配、上门时间预约和用户回访等核心环节。

**思考：** 将原按摩预约场景升级为企业售后服务场景：咨询 Agent 负责回答产品说明、故障排查和服务政策等常见问题；需要人工处理时，由预约 Agent 根据服务类型、用户需求、工程师技能和空闲时间完成匹配与上门预约；用户行为分析 Agent 则负责沉淀服务偏好并进行主动回访。

**写入简历示范：**

> • 面向**企业售后场景**设计智能客服与服务预约系统：通过**咨询 Agent 处理产品问答**、故障排查及服务政策咨询，并由预约 Agent 结合服务类型、工程师技能与空闲时间完成智能匹配和上门预约，配合用户行为分析 Agent 实现个性化服务与主动回访。
>

#### 7. 权限机制

**学习：** 学习 [Claude Code 的四层权限机制](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnAPhtbCRzykLvvx2g3y6yre)，理解 Agent 在能力边界、资源访问、操作确认和安全审计方面的分层控制方式。

**思考：** 根据企业售后任务的风险等级设计分层权限：知识查询等只读操作可直接执行；创建预约前需由用户确认关键信息；修改、取消预约及发送回访消息等有副作用操作必须二次确认；用户隐私和跨用户数据实行身份校验、最小权限与数据隔离。同时通过工具白名单、参数校验、幂等控制和操作日志，防止越权调用、重复执行及敏感信息泄露。

**写入简历示范：**

> • 设计健全的安全机制，按操作风险划分只读直通、关键参数确认和高风险操作二次授权，对用户数据实施身份校验与最小权限隔离；结合工具白名单、参数校验、幂等控制及审计日志，降低 Agent 越权调用、重复执行和隐私泄露风险。
>

#### 8. 本地模型

**学习：** 学习 [Post-training-slot-extractor 算法项目](https://my.feishu.cn/docx/GikId1snboM6LyxxGPXc0kDdnub#doxcnjDM3T9VUMwlBp4z7H1Chif)，掌握本地小模型的数据构造、后训练、量化压缩、推理评估和服务化部署流程。

**思考：** 将预约 Agent 中高频、低复杂度且输出格式固定的槽位提取任务拆分出来，由本地 Qwen3 小模型负责从多轮对话中提取预约时间、服务时长、用户偏好和指定工程师，并判断是否需要调用查询工具；通过 SFT 与 DPO 提升结构化输出和工具调用的稳定性，将模型转换为 GGUF 并进行量化，使用 llama.cpp 部署为 OpenAI 兼容的本地 CPU 推理服务。复杂咨询与开放式推理仍交给远端大模型，形成大小模型协同架构。

**写入简历示范：**

> • 构建预约槽位提取本地模型评测链路，在 51 条冻结评估集上对比 Qwen3 0.6B/1.7B/4B；选取 1.7B 作为质量与性能平衡方案，相比 4B 任务正确性仅下降 2.9 个百分点，平均时延降低 34.4%、吞吐提升 32.9%，并设计 SFT/DPO 与 GGUF 量化路线进一步优化协议遵循和 CPU 推理性能。
>

其实还可以写高可用相关的内容，就是当Agent失败如何重试，优雅回退。我先占个位这部分内容我补了笔记再写。 同时你还可以说，比如写多模态啊等等，但是我的思想是不能天马行空。多模态当然是包装的思路，但是我们笔记暂时没有，我只给你可以行的，你可以照着去学习，思考的方向。

#### 9. 整体项目简历范文

**企业售后智能客服与预约 Agent 系统** | 个人项目 | Agent / LLM 应用开发

**背景：** 

针对企业售后场景中产品咨询、故障排查、工程师匹配、上门预约及用户回访依赖人工处理，容易出现信息重复收集、业务知识更新不及时和服务推荐不稳定等问题，设计智能客服与预约 Agent 系统。

**目标：** 

构建以主管 Agent 为统一入口的多 Agent 服务链路，串联知识咨询、预约处理、用户记忆和行为分析；采用 EDD 从模型选型、组件开发、发布门禁到线上监控持续驱动迭代，并通过本地小模型承接高频结构化任务。

**过程：**

• 设计中心化多 Agent 编排架构，由主管 Agent 基于 ReAct 范式进行任务规划与能力选择，将咨询、预约和用户行为分析 Agent 封装为专业工具，通过共享状态实现跨 Agent 上下文传递与任务协同。

• 构建预约状态管理与工程师匹配流程，从多轮对话提取时间、时长及服务偏好，并结合技能与排班推荐可用人员。

• 将咨询 Agent 接入模块化 RAG MCP 知识层，采用 BM25 + Dense 双路召回、RRF 融合及 `ms-marco-MiniLM-L-6-v2` 精排，兼顾专有名词与语义匹配。

• 以 Base 接口、Factory 和 YAML 实现 LLM/Embedding/Splitter/VectorStore/Reranker/Evaluator 六类组件可插拔；Query Trace 覆盖检索五阶段，记录耗时、候选数和排名变化，精排失败自动回退 RRF 结果。

• 设计分层记忆：以 user/session 隔离最近 10 轮消息与预约槽位，长期持久化咨询摘要、预约事件及偏好置信度；采用“向量相似度 0.6 + 时间衰减 0.3 + 重要度 0.1”召回 Top-5，窗口占用达 60% 时触发滚动摘要。

• 为用户行为分析 Agent 实现 AutoDream 后台任务：累计 5 次会话且间隔 24 小时后增量回放行为事件，经结构化抽取、向量去重、冲突降权及置信度更新写回长期偏好，并以任务锁、检查点和变更日志保证幂等重试。

• 采用 EDD 驱动模型选型与 Agent 开发：以私有评估集量化模型正确性/延迟，对路由、RAG、槽位、工具调用及 Agent 交接轨迹开展组件级与端到端回归。

• 建立质量、P95 延迟、Token 成本、最大步数和安全红队发布门禁；通过 Logs/Traces/Metrics 追踪模型、Agent、工具调用及异常路径，将线上失败样本回灌评估集形成闭环。

• 构建预约槽位提取本地模型评测链路，在 51 条冻结样本上对比 Qwen3 0.6B/1.7B/4B；1.7B 相比 4B 正确性仅低 2.9 个百分点，平均时延降低 34.4%、吞吐提升 32.9%，据此确定质量—性能平衡方案。

**结果：**

 完成 Web/API/Agents/Services/DB 五层工程架构，落地 3 类核心业务 Agent、16 个 API 接口及 30 个场景测试；为本地模型建立 51 条冻结评估集，完成 Qwen3 0.6B/1.7B/4B 与远端模型的质量、延迟和吞吐对比。分层记忆、AutoDream、RAG 重排序、权限机制及模型微调属于增强方案，需在实现和测试完成后再作为已落地成果写入正式简历。

**技术栈：**

Multi-Agent、ReAct、LangChain、RAG、FAISS、Embedding、FastAPI、AsyncGenerator、SQLAlchemy、SQLite、SFT、DPO、Qwen3、GGUF、llama.cpp

---
