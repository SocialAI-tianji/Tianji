# 天机 Tianji

天机是 SocialAI（来事儿AI）制作的一款免费使用、非商业用途的人工智能系统。您可以利用它进行涉及传统人情世故的任务，如`如何敬酒、如何说好话、如何会来事儿`等，以提升您的情商和核心竞争能力。我们坚信，只有人情世故才是未来AI的核心技术，只有会来事儿的AI才有机会走向AGI，让我们携手见证通用人工智能的来临。 —— "天机不可泄漏。"

Tianji is a free, non-commercial artificial intelligence system. You can utilize it for tasks involving worldly wisdom, such as "art of conversation," to enhance your emotional intelligence and core competitiveness. We firmly believe that worldly wisdom are the future core competency of AI, and let us join hands to witness the advent of general artificial intelligence.

<p align="left">
    中文</a>&nbsp ｜ &nbsp<a href="README.md">English(还没空写)</a>&nbsp ｜ &nbsp<a href="README.md">日本語(还没空写)</a> 
</p>
<br><br>

<p align="center">
    <img src="./assets/tianjilogo.jpg" width="400"/>
<p>
<br>


<p align="center">
   <a href="https://python.org/" target="_blank"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/moelib?logo=python&style=flat-square"></a>
   <a href="https://github.com/tatsu-lab/stanford_alpaca/blob/main/LICENSE"><img alt="LICENSE" src="https://camo.githubusercontent.com/ff42248868bc1387751598955e573b397851d947f13ddd7618c0ba9e66aacdf6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f436f64652532304c6963656e73652d4170616368655f322e302d677265656e2e737667"></a>
   <br/>

</p>

SocialAI（来事儿AI） 是设立于中国的非营利组织，我们完全开源了**Tianji**（天机）系列工作，当前开源系统技术路线涉及为`Prompt、AI游戏、Agent、知识库、模型训练`。具体内容，请查看文档与对应仓库。

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

## 目录
- [News](#News)
  - [路线图](#路线图)
- [运行环境](#运行环境)
  - [环境安装](#环境安装)
  - [key配置](#key配置)
- [文件目录说明](#文件目录说明)
  - [文档说明](#文档说明)
- [运行方式](#运行方式)
  - [示例](#示例)
- [使用到的框架](#使用到的框架)
- [如何参与本项目](#如何参与本项目)
  - [提交第一个PR](#提交第一个PR)
- [如何复刻超越本项目](#如何复刻超越本项目)
- [鸣谢](#鸣谢)

## 📰 News

- **[2024.02.01]** 🧑‍🚀 我们发布了有关 [prompt](http://120.76.130.14:6006/prompt/)、[Agent应用](http://120.76.130.14:6005/)、知识库(TODO)、[模型微调(基于InternLM2)](https://openxlab.org.cn/apps/detail/jujimeizuo/tianji-wish)的初版体验地址，将仓库转为开放。

### 🛣 路线图

- [x] 释放初版资源
- [ ] 公开所有服务器体验地址
- [ ] 将项目挂载 huggingface
- [ ] 将项目挂载 openxlab
- [ ] 将项目挂载 modelscope
- [ ] 完成 Agent 贡献指南
- [ ] 完成模型微调数据收集到微调过程的可复现文档
- [ ] 开源人情世故语料-送祝福
- [ ] 开放知识库语料获取细节
- [ ] 开源人情世故语料-6k
- [ ] 收集 & 开源人情世故语料-2w

## 运行环境

### 环境安装

在本项目中，执行下列指令即可安装完成

```
pip install -r requirements.txt
pip install . 
```

### key 配置

为确保项目正常运行，请在`.env` 中设置API密钥，你可以根据下列例子写入对应的 key，即可成功运行调用,目前默认使用 zhipuai，你可以仅写入`ZHIPUAI_API_KEY`即可使用。

```
OPENAI_API_KEY=
OPENAI_API_BASE=
BAIDU_API_KEY=
OPENAI_API_MODEL=
ZHIPUAI_API_KEY=
```

## 文件目录说明

```
assets/：静态图片文件 
run/： 运行用文件 
test/：测试文件 
tianji/：源代码目录，包含主要逻辑与算法实现 
tools/：帮助收集数据的工具  
```


## 🍺运行方式

## 示例

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


## 有效prompt统计
记录目前仓库内有多少有效的prompt

<div style="display: flex; justify-content: space-between;">
  <img src=".ci/gpt_prompt_statistics.png" alt="Image 1" width="45%">
  <img src=".ci/yiyan_prompt_statistics.png" alt="Image 2" width="45%">
</div>


## 鸣谢

感谢下列所有人对本项目的帮助：

- 所有贡献者
- 强大的[智谱AI](https://open.bigmodel.cn/)的token支持！（除微调外，目前基座皆基于智谱AI）
- 上海人工智能实验室 [InternLM(书生·浦语) 模型](https://github.com/InternLM/InternLM)，以及提供的A100显卡资源！
- [InternLM(书生·浦语) 系列开源教程（目前最好的LLM实战全栈教程之一）](https://github.com/InternLM/tutorial)
- Datawhale 开源学习社区
- 奇想星球

TODO......（还没写完


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SocialAI-tianji/Tianji&type=Date)](https://star-history.com/#SocialAI-tianji/Tianji&Date)
