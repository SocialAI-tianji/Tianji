# 天机 Tianji
<p align="center">
    <img src="./assets/tianjilogo.jpg" width="100"/>
<br>
<p align="center">
    &nbsp<a href="README.md">中文</a>&nbsp ｜ &nbsp<a href="README_en.md">English</a>&nbsp ｜ &nbsp<a href="README_jp.md">日本語</a> 
<p align="center">
   <a href="https://python.org/" target="_blank"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/moelib?logo=python&style=flat-square"></a>
   <a href="https://github.com/tatsu-lab/stanford_alpaca/blob/main/LICENSE"><img alt="LICENSE" src="https://camo.githubusercontent.com/ff42248868bc1387751598955e573b397851d947f13ddd7618c0ba9e66aacdf6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f436f64652532304c6963656e73652d4170616368655f322e302d677265656e2e737667"></a>
   <br/>
</p>

天机是 SocialAI（来事儿AI）制作的一款免费使用、非商业用途的人工智能系统。您可以利用它进行涉及传统人情世故的任务，如`如何敬酒、如何说好话、如何会来事儿`等，以提升您的情商和核心竞争能力。我们坚信，只有人情世故才是未来AI的核心技术，只有会来事儿的AI才有机会走向AGI，让我们携手见证通用人工智能的来临。 —— "天机不可泄漏。"

Tianji is a free, non-commercial artificial intelligence system. You can utilize it for tasks involving worldly wisdom, such as "art of conversation," to enhance your emotional intelligence and core competitiveness. We firmly believe that worldly wisdom are the future core competency of AI, and let us join hands to witness the advent of general artificial intelligence.

天機は SocialAI（来事儿AI）が制作した無料で非商業目的の人工知能システムです。伝統的な人間関係や世事に関連するタスク、例えば「乾杯の仕方」「上手な話し方」「人付き合いの仕方」などに活用でき、あなたの情緒的知性とコア競争力を向上させることができます。私たちは、人間関係や世事こそが将来のAIの核心技術であり、人付き合いの上手なAIだけがAGIに向かう機会があると固く信じています。一緒に汎用人工知能の到来を見届けましょう。 —— 「天機は漏らすべからず。」

</p>
</br>
</p>

## 你将在天机中学会 🍉

- 构建 [prompt](./tianji/prompt/gpt_prompt/) 对话[大模型应用](./run/tianji_prompt_webui.py)

- 制作 [AI 游戏](./tianji/prompt/aigame/zhipu/)（类似哄哄模拟器）应用

- 基于 [metagpt](./tianji/agents/metagpt_agents/) 构建[智能体应用](./run/metagpt_webui.py)  （即将重构）

- 从零构建一个[知识库对话应用](./tianji/knowledges/) （即将重构）

- [从零制作数据](./docs/finetune/how-to-get-finetune-data.md)、[微调](./docs/finetune/how-to-get-finetune-data.md)属于自己的大语言模型

**学完全部内容后，你将获得大语言模型入门级全栈应用开发能力。🕶️**

</p>
</br>
</p>

