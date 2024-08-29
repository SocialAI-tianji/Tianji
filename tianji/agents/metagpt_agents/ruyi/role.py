# 此文件定义了RuYi角色，负责处理特定的任务并生成相应的消息。

from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from metagpt.logs import logger
from .action import WriteMarkDown


class RuYi(Role):
    name: str = "RuYi"
    profile: str = "Stylize"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([WriteMarkDown])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)

        return msg
