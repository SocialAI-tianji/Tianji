from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import RecvAndAnalyze, RaiseQuestion


class WenDao(Role):
    name: str = "WenDao"
    profile: str = "GetInformation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([RecvAndAnalyze, RaiseQuestion])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg

    async def _act_by_order(self) -> Message:
        for i in range(len(self.states)):
            self._set_state(i)
            rsp = await self._act()
        return rsp
