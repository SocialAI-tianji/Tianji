from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append("MetaGPT")
from metagpt.roles import Role
from metagpt.schema import Message
from .action import read_and_ana,rerask

class wendao(Role):
    def __init__(
        self,
        name: str = "wendao",
        profile: str = "GetInformation",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([read_and_ana,rerask])
        self._set_react_mode(react_mode="by_order")

    '''
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
    '''
    async def _act_by_order(self) -> Message:
        """switch action each time by order defined in _init_actions, i.e. _act (Action1) -> _act (Action2) -> ..."""
        for i in range(len(self._states)):
            self._set_state(i)
            rsp = await self._act()
        return rsp  # return output from the last action