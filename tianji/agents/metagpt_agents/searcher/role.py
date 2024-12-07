from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import (
    QueryExpansion,
    WebSearch,
    SelectResult,
    SelectFetcher,
    FilterSelectedResult,
)

"""
网络搜索助手 agent，将会使用以下行动：
action 1 （QueryExpansion）：基于用户以及大模型的对话记录，用户所面对的场景，进行查询扩展。
action 2 （WebSearch）：进行网络搜索（duckduckgo_Search），返回网页片段帮助决策。
action 3 （SelectResult）：基于返回的网页片段，判断哪些网页需要进一步查询。
action 4 （SelectFetcher）：通过 requests 模块爬取网页里的内容。
action 5 （FilterSelectedResult）：对爬取的网页内容进行过滤，并且加入到结果中。
"""

class Searcher(Role):
    name: str = "Searcher"
    profile: str = "Get extra result from search engine"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions(
            [
                QueryExpansion,
                WebSearch,
                SelectResult,
                SelectFetcher,
                FilterSelectedResult,
            ]
        )
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
