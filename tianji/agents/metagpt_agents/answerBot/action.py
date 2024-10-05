from dotenv import load_dotenv

load_dotenv()

from metagpt.actions import Action
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.agent_llm import ZhipuApi as LLMApi
from tianji.agents.metagpt_agents.utils.helper_func import *

"""
回答助手 agent 所对应的 action。
"""


class AnswerQuestion(Action):
    PROMPT_TEMPLATE: str = """
    #Role:
    - {scene}小助手

    ## Goals:
    - 作为一个专业的{scene}小助手。你需要参考用户与大模型的历史对话记录（user 表示用户，assistant 表示大模型），场景细化要素，以及每个场景要素的描述以及例子，做出回答，帮助用户解决在该场景下所面对的问题。

    ## Constraints:
    - 你的回答需要基于提供的场景要素进行定制化，提供详细的例子，避免使用概括性或泛泛而谈的表述。

    ## Attention:
    - 场景要素里的详细描述可以参考所提供的场景要素的描述以及例子。
    - 如果搜索引擎结果不为空，你需要完全以其为基础，并做出回答。

    ## Input:
    - 历史对话记录：```{instruction}```
    - 场景要素: ```{scene_attributes}``
    - 场景要素的描述以及例子:```{scene_attributes_description}```
    - 搜索引擎结果：```{search_result}```
    """
    name: str = "AnswerQuestion"

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

        search_results = sharedData.search_results
        filtered_dict = {}

        for index, item in search_results.items():
            if "filtered_content" in item:
                filtered_dict[index] = item["filtered_content"]

        prompt = self.PROMPT_TEMPLATE.format(
            scene=scene,
            scene_attributes=scene_attributes,
            scene_attributes_description=scene_attributes_description,
            instruction=instruction,
            search_result=filtered_dict
            if filtered_dict is not None and filtered_dict
            else "",
        )

        rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
        return rsp
