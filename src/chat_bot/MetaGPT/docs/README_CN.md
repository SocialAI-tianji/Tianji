# MetaGPT: 多智能体框架

<p align="center">
<a href=""><img src="resources/MetaGPT-new-log.png" alt="MetaGPT logo: 使 GPT 以软件公司的形式工作，协作处理更复杂的任务" width="150px"></a>
</p>

<p align="center">
<b>使 GPTs 组成软件公司，协作处理更复杂的任务</b>
</p>

<p align="center">
<a href="docs/README_CN.md"><img src="https://img.shields.io/badge/文档-中文版-blue.svg" alt="CN doc"></a>
<a href="README.md"><img src="https://img.shields.io/badge/document-English-blue.svg" alt="EN doc"></a>
<a href="docs/README_JA.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-blue.svg" alt="JA doc"></a>
<a href="https://discord.gg/DYn29wFk9z"><img src="https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat" alt="Discord Follow"></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
<a href="docs/ROADMAP.md"><img src="https://img.shields.io/badge/ROADMAP-路线图-blue" alt="roadmap"></a>
<a href="https://twitter.com/MetaGPT_"><img src="https://img.shields.io/twitter/follow/MetaGPT?style=social" alt="Twitter Follow"></a>
</p>

<p align="center">
   <a href="https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/geekan/MetaGPT"><img src="https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode" alt="Open in Dev Containers"></a>
   <a href="https://codespaces.new/geekan/MetaGPT"><img src="https://img.shields.io/badge/Github_Codespace-Open-blue?logo=github" alt="Open in GitHub Codespaces"></a>
   <a href="https://huggingface.co/spaces/deepwisdom/MetaGPT" target="_blank"><img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20-Hugging%20Face-blue?color=blue&logoColor=white" /></a>
</p>

1. MetaGPT输入**一句话的老板需求**，输出**用户故事 / 竞品分析 / 需求 / 数据结构 / APIs / 文件等**
2. MetaGPT内部包括**产品经理 / 架构师 / 项目经理 / 工程师**，它提供了一个**软件公司**的全过程与精心调配的SOP
   1. `Code = SOP(Team)` 是核心哲学。我们将SOP具象化，并且用于LLM构成的团队

![一个完全由大语言模型角色构成的软件公司](resources/software_company_cd.jpeg)

<p align="center">软件公司多角色示意图（正在逐步实现）</p>

## 安装
### Pip安装

```bash
# 第 1 步：确保您的系统上安装了 Python 3.9+。您可以使用以下命令进行检查：
# 可以使用conda来初始化新的python环境
#     conda create -n metagpt python=3.9
#     conda activate metagpt
python3 --version

# 第 2 步：克隆最新仓库到您的本地机器，并进行安装。
git clone https://github.com/geekan/MetaGPT.git
cd MetaGPT
pip3 install -e.  # 或者 pip3 install metagpt  # 安装稳定版本

# 第 3 步：执行startup.py
# 拷贝config.yaml为key.yaml，并设置你自己的OPENAI_API_KEY
python3 startup.py "Write a cli snake game"

# 第 4 步【可选的】：如果你想在执行过程中保存像象限图、系统设计、序列流程等图表这些产物，可以在第3步前执行该步骤。默认的，框架做了兼容，在不执行该步的情况下，也可以完整跑完整个流程。
# 如果执行，确保您的系统上安装了 NPM。并使用npm安装mermaid-js
npm --version
sudo npm install -g @mermaid-js/mermaid-cli
```

