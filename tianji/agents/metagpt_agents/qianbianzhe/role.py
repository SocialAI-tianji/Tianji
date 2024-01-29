from dotenv import load_dotenv

load_dotenv()

from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from metagpt.logs import logger
from .action import AnsWrite, Stylize


# 千变者 以自己的身份回答问题
class QianBianZhe(Role):
    name: str = "QianBianZhe"
    profile: str = "Stylize"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([AnsWrite, Stylize])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)

        return msg
