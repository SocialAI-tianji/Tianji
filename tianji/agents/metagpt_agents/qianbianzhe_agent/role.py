from .action import *
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger

# 千变者 以自己的身份回答问题
class qianbianzhe(Role):
    def __init__(
        self,
        name: str = "qianbianzhe",
        profile: str = "stylize",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([ansWrite,stylize])
        print("byorder")
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        # By choosing the Action by order under the hood
        # todo will be first SimpleWriteCode() then SimpleRunCode()
        todo = self._rc.todo

        msg = self.get_memories(k=1)[0] # find the most k recent messagesA
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self._rc.memory.add(msg)
        return msg

# async def main():
#     # 对话导入
#     msg = "test"
#     role = qianbianzhe()
#     logger.info(msg)
#     result = await role.run(msg)
#     logger.info(result)

# asyncio.run(main())
