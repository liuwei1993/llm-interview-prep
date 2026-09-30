> **课时** 52/132　·　**Agent 八股**　·　约 40–45 分钟
> [上一课：10. 大模型幻觉](../04-Agent/16-10. 大模型幻觉.md)　·　[下一课：11.3 Openclaw 记忆](../04-Agent/18-11.3 Openclaw 记忆.md)
>
> 学完标准：合上笔记，能讲清本节在问什么、你怎么答、以及如何套到自己的项目上。

---

## 11 开源框架解读  - Openclaw

（写于2026年3月份）OpenClaw一定是一个必考的问题，大模型应用岗位，产品岗，必须得会。原因很简单，我想先和大家讲清楚这里面的底层逻辑，为什么会考。 因为他是目前最热门的AI Agent产品了。在这个大模型高速发展的时代，热门的东西一定是要了解会考察的。 有人说2025年是Agent年，从2025发展到现在，Agent的形式在不断演进。火爆出圈的Agent从去年的Manus到今年的Openclaw, 它是整个行业发展的风向标。 我回想去年（2025年）面试的时候，很多面试官问我Manus是什么，我说不知道，当时觉得没啥，现在觉得很掉分。对于行业爆品，一定要掌握，是高频考点。网上很多视频基本都是讲的Openclaw如何配置，有什么能力。相关视频太多了，在本章我会给大家推荐2个我自己看的部署，玩openclaw的视频，感兴趣可以去玩。 但是本章更侧重的是Openclaw的原理，技术，为什么出圈。讲的人不多，但是作为开发，或者产品，从面试的角度，你无疑是要掌握这个产品里面包含的核心技术的，本节就从功能，技术层面来讲解Openclaw, 相信他一定是你准备面试必不可少的素材。学了本章，你可以在面试的时候和面试官说你看过Openclaw的源码（其实也有必要看，作为Agent开源项目），Manus其实也可以去学习，因为他也是很火的Agent，而且和Openclaw 侧重点是不同的。可以当作课外作业大家自己去学一下。

### **11.1 OpenClaw是什么**

（一定会问的问题，一般面试官引入一个问题都是先问你概念，所以精心准备一个表达流畅的回答是非常必要的）

 OpenClaw 是一个开源的、可自托管的**个人 AI 助手平台**。

- 核心用 TypeScript (ESM) 编写，运行在 Node.js 22+ 上
- 通过 `npm install -g openclaw` 安装，`openclaw` CLI 是主要入口
- 所有数据和密钥都存在本地（`~/.openclaw/`），不经过任何云中转
总结来说，**它是一个事件驱动的 Agent 执行引擎，前面放了一个多渠道网关。**

### 11.2 Openclaw 总体架构

（这节很核心哈，我结合这个架构图，然后把各个模块功能都讲清楚，你学明白了其实你就知道了它到底是个啥东西，为啥看上去很神奇很主动？Openclaw神秘的面纱就揭开了）

简单来讲，OpenClaw 的架构为**触发、网关、Agent 三层**：

- **触发层**负责产生事件 — 五种来源（消息、心跳、定时任务、钩子、Webhook）不断向系统注入事件
- **网关层**负责接入和路由 — 把不同协议的事件统一收进来，认证后分发到正确的 Agent 会话
- **Agent 层**负责智能执行 — 推理（Think）、调工具（Act）、记忆（Remember）
三层的本质是一个**事件驱动的执行管道**：事件产生 → 网关路由 → Agent 消费执行 → 状态持久化 → 等待下一个事件。这是一个永不停止的循环。

![image.png](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/preview/Kz1yblVZ7oKRWSxI94FcCpxannb)

#### **11.2.1  触发层 - 5层信号源**

Agent 不是只在用户发消息时才工作。OpenClaw 有**五种独立的触发维度**，每一种都能唤醒 Agent 执行：

通过上述图片，我们知道它触发的方式很多，我们通常给他发消息其实只是一种（Message）。不过Message可以触发的方式也很多：通过CLI，通过应用（feishu,telegram), 包括Openclaw的dashboard。 所以其实看上去openclaw好像一直在思考，很主动，其实不过是有记忆功能加上 自动的触发源罢了。（最后我会举例说明）

![image.png](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/preview/KJg4bhXUQofIJcxiHxUcH8NvnPc)

#### **11.2.2 网关 - 大名鼎鼎的Gateway**

Gateway 是一个**本地长驻 Node.js 进程**，监听端口 `:18789`（HTTP + WebSocket），是触发层和 Agent 层之间的**中间件**。

![image.png](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/preview/MryqbUU3GovKrixP9o6cpjWmndd)

