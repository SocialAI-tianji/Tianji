from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import AnswerQuestion

"""
回答助手 agent，具体作用为基于用户与大模型的对话记录，场景标签选项以及，场景要素的描述以及例子，做出回答以解决用户关于人情世故的提问。
"""


class AnswerBot(Role):
    name: str = "Answer Bot"
    profile: str = "Answer User question"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnswerQuestion])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
