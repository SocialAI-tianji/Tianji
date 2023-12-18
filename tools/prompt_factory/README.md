# 文件说明

 - prompt_maker.json  负责 prompt 生成和基础信息语料抽取的 json 配置
 - web_demo.py  供通用型的 prompt 产出调试，可以不断修改 `src/prompt` 中的 `prompt.json`来调试通用型的 prompt。目前只支持 gpt 。


# demo 运行

首先安装依赖

```shell
pip install streamlit
pip install openai==0.28.0
pip install python-dotenv
```

在项目根目录下的`.env`文件中可以修改你使用的openai_key，形式为OPENAI_API_KEY="sk-..."

使用以下命令运行web_demo

```shell
streamlit run tools/prompt_factory/web_demo.py
```

prompt 需要在 `src\prompt\gpt_prompt\prompt.json` 文件中修改。
现在只是在 `prompt.json` 中添加了一个全局指令和一个根据用户描述的场景得到的user_prompt，可以在 `web_demo` 中看到效果。大家可以在 `prompt.json` 中添加自己任务的prompt，然后在 `web_demo` 中修改加载项。 

**当前效果**
本demo能够根据用户输入（描述需要使用social-ai的敬酒场景）返回对话语言