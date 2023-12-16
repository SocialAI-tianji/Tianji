# 文件说明

 - prompt_maker.json  负责 prompt 生成和基础信息语料抽取的 json 配置
 - web_demo.py  供通用型的 prompt 产出调试，可以不断修改 `src/prompt` 中的 `prompt.json`来调试通用型的 prompt。目前只支持 gpt 。


# demo 运行

首先安装依赖

```shell
pip install streamlit
pip install openai
pip install dotenv
```

在`openai.api_key`处填入你的`api_key`，如下所示：

> 注意一定不要将 `api_key` 上传至github仓库，这样会导致 `api_key` 被销毁。

```python
openai.api_key = 'your_api_key'
```

使用以下命令运行web_demo

```shell
streamlit run tools/prompt_factory/web_demo.py
```

prompt 需要在 `src\prompt\gpt_prompt\prompt.json` 文件中修改。现在只是在 `prompt.json` 中添加了一个简单的例子，可以在 `web_demo` 中看到效果。大家可以在 `prompt.json` 中添加自己任务的prompt，然后在 `web_demo` 中修改加载项。 