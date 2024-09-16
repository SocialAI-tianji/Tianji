from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import sceneRefineAnalyze,RaiseQuestion
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.helper_for_agent import *

class sceneRefine(Role):
    name: str = "sceneRefinement"
    profile: str = "Scene Refinement Analyze"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([sceneRefineAnalyze,RaiseQuestion])
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
        while True:
            await self._think()
            if self.rc.todo is None:
                break
            msg = await self._act()
        return msg
