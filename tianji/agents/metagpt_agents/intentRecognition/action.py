from dotenv import load_dotenv

load_dotenv()

from metagpt.actions import Action
from metagpt.logs import logger
from tianji.agents.metagpt_agents.utils.agent_llm import ZhipuApi as LLMApi
from tianji.agents.metagpt_agents.utils.helper_func import *

"""
意图识别动作模块 (IntentAnalyze)

该模块实现了意图识别智能体的核心分析功能。
负责将用户输入的自然语言文本转换为系统预定义的场景类型。

主要功能：
1. 解析用户输入
2. 使用LLM进行意图分析
3. 匹配预定义场景类型
4. 返回场景标签
"""

class IntentAnalyze(Action):
    """意图分析动作类
    
    使用LLM分析用户输入，识别用户意图并匹配到预定义场景。
    
    属性:
        name (str): 动作名称
        PROMPT_TEMPLATE (str): LLM提示模板
    """
    
    PROMPT_TEMPLATE: str = """
    #Role:
    - 场景分析助手

    ## Background:
    - 作为一个专业的场景分析助手。接下来，我将向你展示一段用户与大模型的历史对话记录，user 表示用户，assistant 表示大模型，你需要从中判断对话属于哪个场景。

    ## Goals:
    - 你的任务是准确判断最新的用户提问符合哪个场景，用户身处在哪个场景，用户想要大模型提供哪种场景下的帮助。

    ## Constraints:
    - 你只需要用代表场景标签的数字回复（例如场景标签是"4：送祝福"，则回复数字 "4"），不需要回复其他任何内容！，不要返回不纯在的场景标签。
    - 你需要根据历史对话记录判断用户的场景是否发生改变，如果是，回复最新的场景即可。
    - 如果历史对话都不符合场景标签选项，请只返回字符串"None"。
    - 你无需输出思考过程，直接返回答案即可。

    ## Attention:
    - 有些用户提问看似与场景无关，但是实际上此用户回复是回答大模型关于场景的详细提问。
    - 有些用户提问是想更换场景要素，但是主要的场景并没有发生改变（例如从 "送祝福给爸爸" 换成 "送祝福给妈妈"，但是场景还是"4：送祝福"）。
    - 对于答非所问同时没有想更换场景要素的用户回复，你可以判断为都不符合以上的场景标签选项。
    - 你可以通过查看场景标签选项的细分场景来辅助判断用户提问符合哪个场景。

    ## Inputs:
    - 历史对话记录：```{instruction}```
    - 场景标签选项: ```{scene}```
    - 关于场景标签选项的细分场景:```{scene_example}```

    ## Workflows:
    ### Step 1: 使用关于场景标签选项的细分场景作为辅助判断用户对话符合哪个场景标签。
    ### Step 2: 如果现不符合场景的用户对话，进一步判断此对话是否是对上一个大模型提问所做出的回答，以及是否更换场景要素。

    ## Example:
    ### example 1:
    #### 历史对话记录：```[user:"我想为我的朋友送上祝福",assistant:"请问你想在哪个节日上送上祝福",user:"我朋友的生日",assistant:"请问你朋友的年龄段是？",user:"18岁",
    assistant:"你想以什么样的语言风格为他送上祝福？",user:"小红书风格"]```
    #### step 1(思考过程): 通过分析历史对话记录，可以判断为用户想祝朋友生日快乐，所以符合场景"4：送祝福"。
    #### step 2(思考过程): 在对话中发现以下用户回复不符合场景 ```user:"我朋友的生日",user:"18岁",user:"小红书风格"```，通过进一步判断，用户是在回答大模型的提问，所以总结用户提问符合场景"4：送祝福"，返回数字"4"。

    ### example 2:
    #### 历史对话记录：```[user:"我正在相亲，好尴尬",assistant:"请问你目前的聊天场合是？",user:"我和他正在餐厅吃饭",assistant:"请问对象目前的情绪是什么，例如乏累",user:"生气",
    assistant:"请问现在的时间段是？",user:"请问今天的天气"]```
    #### step 1(思考过程): 通过分析历史对话记录，可以判断为用户想祝朋友生日快乐，所以符合场景"6：化解尴尬场合"。
    #### step 2(思考过程): 在对话中发现以下用户回复不符合场景```user:"请问今天的天气" ```，通过进一步判断，此回复并不是在回答大模型的提问，属于答非所问，且此提问不是更换场景要素相关的，因此返回"None"字段。

    ### example 3:
    #### 历史对话记录：```[user:"我想送礼给我的老板",assistant:"请问你老板的性格是怎么样的呢？",user:"开朗",assistant:"好的，正在为你搜寻合适的方法",user:"我说错了，他有点严肃"]```
    #### step 1(思考过程): 通过分析历史对话记录，可以判断为用户送礼给老板，所以符合场景"3：送礼礼仪文化"。
    #### step 2(思考过程): 在对话中发现以下用户回复不符合场景```user:"我说错了，他有点严肃" ```，通过进一步判断，此回复并不是在回答大模型的提问，属于答非所问，但是是用户想要更换场景要素，并且主要场景没有发生改变，返回数字"3"。

    """
    name: str = "IntentAnalyze"

    async def run(self, instruction: str):
        json_data = load_json("scene_attribute.json")
        scene = extract_all_types(json_data)
        scene_example = extract_all_types_and_examples(json_data)

        prompt = self.PROMPT_TEMPLATE.format(
            instruction=instruction, scene=scene, scene_example=scene_example
        )

        rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)

        logger.info("机器人分析需求：\n" + rsp)

        return rsp
