import os
# os.environ["OPENAI_API_KEY"] = "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"  # 填入你自己的OpenAI API key
# os.environ["OPENAI_API_MODEL"] = "gpt-3.5-turbo" # 选择你要使用的模型，例如：gpt-4, gpt-3.5-turbo
# os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"
os.environ["BAIDU_API_KEY"] = "2d6865cfdda39adae11465125df14705060899e6"

# 项目名称：人情世故大模型
# 项目描述：

import re
import asyncio
import sys
sys.path.append("MetaGPT")
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import json
from json_from import SharedDataSingleton
from common_llm_api import BaiduApi




# json_from_data = {
#         "requirement": "",
#         "scene": "",
#         "festival": "",
#         "role": "",
#         "age": "",
#         "career": "",
#         "state": "",
#         "character": "",
#         "time": "",
#         "hobby": "",
#         "wish": ""
#     }

# 设计思路 给定人设并导入参考聊天话术、历史聊天语料进行聊天。
class read_and_ana(Action):
    PROMPT_TEMPLATE = """
    你是一个需求语言分析大师，你需要根据"历史消息记录"中的内容分析出以下要素(注意：没如果没有不要回答)：
    1.分析对话需求(requirement)。用关键词表示。如：请帮我写一段祝福。->写一段祝福
    2.分析得到目前的语言场景(scene)。用关键词表示。如：我们一家人正在吃饭。->家庭聚会
    3.分析目前的节日(festival)。用关键词表示。如：今天是元旦。->元旦
    4.分析目前的聊天对象角色(role)。用关键词表示。如：妈妈和我说今天多吃点。->妈妈
    5.分析目前的聊天对象年龄段(age)。如：妈妈和我说今天多吃点。->中老年人
    6.分析目前的聊天对象职业(career)。如：妈妈给小朋友们刚上完课。->小学教师
    7.分析目前的聊天对象状态(state)。如：妈妈今年刚做完手术。->身体欠佳
    8.分析目前的聊天对象性格(character)。如：妈妈还是那么爽朗，爱笑。->开朗
    9.分析目前的时间(time)。用关键词表示。如：今天的晚饭很好吃。->傍晚
    10.分析目前的爱好(hobby)。用关键词表示。如：妈妈和平常一样，下楼跳了广场舞。->广场舞
    11.分析目前的愿望(wish)。用关键词表示。如：妈妈希望我们一家人平平安安。->家庭成员平安
    12.分析目前的语言风格(style)。用关键词表示。只能从"老年人版","小红书版","带颜文字可爱版"中选择一个,没有就为空，即""。->小红书版
    并将分析的内容组装成json。
    根据上面的例子组装成如下json(如果没有提取到请用空字符串表示，如："time": ""):
    {case}

    这是对json中每个key的解释：
    语言场景（scene），目前的聊天场合，比如工作聚会。
    节日（festival），对话目前背景所在的节日，比如生日。
    聊天对象角色（role），目前谈话的对象，主要是第三人称。例如和爸爸聊天对象就是爸爸。
    聊天对象年龄段（age），和role相关，就是聊天对象的年龄段，例如中老年。
    聊天对象职业（career）， 和role相关，就是聊天对象的职业，例如教师。
    聊天对象状态（state），和role相关，就是聊天对象的健康状态，例如身体健康。
    聊天对象性格（character），和role相关，就是聊天对象的性格特点，例如开朗健谈。
    时间（time），和role相关，就是聊天对话时间段，如傍晚。
    聊天对象爱好（hobby），和role相关，就是聊天对象的兴趣爱好，例如下象棋。
    聊天对象愿望（wish），和role相关，就是聊天对象目前的愿望是什么，例如果希望家庭成员平安。
    语言风格（style），就是期望用什么语气，语言特点来表达，例如"老年版","小红书版"或者"带颜文字可爱版"。

    历史消息记录如下```
    {instruction}
    ```
    请认真结合历史消息记录分析每一个要素的情况。
    只需要回复我JSON内容，不需要markdown格式，不需要回复其他任何内容！
    """
    
    def __init__(self, name="read_and_ana", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        case = {
            "requirement": "祝福",
            "scene": "家庭聚会",
            "festival": "元旦",
            "role": "妈妈",
            "age": "中老年人",
            "career": "小学教师",
            "state": "身体欠佳",
            "character": "开朗",
            "time": "傍晚",
            "hobby": "广场舞",
            "wish": "家庭成员平安",
            "style": "小红书版"
        }
        case1 = {
            "requirement": "给爸爸送祝福",
            "scene": "家庭庆祝生日",
            "festival": "生日",
            "role": "爸爸",
            "age": "中年",
            "career": "软件工程师",
            "state": "对新技术热情高涨",
            "character": "经验丰富",
            "time": "晚上",
            "hobby": "摄影",
            "wish": "希望我能学会欣赏艺术的美",
            "style": "老年人版"
        }
        case = json.dumps(case)
        case1 = json.dumps(case1)
        sharedData  = SharedDataSingleton.get_instance()
        print("instruction",instruction)

        prompt = self.PROMPT_TEMPLATE.format(instruction=sharedData.first_status_user_history,case = case,case1 = case1)
        print("prompt",prompt)
        rsp = await BaiduApi()._aask(prompt=prompt,top_p=0.1)
        rsp = rsp.replace("```json", "").replace("```", "")
        #rsp = rsp.strip('json\n').rstrip('')

        print("机器人分析需求：",rsp)
        sharedData.json_from_data = json.loads(rsp)
        # json_from_data = json.loads(rsp)
        return rsp

# 设计思路 根据当前状态和聊天与恋爱相关性等综合打分。给出当前回合的打分情况
class rerask(Action):
    sharedData  = SharedDataSingleton.get_instance()
    json_from_data = sharedData.json_from_data

    PROMPT_TEMPLATE = """
    限定提问的问题```
    {question_list_str}
    ```
    你是一个提问大师，你只能从"限定提问的问题"中随机选择一个对我进行提问，每次提问只能问一个问题。
    提问问题的时候，你的语言风格满足：
    1.友好，活泼
    你只需要回复我你的提问内容，不需要任何其他内容!
    """
    PROMPT_TEMPLATE = """
    你是一个提问大师，你只能从"限定提问的问题"中随机选择一个对我进行提问，每次提问只能问一个问题。
    限定提问的问题```
    {question_list_str}
    ```
    每次提问只能问一个问题。
    """
    def __init__(self, name="rerask", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        sharedData  = SharedDataSingleton.get_instance()
        json_from_data = sharedData.json_from_data
        #case = {"requirement": "", "scene": "家庭聚会", "festival": "元旦", "role": "妈妈", "age": "中老年人", "career": "退休中学教师", "state": "", "character": "开朗", "time": "傍晚", "hobby": "园艺", "wish": ""}
        #case = json.dumps(json_from_data)
        #print("case",case)
        check_after_question_list = {
            "requirement": "请告诉我你的需求，比如送祝福。",
            #"scene": "你准备在什么场景下进行呢？比如家庭聚会，朋友聚会等等。",
            "festival": "是在哪个特殊的节日(比如中秋节，春节)吗?",
            "role": "你送祝福的对象是谁呢？",
            #"age": "你送祝福的对象年龄多大呢？",
            #"career": "送祝福的对象是做什么职业呢？",
            #"state": "送祝福的对象最近状态如何呢？比如身体状况，精神状况等等。",
            #"character": "送祝福的对象他有什么性格特点吗？",
            "time": "你准备在什么时间送祝福呢？",
            #"hobby": "送祝福的对象有什么习惯吗？",
            #"wish": "送祝福的对象有哪些个人愿望吗？",
            "style": "你期望送祝福的语气是老年风格，小红书风格还是带颜文字可爱风格呢?"
        }
        question_list = []
        for key, value in json_from_data.items():
            if key in check_after_question_list:
                if json_from_data[key] == "":
                    question_list.append(check_after_question_list[key])

        question_list_str = "\n".join(question_list)


        prompt = self.PROMPT_TEMPLATE.format(question_list_str=question_list_str)
        print("rerask prompt",prompt)
        rsp = await BaiduApi()._aask(prompt=prompt,top_p=0.1)
        print("机器人提问：",rsp)

        if question_list == []:
            rsp = "YES|"+str(rsp)
        else:
            rsp = "NO|"+str(rsp)
        print(rsp)
        return rsp


# 问道  问出来信息
class wendao(Role):
    def __init__(
        self,
        name: str = "wendao",
        profile: str = "GetInformation",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([read_and_ana,rerask])
        self._set_react_mode(react_mode="by_order")

    '''
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        # By choosing the Action by order under the hood
        # todo will be first SimpleWriteCode() then SimpleRunCode()
        todo = self._rc.todo

        msg = self.get_memories(k=1)[0] # find the most k recent messagesA
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self._rc.memory.add(msg)
        return msg
    '''
    async def _act_by_order(self) -> Message:
        """switch action each time by order defined in _init_actions, i.e. _act (Action1) -> _act (Action2) -> ..."""
        for i in range(len(self._states)):
            self._set_state(i)
            rsp = await self._act()
        return rsp  # return output from the last action