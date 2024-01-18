import os
# os.environ["OPENAI_API_KEY"] = "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"  # 填入你自己的OpenAI API key
# os.environ["OPENAI_API_MODEL"] = "gpt-3.5-turbo" # 选择你要使用的模型，例如：gpt-4, gpt-3.5-turbo
# os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"
os.environ["BAIDU_API_KEY"] = "2d6865cfdda39adae11465125df14705060899e6"

# 项目名称：人情世故大模型
# 项目描述：

import re
import asyncio
import json
from common_llm_api import BaiduApi
import sys
sys.path.append("MetaGPT")
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from json_from import SharedDataSingleton
from knowledge_tool import getDocumentsListByQuery
# 给出针对回答的知识 并用md展示
class writeMD(Action):
    
    # 这是对json中每个key的解释：
    # 语言场景（scene），目前的聊天场合，比如工作聚会。
    # 节日（festival），对话目前背景所在的节日，比如生日。
    # 聊天对象角色（role），目前谈话的对象，主要是第三人称。例如和爸爸聊天对象就是爸爸。
    # 聊天对象年龄段（age），和role相关，就是聊天对象的年龄段，例如中老年。
    # 聊天对象职业（career）， 和role相关，就是聊天对象的职业，例如教师。
    # 聊天对象状态（state），和role相关，就是聊天对象的健康状态，例如身体健康。
    # 聊天对象性格（character），和role相关，就是聊天对象的性格特点，例如开朗健谈。
    # 时间（time），和role相关，就是聊天对话时间段，如傍晚。
    # 聊天对象爱好（hobby），和role相关，就是聊天对象的兴趣爱好，例如下象棋。
    # 聊天对象愿望（wish），和role相关，就是聊天对象目前的愿望是什么，例如果希望家庭成员平安。

    knowledge = ""
    json_from_data = SharedDataSingleton.get_instance().json_from_data
    
    
    def __init__(self, name="writeMD", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        # knowledge = ""
        json_from_data = SharedDataSingleton.get_instance().json_from_data
        knowledge_key= json_from_data["festival"] + json_from_data["requirement"]
        knowledge = getDocumentsListByQuery(query_str=knowledge_key)
        PROMPT_TEMPLATE = f"""
            你是一个{json_from_data["festival"]}的祝福大师。
            你需要写一段关于如何写{json_from_data["festival"]}{json_from_data["requirement"]}的思路总结。目前了解到这段{json_from_data["festival"]}{json_from_data["requirement"]}是在{json_from_data["scene"]}送给{json_from_data["role"]}的。
            你写的总结需要考虑如何认同{json_from_data["role"]}的愿望：{json_from_data["wish"]}。
            你需要考虑如何对{json_from_data["role"]}写符合{json_from_data["scene"]}的语言场景的祝福。
            你需要考虑如何对{json_from_data["role"]}写符合{json_from_data["festival"]}的节日氛围的祝福。
            你还可以根据{json_from_data["role"]}的年龄段：{json_from_data["age"]}，职业：{json_from_data["career"]}，状态：{json_from_data["state"]}，性格：{json_from_data["character"]}，当前的时间段：{json_from_data["time"]}，爱好：{json_from_data["hobby"]}作为素材，告诉我怎么用到祝福里。

            你还可以以{knowledge}为参考。

            经过思考后，告诉我怎么完成{json_from_data["festival"]}{json_from_data["requirement"]}，并整理成md结构的文档。

            """
        prompt = PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await BaiduApi()._aask(prompt=prompt,top_p=0.1)
        print("回复生成：",rsp)
        return rsp


# 如何写 如意如意如我心意
class ruyi(Role):
    def __init__(
        self,
        name: str = "ruyi",
        profile: str = "stylize",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([writeMD])
        self._set_react_mode(react_mode="by_order")

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

# async def main():
#     # 对话导入 
#     msg = "test"
#     role = ruyi()
#     logger.info(msg)
#     result = await role.run(msg)
#     logger.info(result)

# asyncio.run(main())
