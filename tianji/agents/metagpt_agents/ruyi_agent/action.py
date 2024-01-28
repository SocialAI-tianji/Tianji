from dotenv import load_dotenv

load_dotenv()
# 项目名称：人情世故大模型
# 项目描述：

from tianji.utils.common_llm_api import LLMApi
import sys
from typing import Optional
from metagpt.actions import Action
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.knowledge_tool import get_docs_list_query_openai


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

    name: str = "writeMD"

    knowledge: str = ""
    json_from_data: str = SharedDataSingleton.get_instance().json_from_data

    async def run(self, instruction: str):
        # knowledges = ""
        json_from_data = SharedDataSingleton.get_instance().json_from_data
        knowledge_key = json_from_data["festival"] + json_from_data["requirement"]
        knowledge = get_docs_list_query_openai(query_str=knowledge_key)
        PROMPT_TEMPLATE: str = f"""
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
        rsp = await LLMApi()._aask(prompt=prompt, top_p=0.1)
        print("回复生成：", rsp)
        return rsp

# 如何写 如意如意如我心意