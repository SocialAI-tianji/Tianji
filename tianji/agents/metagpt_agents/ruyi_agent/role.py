from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from .action import writeMD


class ruyi(Role):
    name: str = "ruyi"
    profile: str = "stylize"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([writeMD])
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]  # find the most k recent messagesA
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
