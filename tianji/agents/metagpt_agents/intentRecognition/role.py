from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import IntentAnalyze

"""
意图识别 agent，具体作用为基于用户与大模型的对话记录，场景标签选项以及，场景标签选项的细分场景，识别用户目前的意图属于哪个场景（具体场景设置请参考 scene_attribute.json）。
"""


class IntentReg(Role):
    name: str = "IntentReg"
    profile: str = "Intent Analyze"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([IntentAnalyze])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
