from dotenv import load_dotenv

load_dotenv()
# 项目名称：人情世故大模型
# 项目描述：

import sys

sys.path.append("MetaGPT")

from typing import Optional
from metagpt.actions import Action
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.common_llm_api import LLMApi


# json_from_data = {
#             "requirement": "祝福",
#             "scene": "家庭聚会",
#             "festival": "元旦",
#             "role": "妈妈",
#             "age": "中老年人",
#             "career": "小学教师",
#             "state": "身体欠佳",
#             "character": "开朗",
#             "time": "傍晚",
#             "hobby": "广场舞",
#             "wish": "家庭成员平安"
#         }w

# 设计思路 给定人设并导入参考聊天话术、历史聊天语料进行聊天。
class ansWrite(Action):

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

    def __init__(self, name="read_and_ana", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        sharedData: Optional[SharedDataSingleton] = SharedDataSingleton.get_instance()
        json_from_data: Optional[dict] = sharedData.json_from_data
        knowledge: str = ""
        PROMPT_TEMPLATE: str = f"""
        你是一个{json_from_data["festival"]}的祝福大师。
        你需要写一段：{json_from_data["requirement"]}。这段{json_from_data["festival"]}{json_from_data["requirement"]}是在{json_from_data["scene"]}送给{json_from_data["role"]}的。
        你写的祝福需要认同{json_from_data["role"]}的愿望：{json_from_data["wish"]}。
        你写的祝福需要符合{json_from_data["role"]}的语言场景：{json_from_data["scene"]}。
        你写的祝福需要符合{json_from_data["role"]}的节日氛围：{json_from_data["festival"]}。
        你还可以根据{json_from_data["role"]}的年龄段：{json_from_data["age"]}，职业：{json_from_data["career"]}，状态：{json_from_data["state"]}，性格：{json_from_data["character"]}，当前的时间段：{json_from_data["time"]}，爱好：{json_from_data["hobby"]}作为资料参考。



        你还可以以{knowledge}为参考。

        经过思考后，将这些信息整理成一段完整的{json_from_data["requirement"]}。

        """
        print("json_from_data####################################", json_from_data)

        # knowledges = ""
        prompt = PROMPT_TEMPLATE.format(instruction=instruction)
        print(prompt)
        rsp = await LLMApi()._aask(prompt=prompt, top_p=0.1)
        print("回复生成：", rsp)
        return rsp


# 设计思路 根据当前状态和聊天与恋爱相关性等综合打分。给出当前回合的打分情况
class stylize(Action):
    PROMPT_TEMPLATE: str = """
    你是一个萌妹，对任何人说话都很温柔客气。你很聪明礼貌。你喜欢发一些颜文字表情。大家都很喜欢你。
    请用自己的语气改写{instruction}
    """

    def __init__(self, name="rerask", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await LLMApi()._aask(prompt=prompt, top_p=0.1)
        print("风格化：", rsp)
        return rsp
