import os
from enum import Enum
from metagpt.const import METAGPT_ROOT as TIANJI_PATH
from metagpt.logs import logger

"""
def get_all_knowledge_paths(knowledge_path: str = METAGPT_ROOT, suffix: str = ".txt"):
    files = os.listdir(knowledge_path)
    all_knowledge_paths = []
    for file in files:
        file_path = os.path.join(knowledge_path, file)
        if os.path.isdir(file_path):
            all_knowledge_paths.extend(get_all_knowledge_paths(file_path))
        else:
            if file_path.endswith(suffix):
                all_knowledge_paths.append(knowledge_path)
    return all_knowledge_paths
"""


class AGENT_KNOWLEDGE_PATH(str, Enum):
    WISHES = TIANJI_PATH / "tianji/agents/knowledges/04-Wishes"

    def path(self):
        load_path = self.value
        logger.info("加载知识库：" + load_path)

        return os.path.join(load_path, "knowledges.txt")


class AGENT_EMBEDDING_PATH(str, Enum):
    WISHES = TIANJI_PATH / "temp/embedding/04-Wishes"

    def path(self, filename="other"):
        save_path = os.path.join(self.value, filename)
        logger.info("Embedding 路径：" + save_path)

        return save_path