**Gateway 的核心职责：连接管理、协议转换、路由分发、安全控制。**

**关键边界：Gateway 不做推理，不调 LLM，不执行工具。** 它只负责"消息到了该给谁"和"回复该送回哪里"。

#### 11.2.3 Agent层 

这层就是咱们熟悉的Agent的知识啦。React, LLM 的调用，Function Call, Memory都在这里啦~都是我们学过的知识啦~~。

##### 11.2.3.1 推理 (think)

Agent 的核心是 **Pi Embedded Agent**，一个多轮推理循环。它收到消息后开始思考，决定是直接回复还是需要调用工具获取更多信息，调完工具拿到结果后继续思考，如此循环直到生成最终回复。

推理过程中需要调用 LLM。LLM 调用是从本地 Gateway 进程直接发往模型提供商 API 的（OpenAI、Anthropic、Gemini、Ollama 等），不经过 OpenClaw 的任何云服务。如果用 Ollama 等本地模型，整个流程甚至完全不出你的局域网。

**Auth Profiles** 管理多套 API 凭证，支持轮换和 failover——一个 key 被限速了会自动切到下一个。**Session Manager** 维护多轮对话的上下文，当历史过长时自动压缩（compact），管理 token 预算。

##### 11.2.3.2 工具执行 (Act)

Agent 推理时可以自主决定调用工具。内置的核心工具包括：

- **exec** — 执行 Shell 命令，有 allowlist 安全策略控制哪些命令可以运行
- **browser** — 通过 CDP 协议控制 Chromium 浏览器，可以浏览网页、截图、操作页面
- **message** — 向任意渠道发送消息，实现跨渠道通信
- **nodes** — 远程调用已配对的 iOS/Android 设备上的能力
- **subagents** — 启动子 Agent 并行处理复杂任务
- **apply_patch** — 修改代码文件
除了内置工具，插件也可以通过 `registerTool` 注册额外的工具，能力可以无限扩展。

##### 11.2.3.3 记忆(Memory)

记忆是 Agent 主动调用的，不是每次对话都自动塞入上下文（那样会浪费 token）。Agent 自己判断"需不需要回忆过去的信息"，然后调用 `memory_search` 工具进行混合检索——70% 权重给向量语义搜索，30% 权重给 BM25 关键词搜索（**哇，这不是我们自己的RAG项目的稀疏向量和稠密向量双路检索吗~**）。找到相关结果后，再通过 `memory_get` 读取完整的记忆内容。

底层存储是一个 SQLite 数据库，同时维护向量 embedding 索引和全文索引。记忆的原始数据是 Markdown 文件（MEMORY.md 以及自动生成的会话摘要文件）。

记忆的写入有两种方式。第一种是自动捕获：当会话结束时（用户输入 `/new` 或 `/reset`），hook 会自动把最近的对话保存为 `memory/YYYY-MM-DD-slug.md` 文件。第二种是文件同步：用户手动编辑 MEMORY.md 或 memory 目录下的文件，chokidar 文件监听器检测到变化后，自动进行分块、计算 embedding、写入索引库。

#### 11.2.4 总结&举例

朋友们，所以你看，Openclaw其实也没有什么特别大不了的对吗？比如Agent模块，我们的描述并不复杂，没有用什么深奥的技术。如果你看完了我这个笔记Agent，我相信你很容易理解，所以OpenClaw本身也没啥大不了的对吧。我在这一节再给大家用实际例子来讲解，其实他就是这么回事~.

**先总结**，OpenClaw的本质是**事件驱动模型**，看起来主动是有定时任务以及间隔触发，看起来能记事是因为有记忆，采用双路检索。看上去功能强大，可以用应用驱动是因为用了Gateway做适配。快速总结：

Time    → Heartbeats, Crons

Humans   → Messages

External   → Webhooks

Internal   → Hooks → Queue → Agent Executes → State Persists

Agents     → Subagents

**再举例：**一个外国小哥哥使用了Openclaw，然后发帖说他给他的妻子用Openclaw设置了定时发送早上好，结果晚上回去，他发现他的龙虾和妻子从早聊到晚，他的妻子完全不知道对面不是真人。他觉得太amazing了。我们现在知道，他看上去主动的原因是，因为你设置了定时器，然后还有间隔触发。Agent每次触发，会根据上下文，思考调用工具比如可以打电话，发新闻，图片。所以整体看上去你没和它主动聊天，他也会和你说话甚至会打电话。无非是这么实现的。

![image.png](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/preview/Zokqb35jfo0Lr7xj6Tjc0x9Anhc)
