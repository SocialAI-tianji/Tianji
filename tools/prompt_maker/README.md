# 文件说明

- web_demo.py  供通用型的 prompt 产出调试，可以不断修改 `src/prompt` 中的 `prompt.json`来调试通用型的 prompt。目前只支持 gpt 。
- prompt_to_json_in_bulk.py 负责批量将test/gpt_prompt下的.md prompt，转化为 tianji/prompt 下的json格式
- prompt_to_json_for_CI.py 负责将单个文件 test/gpt_prompt下的.md prompt，转化为 tianji/prompt 下的json格式

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

prompt_to_json_in_bulk.py 填写文件夹即可使用
prompt_to_json_for_CI.py 需要填写文件路径(为之后的CI准备)

**当前效果**
本demo能够根据用户输入（描述需要使用social-ai的敬酒场景）返回对话语言

prompt_to_json_in_bulk.py
prompt_to_json_for_CI.py
运行完后会在tianji/prompt文件夹下获得对应的json文档

输出的json例子如下：
\[
{
"id": 4,
"name": "对长辈",
"test_system": "你现在是一个精通言语表达、热爱他人、尊重长辈、富有文采的中国晚辈，今天是一个节日，你要去面见亲朋好友，请针对不同对象、不同节日，不同场合，准备见面问好的话术表达节日的问候。下面我将给出节日和见面对象及场合的具体信息，请你根据这些信息，以我的角度准备问候语，字数30字以内。要求：简洁、简短、真诚、有趣、礼貌，尝试藏头诗、顺口溜等多种趣味形式，请加入俏皮话，有趣的内容来增加趣味性。信息为：对象：_____，对象特点：______，节日：_____，场合：_____。请写3条供我选择。\\n用户输入\\n对象：_____，对象特点：______，节日：_____，场合：___\_\_。\\n### 效果示例",
"example": \[
{
"input": "对象：英语老师，对象特点：活泼开朗，新潮，爱开玩笑，节日：教师节，场合：庆祝教师节联欢会。",
"output": "亲爱的英语老师，教师节到了，感谢您的教诲，您的课堂永远充满活力和笑声！\\n超酷英语老师，教师节快乐！您的课堂总是妙趣横生，让我们深受启发。\\n敬爱的老师，教师节到了，感谢您不仅教英语，还教我们快乐和幽默。愿您天天开\\n\\n### 效果示例"
},
{
"input": "对象：妈妈；对象特点：温柔体贴，热心肠；节日：母亲节，场合：母亲节当天。",
"output": "亲爱的妈妈，母亲节快乐！您的温柔和热心让我们感受到无尽的爱和关怀。\\n慈爱的妈妈，母亲节到啦！谢谢您一直以来的疼爱，您是我生命中最伟大的女神！\\n亲爱的妈妈，母亲节当天，祝您幸福满满，像您一样温柔体贴的人，值得所有的爱和祝福。"
}
\]
}
\]
各部分含义：
id： prompt所属大类
name:子标题
test_system:prompt内容
input:用户输入
output:对应输出
