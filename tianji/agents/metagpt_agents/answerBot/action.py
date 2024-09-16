from dotenv import load_dotenv

load_dotenv()

from typing import Optional, Any
import json

from metagpt.actions import Action
from metagpt.logs import logger
from copy import deepcopy
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.common_llm_api import LLMApi
from tianji.utils.helper_for_agent import *
from metagpt.const import METAGPT_ROOT as TIANJI_PATH

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
    
    ## Input:
    - 历史对话记录：```{instruction}```
    - 场景要素: ```{scene_attributes}``
    - 场景要素的描述以及例子:```{scene_attributes_description}```
    """
    name: str = "AnswerQuestion"
    async def run(self, instruction: str):

        sharedData = SharedDataSingleton.get_instance()
        scene_label=sharedData.scene_label
        scene_attributes=sharedData.scene_attribute

        json_data=load_json("scene_attribute.json")
        scene,_,_=extract_single_type_attributes_and_examples(json_data,scene_label)

        scene_attributes_description=extract_attribute_descriptions(json_data,scene_attributes)

        prompt = self.PROMPT_TEMPLATE.format(
            scene=scene,scene_attributes=scene_attributes,scene_attributes_description=scene_attributes_description,instruction=instruction
        )
        rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
        return rsp