详细的安装请安装 [cli_install](https://docs.deepwisdom.ai/guide/get_started/installation.html#install-stable-version)

### Docker安装
> 注意：在Windows中，你需要将 "/opt/metagpt" 替换为Docker具有创建权限的目录，比如"D:\Users\x\metagpt"

```bash
# 步骤1: 下载metagpt官方镜像并准备好config.yaml
docker pull metagpt/metagpt:latest
mkdir -p /opt/metagpt/{config,workspace}
docker run --rm metagpt/metagpt:latest cat /app/metagpt/config/config.yaml > /opt/metagpt/config/key.yaml
vim /opt/metagpt/config/key.yaml # 修改配置文件

# 步骤2: 使用容器运行metagpt演示
docker run --rm \
    --privileged \
    -v /opt/metagpt/config/key.yaml:/app/metagpt/config/key.yaml \
    -v /opt/metagpt/workspace:/app/metagpt/workspace \
    metagpt/metagpt:latest \
    python startup.py "Write a cli snake game"
```

详细的安装请安装 [docker_install](https://docs.deepwisdom.ai/zhcn/guide/get_started/installation.html#%E4%BD%BF%E7%94%A8docker%E5%AE%89%E8%A3%85)

### 快速开始的演示视频
- 在 [MetaGPT Huggingface Space](https://huggingface.co/spaces/deepwisdom/MetaGPT) 上进行体验
- [Matthew Berman: How To Install MetaGPT - Build A Startup With One Prompt!!](https://youtu.be/uT75J_KG_aY)
- [官方演示视频](https://github.com/geekan/MetaGPT/assets/2707039/5e8c1062-8c35-440f-bb20-2b0320f8d27d)

https://github.com/geekan/MetaGPT/assets/34952977/34345016-5d13-489d-b9f9-b82ace413419

## 教程
- 🗒 [在线文档](https://docs.deepwisdom.ai/zhcn/)
- 💻 [如何使用](https://docs.deepwisdom.ai/zhcn/guide/get_started/quickstart.html)  
- 🔎 [MetaGPT的能力及应用场景](https://docs.deepwisdom.ai/zhcn/guide/get_started/introduction.html)
- 🛠 如何构建你自己的智能体？
  - [MetaGPT的使用和开发教程 | 智能体入门](https://docs.deepwisdom.ai/zhcn/guide/tutorials/agent_101.html)
  - [MetaGPT的使用和开发教程 | 多智能体入门](https://docs.deepwisdom.ai/zhcn/guide/tutorials/multi_agent_101.html)
- 🧑‍💻 贡献
  - [开发路线图](ROADMAP.md)
- 🔖 示例
  - [辩论](https://docs.deepwisdom.ai/zhcn/guide/use_cases/multi_agent/debate.html)
  - [调研员](https://docs.deepwisdom.ai/zhcn/guide/use_cases/agent/researcher.html)
  - [票据助手](https://docs.deepwisdom.ai/zhcn/guide/use_cases/agent/receipt_assistant.html)
- ❓ [常见问题解答](https://docs.deepwisdom.ai/zhcn/guide/faq.html)

## 支持

### 加入我们

📢 加入我们的[Discord频道](https://discord.gg/ZRHeExS6xv)！

期待在那里与您相见！🎉

### 联系信息

如果您对这个项目有任何问题或反馈，欢迎联系我们。我们非常欢迎您的建议！

- **邮箱：** alexanderwu@fuzhi.ai
- **GitHub 问题：** 对于更技术性的问题，您也可以在我们的 [GitHub 仓库](https://github.com/geekan/metagpt/issues) 中创建一个新的问题。

我们会在2-3个工作日内回复所有问题。

## 引用

引用 [arXiv paper](https://arxiv.org/abs/2308.00352):

```bibtex
@misc{hong2023metagpt,
      title={MetaGPT: Meta Programming for Multi-Agent Collaborative Framework},
      author={Sirui Hong and Xiawu Zheng and Jonathan Chen and Yuheng Cheng and Jinlin Wang and Ceyao Zhang and Zili Wang and Steven Ka Shing Yau and Zijuan Lin and Liyang Zhou and Chenyu Ran and Lingfeng Xiao and Chenglin Wu},
      year={2023},
      eprint={2308.00352},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
