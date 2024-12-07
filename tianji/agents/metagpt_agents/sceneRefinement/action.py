from dotenv import load_dotenv

load_dotenv()

import json
from metagpt.actions import Action
from metagpt.logs import logger
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.agent_llm import ZhipuApi as LLMApi
from tianji.agents.metagpt_agents.utils.helper_func import extract_single_type_attributes_and_examples, extract_attribute_descriptions, load_json

"""
场景细化 agent 所对应的 action。
"""


class sceneRefineAnalyze(Action):
    PROMPT_TEMPLATE: str = """
    #Role:
    - 场景细化小助手

    ## Background:
    - 作为一个专业的{scene}场景分析助手。接下来，我将向你展示一段用户与大模型的历史对话记录，user 表示用户，assistant 表示大模型，你需要从中提取相对应的场景要素并组装成json。

    ## Goals:
    - 我将提供给你需要提取的场景要素，你的任务是从历史对话记录中的内容分析并提取对应场景的场景要素。

    ## Constraints:
    - 你只需要返回单个 json 对象，不需要回复其他任何内容！，不要返回我提供以外的场景要素。
    - 如果没有提取到对应的场景要素请用空字符串表示，例如："对象角色": ""
    - 你需要根据最新的对话记录判断场景要素是否发生改变，如果是，把旧的要素替换成新的（例如"对象角色"从"爸爸"变成"妈妈"）。

    ## Attention:
    - 你可以通过查看我所提供的场景要素的描述以及例子来辅助提取对应场景的场景要素。

    ## Input:
    - 历史对话记录：```{instruction}```
    - 需要提取的场景要素: ```{scene_attributes}``
    - 每个场景要素的描述以及例子:```{scene_attributes_description}```

    ## Workflows:
    ### Step 1: 通过查看场景要素的描述以及例子，思考对话记录中有没有对应的场景要素。
    ### Step 2: 继续查看对话记录以判断已经提取的场景要素有没有发生更新，如果有，就把旧的替换掉。

    ## Example:
    ### example 1:
    #### 历史对话记录：```[user:"我想为我的朋友送上祝福",assistant:"请问你想在哪个节日上送上祝福",user:"我朋友的生日",assistant:"请问你朋友的年龄段是？",user:"18岁",
    assistant:"你想以什么样的语言风格为他送上祝福？",user:"小红书风格"]```
    #### step 1(思考过程): 通过分析每个场景要素的描述以及例子，以及查看要提取的场景要素，分析对话中拥有以下场景要素{{"节日":"生日","对象角色":"朋友","对象年龄段":"少年","语言风格":"小红书"}}。
    #### step 2(思考过程): 已经提取的场景要素并没有发生更新。

    ### example 2:
    #### 历史对话记录：```[user:"我正在相亲，好尴尬",assistant:"请问你目前的聊天场合是？",user:"我和他正在餐厅吃饭",assistant:"请问对象目前的情绪是什么，例如乏累",user:"他看起来有点生气"]```
    #### step 1(思考过程): 通过分析每个场景要素的描述以及例子，以及查看要提取的场景要素，分析对话中拥有以下场景要素{{"语言场景":"餐厅用餐","对象角色":"相亲对象","对象情绪":"乏累","对象状态":"","时间":""}}。
    #### step 2(思考过程): 已经提取的场景要素并没有发生更新。

    ### example 3:
    #### 历史对话记录：```[user:"我想送礼给我的老板",assistant:"请问你老板的性格是怎么样的呢？",user:"开朗",assistant:"好的，正在为你搜寻合适的方法",user:"我说错了，他有点严肃"]```
    #### step 1(思考过程): 通过分析每个场景要素的描述以及例子，以及查看要提取的场景要素，分析对话中拥有以下场景要素{{"对象角色":"老板","对象性格":"开朗","对象职业":""}}。
    #### step 2(思考过程): 已经提取的场景要素发生更新，"对象性格" 从 "开朗" 改变成 "严肃"，返回{{"对象角色":"老板","对象性格":"严肃","对象职业":""}}。
    """

    name: str = "sceneRefineAnalyze"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()
        scene_label = sharedData.scene_label

        scene_attributes = sharedData.scene_attribute

        json_data = load_json("scene_attribute.json")
        scene, scene_attributes, _ = extract_single_type_attributes_and_examples(
            json_data, scene_label
        )

        scene_attributes_description = extract_attribute_descriptions(
            json_data, scene_attributes
        )

        prompt = self.PROMPT_TEMPLATE.format(
            instruction=instruction,
            scene=scene,
            scene_attributes=scene_attributes,
            scene_attributes_description=scene_attributes_description,
        )

        max_retry = 5
        for attempt in range(max_retry):
            try:
                rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
                logger.info("机器人分析需求：\n" + rsp)
                rsp = (
                    rsp.replace("```json", "")
                    .replace("```", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("“", '"')
                    .replace("”", '"')
                    .replace("，", ",")
                )
                sharedData.scene_attribute = json.loads(rsp)
                logger.info("机器人分析需求：\n" + rsp)
                return rsp
            except:
                pass
        raise Exception("sceneRefinement agent failed to response")


class RaiseQuestion(Action):
    PROMPT_TEMPLATE: str = """
    #Role:
    - 提问小助手

    ## Goals:
    - 作为一个专业的提问小助手。接下来，我将提供你用户面对的场景，场景要素，以及每个场景要素的描述以及例子.
    - 你需要结合当前场景以及为空的场景要素,进行提问的返回
    - 例如,场景是送祝福，空的场景要素为 "对象角色": "" ，此时你才需要提问：请问你想要送祝福给谁呢？是妈妈吗？ 如果不为空,你不需要做任何事情.

    ## Constraints:
    - 如果所有场景要素都有，则不需要提问，直接返回字段"Full"。
    - 你每次只能提问一个问题。
    - 你无需输出思考过程，直接返回提问即可。

    ## Input:
    - 用户面对的场景：```{scene}```
    - 当前场景要素: ```{scene_attributes}``
    - 每个场景要素的描述以及例子:```{scene_attributes_description}```

    ## Workflows:
    ### Step 1: 判断空的场景要素是什么。
    ### Step 2: 结合用户面对的场景以及场景要素的描述以及例子进行提问。

    ## Example:
    ### example 1:
    #### 用户面对的场景："4：送祝福"
    #### 场景要素：```{{"节日":"生日","对象角色":"朋友","对象年龄段":"少年","语言风格":"小红书"}}```
    #### step 1(思考过程): 没有为空的场景要素，返回字段"Full"。

    ### example 2:
    ### 用户面对的场景："6：化解尴尬场合"
    #### 场景要素：```{{"语言场景":"餐厅用餐","对象角色":"相亲对象","对象情绪":"乏累","对象状态":"","时间":""}}```
    #### step 1(思考过程): 空的场景要素为"对象状态":""以及"时间":""。
    #### step 2(思考过程): 结合场景要素的描述以及例子，返回提问："请问目前相亲对象状态是怎么样的？，他也表现得很尴尬吗？，还是？"。

    ### example 3:
    #### 用户面对的场景："3：送礼礼仪文化"
    #### 历史对话记录：```{{"对象角色":"老板","对象性格":"开朗","对象职业":""}}```
    #### step 1(思考过程): 空的场景要素为"对象职业":""。
    #### step 2(思考过程): 结合场景要素的描述以及例子，返回提问："请问您的老板从事哪个行业？，例如科技行业还是教育行业？"
    """
    name: str = "RaiseQuestion"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()
        scene_label = sharedData.scene_label
        scene_attributes = sharedData.scene_attribute

        json_data = load_json("scene_attribute.json")
        scene, _, _ = extract_single_type_attributes_and_examples(
            json_data, scene_label
        )

        scene_attributes_description = extract_attribute_descriptions(
            json_data, scene_attributes
        )

        prompt = self.PROMPT_TEMPLATE.format(
            scene=scene,
            scene_attributes=scene_attributes,
            scene_attributes_description=scene_attributes_description,
        )
        rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
        logger.info("机器人分析需求：\n" + rsp)
        return rsp
