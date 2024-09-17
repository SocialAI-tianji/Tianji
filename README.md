# 天机 Tianji

[English](./README_en.md)

[日本語](./README_jp.md)

<div align="center">
<img src=assets\tianjilogo.jpg width="30%"/>
</div>
<p align="center">

🍵 在线体验懂人情世故的天机[prompt应用](http://120.76.130.14:6006/prompt/)、[知识库应用](http://120.76.130.14:6006/knowledges/)、[Agent应用](http://120.76.130.14:6005/)

在上海人工智能实验室 OpenXLab 在线体验天机人情世故微调模型：[送祝福模块](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Wishes)、[敬酒礼仪文化](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Etiquette)
</p>

<p align="center">
📚 查看  <a href="docs" target="_blank">使用文档</a>
</p>

<p align="center">
🍓 在 🤗 huggingface 获取天机的 <a href="https://huggingface.co/datasets/sanbu/tianji-chinese/tree/main" target="_blank"> 所有数据</a>
</p>

<p align="center">
    💡  有疑问或功能请求，欢迎 <a href="https://github.com/SocialAI-tianji/Tianji/issues" target="_blank">创建一个 issue</a> ，或者加入我们的 <a href="assets\tianji-wechat.jpg" target="_blank">微信社区群</a>
</p>


## 📰News


🔥🔥**News**: ```2024.09.02```: 我们更新了第一款专注[敬酒场景的知识库](http://120.76.130.14:6006/knowledges/)对话模型

 🔥 **News**: ```2024.08.31```: -我们重构了仓库组织结构，更新了相关工具代码以及README。彻底更新了 langchain [知识库问答](./tianji/knowledges/) 相关内容以及对应 [demo](run/demo_rag_langchain_onlinellm.py)，让项目更适合一键学习使用。
 🔥**News**: ```2024.07.16```: 我们发布了第一款们发布了第一款专注[敬酒场景的天机模型](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Etiquette), 对应[敬酒语料](https://huggingface.co/datasets/sanbu/tianji-chinese/blob/main/tianji-etiquette-chinese-v0.1.json)专注[敬酒场景的天机模型](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Etiquette), 对应[敬酒语料](https://huggingface.co/datasets/sanbu/tianji-chinese/blob/main/tianji-etiquette-chinese-v0.1.json)

 🔥**News**: ```2024.07.14```: 更新了新版的[送祝福模块](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Wishes) 支持更多风格切换，数据已开源至 [huggingface](https://huggingface.co/datasets/sanbu/tianji-chinese/blob/main/tianji-wishes-chinese-v0.1.json)

 🔥**News**: ```2024.05.04```: 我们发布了以《化解"尴尬"场合》为例的[微调数据获取、制造教程](https://github.com/SocialAI-tianji/Tianji/blob/main/docs/finetune/how-to-get-finetune-data.md)，对应数据开源至 [huggingface](https://huggingface.co/datasets/sanbu/tianji-chinese/tree/main)

 🔥**News**: ```2024.05.02```: 我们发布了有关人情世故大模型-送祝福的数据收集到微调过程的[全流程可复现文档](./docs/finetune/tianji-wishes-chinese.md)及其对应[数据](https://huggingface.co/datasets/sanbu/tianji-chinese/tree/main)、[配置](./tianji/finetune/xtuner/internlm2_chat_7b_qlora_oasst1_e3_copy.py)、[辅助脚本](./tools/finetune/README.md)，（鸽了一段时间但又回来了，主要维护者持续加班忙了，放假才能快乐开源）

 🍵 **News**: ```2024.02.01```: 🧑‍🚀 我们发布了有关 [prompt](http://120.76.130.14:6006/prompt/)、[Agent应用](http://120.76.130.14:6005/)、知识库(TODO)、[模型微调(基于InternLM2)](https://openxlab.org.cn/apps/detail/tackhwa00/Tianji-Wishes)的初版体验地址，将仓库转为开放。

## 你将在该项目中学会 🍉

**学完全部内容，你将获得大语言模型入门级全栈应用开发能力。**

- 构建 [prompt](./tianji/prompt/gpt_prompt/) 对话[大模型应用](./run/tianji_prompt_webui.py)

- 制作 [AI 游戏](./tianji/prompt/aigame/zhipu/)（类似哄哄模拟器）应用

- 基于 [metagpt](./tianji/agents/metagpt_agents/) 构建[智能体应用](./run/metagpt_webui.py)  （即将重构）

- 从零构建一个[知识库对话应用](./tianji/knowledges/)

- [从零制作语言模型微调数据](./docs/finetune/how-to-get-finetune-data.md)、[微调](./docs/finetune/how-to-get-finetune-data.md)属于自己的大语言模型


## 目录


- [快速开始](#%E8%BF%90%E8%A1%8C%E7%8E%AF%E5%A2%83)
  - [环境安装](#%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85)
  - [key配置](#key%E9%85%8D%E7%BD%AE)
- [路线图](#%E8%B7%AF%E7%BA%BF%E5%9B%BE)
- [技术路线](#%E6%8A%80%E6%9C%AF%E8%B7%AF%E7%BA%BF)
- [文件目录说明](#%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E8%AF%B4%E6%98%8E)
  - [文档说明](#%E6%96%87%E6%A1%A3%E8%AF%B4%E6%98%8E)
- [运行方式](#%F0%9F%8D%BA%E8%BF%90%E8%A1%8C%E6%96%B9%E5%BC%8F)
  - [示例](#%E7%A4%BA%E4%BE%8B)
- [如何参与本项目](#%E5%A6%82%E4%BD%95%E5%8F%82%E4%B8%8E%E6%9C%AC%E9%A1%B9%E7%9B%AE)
  - [问题看板](#%E9%97%AE%E9%A2%98%E7%9C%8B%E6%9D%BF)
  - [提交第一个PR](#%E6%8F%90%E4%BA%A4%E7%AC%AC%E4%B8%80%E4%B8%AAPR)
- [如何复刻本项目](#%E5%A6%82%E4%BD%95%E5%A4%8D%E5%88%BB%E6%9C%AC%E9%A1%B9%E7%9B%AE)
- [贡献者](#%E8%B4%A1%E7%8C%AE%E8%80%85)
- [鸣谢](#%E9%B8%A3%E8%B0%A2)


## 快速开始 💫

### 环境安装

在本项目中，执行下列指令即可完成项目的安装

```
pip install -e .
```

### key配置

为确保项目正常运行，**请在项目内新建`.env`文件，并在其中设置你的API密钥**，你可以根据下列例子写入对应的 key，即可成功运行调用,目前默认使用 zhipuai，你可以仅写入`ZHIPUAI_API_KEY`即可使用。

```
ZHIPUAI_API_KEY=
```

如果在从Hugging Face下载模型时遇到速度极慢或无法下载的问题，请在.env文件中设置`HF_ENDPOINT`的值为`https://hf-mirror.com`。请注意，某些Hugging Face仓库可能需要访问权限（例如Jina Ai）。为此，请注册一个Hugging Face账号，并在.env文件中添加`HF_TOKEN`。你可以在[这里](https://huggingface.co/settings/tokens)找到并获取你的token。

```
HF_HOME='./cache/'
HF_ENDPOINT = 'https://hf-mirror.com'
OPENAI_API_KEY=
OPENAI_API_BASE=
ZHIPUAI_API_KEY=
BAIDU_API_KEY=
OPENAI_API_MODEL=
HF_TOKEN=
```

### 运行

以下给出 prompt 以及 agent 的相关应用方式，在运行前请确保你已经新建`.env`文件：

```bash
# 运行prompt webui前端
python3 run/tianji_prompt_webui.py

# 运行agent前端
streamlit run run/metagpt_webui.py

# 运行langchain前端
python run/demo_rag_langchain_onlinellm.py
```

### 开发环境配置

在进行项目开发与贡献之前，在保证key的正确设定后，你还需要在提交 pull request 前进行格式检查。你可以参考下列方式进行 pre-commit 的安装，在 commit 环节将会看到变更文件格式会被自动修改。

```
pip install pre-commit
pre-commit install
git add .
git commit -m "提交信息"
git push
```

这一步，你需要反复执行下列两步,直到 commit 成功 （该过程会帮助你自动修复绝大部分格式错误，但对于某些复杂格式需要自己手动根据提示修改。）

```
git add .
git commit -m "提交信息"
```

若全部成功，你将会看到类似如下信息显示：

```
[main 2333] rebuild code standard
 5 files changed, 4 insertions(+), 3 deletions(-)
```

## 路线图

- [x] 释放最简初版(涉及prompt、aigame、agent、知识库、模型微调)
- [x] 完成[人情世故大模型-送祝福](https://openxlab.org.cn/apps/detail/jujimeizuo/tianji-wish)的模型微调数据收集到微调过程的可复现文档
- [x] 开源人情世故语料-送祝福至huggingface
- [x] 迭代更好的数据制造工具与清洗方案，开源数据清洗脚本
- [ ] 完成知识库部分迭代
- [ ] 开放知识库语料获取细节至huggingface
- [ ] 完成 Agent 部分文档
- [ ] 补充文档（如何参考本项目构建自己的应用prompt、agent、知识库、微调应用）
- [ ] 整理多维度数据，开源较完整人情世故语料
- [ ] 收集 & 开源人情世故语料-2w并训练给出结果和全过程

## 技术路线

基于整理后的人情世故数据，人情世故大模型系统-天机包括了常见人际交往中的七大领域（具体可以参考 [场景分类](test/%E5%9C%BA%E6%99%AF%E5%88%86%E7%B1%BB) 中的场景细化细节），其中大体可分为：

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

## 示例

### 微调 - 祝福模块

当前祝福模块支持三种模式触发：

1. 普通风格，直接写祝福对象，符合常见对话规律。
1. 小红书风格，在祝福对象指定后加上 小红书风格，可触发；自带emoji以及可爱对话风格。
1. 严肃风格，在祝福对象指定后加上 严肃风格，可触发；文书风格。

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
提交PR后，新的prompt将自动合并于 `tianji/prompt` 下的json文件中，方便一键调用。如果你不知道写什么，可以参考 [场景分类](test/%E5%9C%BA%E6%99%AF%E5%88%86%E7%B1%BB) 中的各类场景细化细节，写出不同人情世故领域的prompt。

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
- 项目最开始时刻 [智谱AI](https://open.bigmodel.cn/) 的token支持！
- 上海人工智能实验室 [InternLM(书生·浦语) 模型](https://github.com/InternLM/InternLM)，以及提供的A100显卡资源！
- [InternLM(书生·浦语) 系列开源教程（目前最好的LLM实战全栈教程之一）](https://github.com/InternLM/tutorial)
- [Datawhale 开源学习社区](https://github.com/datawhalechina)
- [奇想星球](https://1aigc.cn/)

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=SocialAI-tianji/Tianji&type=Date)
