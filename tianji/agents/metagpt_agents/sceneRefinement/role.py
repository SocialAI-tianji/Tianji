from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import sceneRefineAnalyze, RaiseQuestion
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.helper_func import *

"""
场景细化 agent，具体作用为：
action 1 （sceneRefineAnalyze）: 信息抽取，基于用户与大模型的对话记录，
获得场景要素的描述以及例子，抽取出个别场景所需要的要素，
以便后续大模型可以提供更详细的回答（具体场景要素置请参考 scene_attribute.json）。

action 2 （RaiseQuestion）:提问助手，对于没有抽取到的场景要素，
大模型会进一步对用户做出提问（以提问方式要求用户补充该场景要素）。
"""


class SceneRefine(Role):
    name: str = "sceneRefinement"
    profile: str = "Scene Refinement Analyze"

    # RoleReactMode.REACT 模式下，agent运行过程为 _react -> _think -> _act
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([sceneRefineAnalyze, RaiseQuestion])
        self._set_react_mode(react_mode=RoleReactMode.REACT.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        if type(todo) is RaiseQuestion:
            return msg
        else:
            return Message(content="", role=self.profile, cause_by=type(todo))

    # 如果全部场景要素都不为空的情况下，直接跳过 RaiseQuestion action，不再向用户提问
    async def _think(self) -> None:
        sharedData = SharedDataSingleton.get_instance()
        if not has_empty_values(sharedData.scene_attribute):
            self.rc.todo = None
            return
        if self.rc.state + 1 < len(self.states):
            self._set_state(self.rc.state + 1)
        else:
            self.rc.todo = None

    async def _react(self) -> Message:
        msg=None
        while True:
            await self._think()
            if self.rc.todo is None:
                break
            msg = await self._act()
        return msg