[SocialAI（来事儿AI）](https://socialai-tianji.github.io/socialai-web/) 是设立于中国的非营利组织，我们完全开源了**Tianji**（天机）系列工作，当前开源系统技术路线涉及为[Prompt](tianji/prompt/yiyan_prompt)、[AI游戏](test/prompt/aigame/zhipu)、[Agent](tianji/agents)、知识库、[模型训练](docs/finetune/tianji-wishes-chinese.md)。具体内容，请查看文档与对应仓库。

基于整理后的人情世故数据，人情世故大模型系统-天机包括了常见人际交往中的七大领域（具体可以参考 [场景分类](test/场景分类) 中的场景细化细节），其中大体可分为：

```
1.敬酒礼仪文化 Etiquette
  不惧碰杯，酒席桌上一条龙
2.请客礼仪文化 Hospitality
  友好地展示你的友好
3.送礼礼仪文化 Gifting
  此礼非礼，直击人心
4.送祝福 Wishes
  承包你的所有祝福语
5.如何说对话 Communication
  据说是低情商救星
6.化解"尴尬"场合 Awkwardness
  没心没肺，找回自我
7.矛盾&冲突应对 Conflict
  《能屈能伸》  
```

结合这些领域，Tianji涉及到的技术路线共有四种：

- 纯prompt（包括AI游戏）：内置 system prompt 基于大模型自身能力对话。
- Agent（MetaGPT等）：利用 Agent 架构的得到更丰富、更定制化详细的回答。
- 知识库：直接检索人情世故法则（比如餐桌上一般怎么喝酒）。
- 模型训练：基于不同优秀的模型基座，在积累大量数据的情况下进行Lora微调或全量微调。

您可以在 tianji 目录下找到四种路线的对应源码，如果您想参考 `Tianji` 的项目架构、数据管理、技术路线复刻出属于自己的垂直领域 AI 应用，欢迎 fork 或者直接参考，我们将会开源所有包括从`项目的起步、数据的方向探索、数据构建与管理、AI应用从0制作、领域（比如人情世故）与技术路线的深入结合`的全过程；我们希望看到 AI 原生应用在生活中进一步的加速推进。

如果您想提建议 / 参与这个项目的开发流程，欢迎加入社区群！

![image](./assets/tianji-wechat.jpg)

## 目录
- [News](#📰News)
  - [路线图](#路线图)
- [运行环境](#运行环境)
  - [环境安装](#环境安装)
  - [key配置](#key配置)
- [文件目录说明](#文件目录说明)
  - [文档说明](#文档说明)
- [运行方式](#🍺运行方式)
  - [示例](#示例)
- [如何参与本项目](#如何参与本项目)
  - [问题看板](#问题看板)
  - [提交第一个PR](#提交第一个PR)
- [如何复刻本项目](#如何复刻本项目)
- [贡献者](#贡献者)
- [鸣谢](#鸣谢)

## 📰News

- **[2024.07.14]** 更新了新版的[送祝福模块](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Wishes) 支持更多风格切换，数据已开源至 [huggingface](https://huggingface.co/datasets/sanbu/tianji-chinese/blob/main/tianji-wishes-chinese-v0.1.json)

- **[2024.05.04]** 🚀 我们发布了以《化解"尴尬"场合》为例的[微调数据获取、制造教程](https://github.com/SocialAI-tianji/Tianji/blob/main/docs/finetune/how-to-get-finetune-data.md)，对应数据开源至 [huggingface](https://huggingface.co/datasets/sanbu/tianji-chinese/tree/main)

- **[2024.05.02]** 🚀 我们发布了有关人情世故大模型-送祝福的数据收集到微调过程的[全流程可复现文档](./docs/finetune/tianji-wishes-chinese.md)及其对应[数据](https://huggingface.co/datasets/sanbu/tianji-chinese/tree/main)、[配置](./tianji/finetune/xtuner/internlm2_chat_7b_qlora_oasst1_e3_copy.py)、[辅助脚本](./tools/finetune/README.md)，（鸽了一段时间但又回来了，主要维护者持续加班忙了，放假才能快乐开源）

- **[2024.02.01]** 🧑‍🚀 我们发布了有关 [prompt](http://120.76.130.14:6006/prompt/)、[Agent应用](http://120.76.130.14:6005/)、知识库(TODO)、[模型微调(基于InternLM2)](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Wishes)的初版体验地址，将仓库转为开放。

### 路线图

- [x] 释放最简初版(涉及prompt、aigame、agent、知识库、模型微调)
- [x] 完成[人情世故大模型-送祝福](https://openxlab.org.cn/apps/detail/jujimeizuo/tianji-wish)的模型微调数据收集到微调过程的可复现文档
- [x] 开源人情世故语料-送祝福至huggingface
- [x] 迭代更好的数据制造工具与清洗方案，开源数据清洗脚本
- [ ] 完成知识库部分迭代
- [ ] 完成 Agent 部分文档
- [ ] 开放知识库语料获取细节至huggingface
- [ ] 补充文档（如何参考本项目构建自己的应用prompt、agent、知识库、微调应用）
- [ ] 整理多维度数据，开源较完整人情世故语料
- [ ] 收集 & 开源人情世故语料-2w并训练给出结果和全过程

## 运行环境

### 环境安装

在本项目中，执行下列指令即可安装项目的完成

```
pip install -r requirements.txt
pip install . 
```

### key配置

为确保项目正常运行，**请在项目内新建`.env`文件，并在其中设置你的API密钥**，你可以根据下列例子写入对应的 key，即可成功运行调用,目前默认使用 zhipuai，你可以仅写入`ZHIPUAI_API_KEY`即可使用。

如果在从Hugging Face下载模型时遇到速度极慢或无法下载的问题，请在.env文件中设置`HF_ENDPOINT`的值为`https://hf-mirror.com`。请注意，某些Hugging Face仓库可能需要访问权限（例如Jina Ai）。为此，请注册一个Hugging Face账号，并在.env文件中添加`HF_TOKEN`。你可以在[这里](https://huggingface.co/settings/tokens)找到并获取你的token。

```
OPENAI_API_KEY=
OPENAI_API_BASE=
ZHIPUAI_API_KEY=
BAIDU_API_KEY=
OPENAI_API_MODEL=
HF_HOME='./cache/'
HF_ENDPOINT = 'https://hf-mirror.com'
HF_TOKEN=
```

## 文件目录说明

```
assets/：静态图片文件 
run/： 包括了各类演示用前端
test/：这里存放了各类功能的测试文件，包括核心模块以及llm运行的单元测试
tianji/：源代码目录，包含主要逻辑与算法实现
tools/：帮助收集数据、整理数据清洗语料的工具
```

### 文档说明

TODO,待覆盖全文档

## 🍺运行方式

以下给出 prompt 以及 agent 的相关应用方式，在运行前请确保你已经新建`.env`文件：

```bash
# 运行prompt webui前端
python3 run/tianji_prompt_webui.py

# 运行agent前端
streamlit run run/metagpt_webui.py
```

## 示例

### 微调 - 祝福模块
当前祝福模块支持三种模式触发： 

1. 普通风格，直接写祝福对象，符合常见对话规律。
2. 小红书风格，在祝福对象指定后加上 小红书风格，可触发；自带emoji以及可爱对话风格。 
3. 严肃风格，在祝福对象指定后加上 严肃风格，可触发；文书风格。

![](./assets/demo_wishes.png)

### prompt - 如何敬酒

以下给出 特斯拉创始人 Elon Musk  向 OpenAI 创始人 Sam Altman 敬酒的对话示例（基于内置提示词生成）：

```
elon musk：sam，你的Openai不如叫做CloseAI
sam altman：你先管好你的grok，罚你三杯!
elon musk： 瞧你说的，是要我喝完这瓶白酒？
sam altman：哈哈，埃隆，你可是以星辰大海为目标的男人，一瓶白酒算什么？我可是听说你在SpaceX的派对上连火箭燃料都敢喝呢！来，这杯我干了，你随意，但别失了世界首富的风度啊！
elon musk：你这是在激我啊，Sam老兄！那我就不客气了，我喝掉，你半杯。不过说回来，OpenAI的成果可不只是靠吹牛，你可得好好看着，别让它真的变成了“CloseAI”。
sam altman：嘿，我这CEO的帽子可是随时准备摘下来给你戴戴的，马斯克老兄。不过今晚，让我们先忘了这些，来，为我们的友谊干杯！我喝掉，你随意，但记得，明天还得继续改变世界呢！
elon musk：行，就为你这句“改变世界”，我干了这杯！不过别以为我会轻易放过你，等我下次带上我的特斯拉充电桩，看你怎么应对！
sam altman：哈哈，我等着那一天！不过现在，让我们先享受今晚。来，最后一杯，我干了，你随意，喝得开心，别忘了，OpenAI的AI们可还在等着我们回去继续训练呢！
```

### 知识库 - xxx
TODO

## 如何参与本项目

### 问题看板

  [这里](https://github.com/SocialAI-tianji/Tianji/issues/31)记录了该项目存在的一些问题（欢迎领取解决），以及未来的一些路线图需要完成，当前还没时间写，如果您有时间想一起来玩儿，请issue或者直接邮箱联系我: physicoada@gmail.com

### 提交第一个PR 
  
  得益于良好的ci设施，你只需要参考[示例PR](https://github.com/SocialAI-tianji/Tianji/pull/27)，就可以很快提出自己的第一个prompt PR！
  提交PR后，新的prompt将自动合并于 `tianji/prompt` 下的json文件中，方便一键调用。如果你不知道写什么，可以参考 [场景分类](test/场景分类) 中的各类场景细化细节，写出不同人情世故领域的prompt。

## 如何复刻本项目

  该项目的初衷，第一是为了让`AI学会核心技术`，第二是让更多人（领域/行业）可以构建属于自己的AI系统，加速AI对每一个领域的渗透。你可以通过以下方式来学习该项目：

  你可以参考本项目创造出新的垂直领域应用:
  - 租房助手（agent）
  - 带娃助手（数据收集与知识库）
  - 生活指南（数据收集与知识库）
  ......

## 贡献者

<a href="https://github.com/eryajf/learn-github/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SocialAI-tianji/Tianji" />
</a>

[有些贡献者没有github，我们感谢其中的每一位贡献者！](docs/contributor.md)，也欢迎你一起加入！

## 鸣谢

感谢下列所有人对本项目的帮助：

- 所有贡献者
- 强大的[智谱AI](https://open.bigmodel.cn/)的token支持！（除微调外，目前基座皆基于智谱AI）
- 上海人工智能实验室 [InternLM(书生·浦语) 模型](https://github.com/InternLM/InternLM)，以及提供的A100显卡资源！
- [InternLM(书生·浦语) 系列开源教程（目前最好的LLM实战全栈教程之一）](https://github.com/InternLM/tutorial)
- [Datawhale 开源学习社区](https://github.com/datawhalechina)
- [奇想星球](https://1aigc.cn/)

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=SocialAI-tianji/Tianji&type=Date)](https://star-history.com/#SocialAI-tianji/Tianji&Date)
