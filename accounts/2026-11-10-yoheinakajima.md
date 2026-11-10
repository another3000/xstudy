# @yoheinakajima（Yohei）

## 0. 元信息

| 字段 | 内容 |
|------|------|
| 平台 | X |
| 链接 | https://x.com/yoheinakajima |
| 采集时间 | 2026-11-10 ~09:20 Asia/Shanghai |
| 显示名 / handle | Yohei / @yoheinakajima |
| 开号时间 / 账号年龄 | 2009-04-11（约 17.6 年） |
| 粉丝 / 关注 / 帖量 | 127180 / 12614 / 29311 |
| 蓝标 / 认证类型 | verified=true；verified_type=blue |
| 媒体数 / listed | media≈4250；listed≈3035 |
| 备注 | 粉关比约 **10.1:1**（数字偏低，但符合 VC 白天广泛连接创始人的社交半径；近窗未见互关口号或回关话术，不按刷屏号处理）。Bio：「VC by day @untappedvc, builder by night: babyagi / @activegraphai. Build-in-public log: yohei.me」；站点 yoheinakajima.com；坐标 Seattle, WA。用户 id：`30439303`。置顶：[reintroducing untapped capital](https://x.com/yoheinakajima/status/2102419894994411599)（56173曝 / 329赞 / 书签84）。近采 25 条覆盖 2026-10-29 21:40 至 11-10 04:18 Asia/Shanghai（含部分自回帖/线程续帖，API 在 exclude replies 后仍返回了同一对话的后续层）。判定：**可学**——把失败率写进发车（循环 32/32，任务 0/24）是近窗最强资产；轻松引用和装扮玩梗有曝低藏，可作对照，不作为主食。 |

## 1. 一句话定性

BabyAGI 作者兼白天做 VC 的公开建造日志：近窗把 **Agent 循环编译进 Qwen 权重**，并公开「循环成立、智能体仍然很差」的分数；学他的失败率和附件，不学轻松玩梗的虚荣曝光。

## 2. 人设与定位

- **Bio 承诺：** 白天是 Untapped VC，晚上建造 BabyAGI / Active Graph；建造过程公开写在 yohei.me。
- **时间线实际：** 近窗主线非常集中——`babyagi-inside`：把一个有界的 Agent 循环编译进 Qwen3.5-2B 的权重，模型外部不再跑调度器。主帖写明「the agent still sucks, but the loop works」，线程里给出分数（循环 32/32 按顺序跑完并按时停；算术链 8/8，其余 0/24；普通 Qwen 在同样算术上是 5/8），并附代码、论文和 traces。几天后的跟进：Qwen3.5-4B「更好的推理解决了 2B 测试里大多数没做出来的任务」。旁支包括：病毒项目如何在 10 天窗口里催生新项目、ArXiv 从投稿到接收 68 天 vs 另一篇 4 天、对 Codex 把 Active Graph 称作 “our project”、以及一条「帮助银行安全地采用 Agent」的引用。
- **目标受众：** Agent / 权重编程研究者、开源黑客、关注早期基金的创始人。
- **差异点 / 人设钩子：** **先公布失败，再公布附件。** 「nothing runs outside the model」「same loop as 2023, minus the python」这种可核对的技术立场，比「我们做了更强的 Agent」可信得多。
- **与 Bio 的错位：** Bio 把 VC 和 builder 并列；近窗几乎全是夜间建造，基金露出主要是置顶的 Untapped 重发和一条 Zoom 整蛊创始人的轻松帖。人设没有崩，只是近窗偏向实验室日志。

## 3. 内容母题地图

近采窗口（2026-10-29 21:40 至 11-10 04:18 Asia/Shanghai）25 条（含线程续帖）。

| 母题 | 约占比 | 代表帖 | 互动摘要 |
|------|--------|--------|----------|
| 实验发车（babyagi-inside） | 高（最高曝与最高藏） | [I put BabyAGI in Qwen：循环成立，智能体仍然很差](https://x.com/yoheinakajima/status/2118134446947971336) | **17119曝** / 143赞 / **书签87** / 回复37 |
| 生态观察 | 中 | [i love how fast viral projects can trigger new projects into existence](https://x.com/yoheinakajima/status/2117482014899408898) | 8668曝 / 101赞 / 书签20 |
| 研究运营账本 | 低 | [最近一篇 ArXiv 从投稿到接收花了 68 天，上一篇只要 4 天](https://x.com/yoheinakajima/status/2118750377160175736) | 5144曝 / 37赞 / 书签12 |
| 建造者旁白 | 中 | [I just caught myself referring to activegraph as “our project” to Codex](https://x.com/yoheinakajima/status/2117360831176606171) | 5623曝 / 38赞 / 书签1 |
| 轻松玩梗/引用 | 中（低藏） | [okay so this kinda worked but I can’t breathe in it](https://x.com/yoheinakajima/status/2116227972919349646) | 6058曝 / 35赞 / 书签3 |

## 3.5 Top5 高互动帖（便于临摹）

近窗 25 条按曝光 Top5（主帖优先；线程续层单独说明）：

| # | 帖子 | 曝光 | 赞 | 回复 | 书签 | 可学钩子 / 慎学 |
|---|------|------|----|------|------|-----------------|
| 1 | [I put BabyAGI in Qwen：bounded agent loop compiled into Qwen3.5-2B](https://x.com/yoheinakajima/status/2118134446947971336) | 17119 | 143 | 37 | **87** | 书签/赞≈0.61。钩子兑现了三件事：做了什么、诚实评价（agent still sucks）、循环本身成立。后续层给出 32/32、8/8、0/24 和「code, paper, traces」。这是近窗五人里最完整的实验发车。 |
| 2 | [i love how fast viral projects can trigger new projects into existence](https://x.com/yoheinakajima/status/2117482014899408898) | 8668 | 101 | 5 | 20 | 观察而不是教程。兑现的是一种生态机制：病毒项目会在几天内催生下游项目。可学「把机制说成一句人话」，不要停在感叹。 |
| 3 | [evil qwen, weight-space programming, and qwenputer went viral in a 10-day window](https://x.com/yoheinakajima/status/2118447761012179079) | 6678 | 75 | 16 | 20 | 给近窗热潮画出时间盒（10 天）。和 #2 是同一机制的量化版：不只说「很快」，写出窗口长度。 |
| 4 | [okay so this kinda worked but I can’t breathe in it @alexandr_wang](https://x.com/yoheinakajima/status/2116227972919349646) | 6058 | 35 | 12 | 3 | 轻松实物/装扮玩梗，书签很低。有曝无藏，属于人设调剂，不是资产。 |
| 5 | [looks like we’re about to start benchmarking loyalty](https://x.com/yoheinakajima/status/2117535771242709091) | 6021 | 41 | 17 | 7 | 一句锐评。有讨论（17 回复）但可带走物不多。 |

另记可学非 Top 曝：同一线程里的 [does it work? 32/32 loop, 8/8 arithmetic, 0/24 everything else](https://x.com/yoheinakajima/status/2118134455831609470) 和 [code, paper, traces](https://x.com/yoheinakajima/status/2118134457710567888)（1449曝 / 9赞 / 书签5）——分数和附件才是主帖被收藏的原因。[Qwen3.5-4B this weekend solved most unsolved tasks from the 2B test](https://x.com/yoheinakajima/status/2119887412432355385)（2967曝 / 33赞 / 书签17，书签/赞≈0.52）是少见的诚实升级日志：告诉你换更大模型后，哪些失败被解开了。[ArXiv 68 天 vs 4 天](https://x.com/yoheinakajima/status/2118750377160175736)（5144曝 / 书签12）把研究运营写成账本，并猜测短的那篇可能只是因为投到了投稿量更小的 condensed matter 分区。

## 4. 发帖节奏与产能

- 25 条跨度约 11 天；主帖密度中等，但一次发车会拆成 5–6 层线程（原理、和 qwenputer 的对比、残差维度怎么切、循环伪代码、分数、附件）。
- 日峰值出现在 11-05 发车日（主帖 + 多层续帖 + 稍后的「viral in a 10-day window」）。
- 高峰偏北美白天（对应 Asia 深夜到次日上午）。
- 全号 29311 帖 / 17.6 年，是长线公开日志，不是为涨粉新开的号。
- 存在感来自发车线程和后续升级，而不是每天刷信息流。

## 5. 增长机制拆解

1. **互关 / 粉关比：** ≈10.1:1。关注 12614 偏多，对中文增长号会敲警钟；结合 VC 身份和 listed 3035 的专业订阅盘，近窗又没有「互关」「回关」话术，判定为**职业网络而非刷屏**。增长主力是 BabyAGI 这一类开源资产，不是关注列表。
2. **回复工时：** 中。发车帖 37 回复，他用线程自答「does it work / how / code」——把评论区可能问的问题提前写进楼层。
3. **钩子话术：** 婴儿 emoji 和「I put BabyAGI in Qwen」这种具体动作；紧接着自砸：「the agent still sucks」；用 32/32、8/8、0/24 这种可复核分数代替形容词。
4. **书签型 vs 虚荣赞：** 发车主帖书签/赞≈0.61，4B 升级≈0.52；「can’t breathe」6058 曝 / 书签 3，「our project to Codex」5623 曝 / 书签 1。轻松旁白能维持人味，存不下来。
5. **权威资产：** 2023 年的 BabyAGI 原循环、这次的权重内循环、代码/论文/traces、yohei.me 日志、Untapped Capital。他明确写「no scheduler, no parser, no tool executor」——限制条件本身就是资产。
6. **跨平台 / 漏斗：** GitHub / 论文 / yohei.me / 基金站点。漏斗是：实验钩进场 → 分数和附件收藏 → 代码或基金站点。几乎看不到硬广。
7. **其他：** 「helping banks adopt agents safely」说明他知道 Agent 进入受监管行业要先谈安全；这条只有 3464 曝、书签 0，提醒我们：**正确的企业主题如果只点题不给步骤，一样存不下来**。

## 6. 爆款与平帖对比

| | 爆款（可学面） | 平帖 / 对照 |
|--|------|------|
| 链接 | [babyagi-inside 发车](https://x.com/yoheinakajima/status/2118134446947971336) | [I can’t breathe in it](https://x.com/yoheinakajima/status/2116227972919349646) |
| 结构特征 | 动作 + 诚实评价 + 分层分数 + 附件 | 图片玩梗 + @ 名人 |
| 情绪 / 数字 / 图 | 17119曝 / 书签87 | 6058曝 / 书签3 |
| 差异结论 | **失败率和附件会被想复现的人存下来**；好玩的现场只维持温度 |

更细的对照在线程内部：只说「loop works」不够，写出 32/32 和 0/24，读者才知道该不该跟上。

## 7. 可学习清单（→ 微李玩AI / LIS / AI入企 / 小程序）

1. **交实验必带失败率** → LIS / AI入企：试点不要只报「模型能跑通」。写成「规则循环 32/32 跑完，字段抽取对了 X/Y，其余失败集中在哪些字段」。
2. **附件三件套** → 微李玩AI：对照 code / paper / traces，我们发案例时带上提示词、前后样本、失败例子。
3. **先说限制条件** → 「nothing runs outside the model」「same loop as 2023, minus the python」。院内方案先写「这次没有调度器 / 没有外挂工具 / 只在这些数据上测过」。
4. **升级日志对着上次的失败项写** → 4B「解决了 2B 测试里大多数没做出来的任务」。版本更新不要列举新功能，要对着上一版失败清单打勾。
5. **给热潮加上时间盒** → 「viral in a 10-day window」。观察行业时写出窗口，而不是「最近很火」。

## 8. 风险与不该学

- 关注 1.2 万这个数字本身不必模仿；中文专业号维持高粉关比仍然更稳。
- 「agent still sucks」这种自砸在研究圈加分，对医院客户要改成「循环稳定、抽取准确率仍低，所以我们先只用于辅助、不自动写报告」——诚实，但不消遣。
- 装扮玩梗、海盘生日、工具域名吐槽可以偶尔出现，成主食就会把建造日志冲淡。
- 企业安全主题（银行采用 Agent）如果只点题，效果接近空气；要么展开步骤，要么别发。

## 9. 对我们的行动建议

1. 本周发 1 条 **带分数的试点日志**：某 LIS/质控任务的通过项、失败项、样本数，对照 32/32 与 0/24。
2. 同一条下贴出 **提示词 + 前后样本 + 失败例子**，相当于他的 code / paper / traces。
3. 人审红线：**禁止用「效果很好」代替分数**；升级必须写清解开了上一版的哪几条失败。

## 10. 附录

- 数据源：`get_users_by_usernames` + `get_users_posts`（exclude retweets,replies；单页最多 25 条，本号返回 25 条，含同一对话的续层；最近一条 2026-11-10 04:18 Asia/Shanghai；`next_token` 指向更早帖，未再翻页）；关键长帖与置顶用 `get_posts_by_ids` 核对。采集 2026-11-10 ~09:20 Asia/Shanghai；用户 id：`30439303`。
- 判定说明：可学。粉关比偏低但按 VC 职业网络理解，不标互关刷屏。Top5 按曝光，另标出线程内分数帖与 4B 升级帖。
