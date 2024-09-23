from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import QueryExpansion,WebSearch,SelectResult,SelectFetcher,FilterSelectedResult
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.helper_for_agent import *

class Searcher(Role):
    name: str = "Searcher"
    profile: str = "Get extra result from search engine"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([QueryExpansion,WebSearch,SelectResult,SelectFetcher,FilterSelectedResult])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)


    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
