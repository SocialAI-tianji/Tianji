from dotenv import load_dotenv

load_dotenv()

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import IntentAnalyze

"""
意图识别智能体 (IntentReg)

该模块负责理解和分析用户输入，将用户问题映射到预定义的场景类型中。
它是整个系统的第一个处理环节，为后续的场景细化和回答生成提供基础。

主要功能：
1. 分析用户输入的自然语言文本
2. 识别用户当前的意图和需求
3. 将用户问题匹配到预定义的场景类型
4. 输出场景标签供后续处理

工作流程：
1. 接收用户输入
2. 使用LLM分析用户意图
3. 匹配到预定义场景
4. 返回场景标签
"""


class IntentReg(Role):
    """意图识别智能体
    
    该智能体负责理解用户输入并映射到预定义场景。它是系统的第一个处理环节，
    为后续的场景细化和回答生成提供基础。
    
    属性:
        name (str): 角色名称
        profile (str): 角色描述
    """
    name: str = "IntentReg"
    profile: str = "Intent Analyze"

    def __init__(self, **kwargs):
        """初始化意图识别智能体
        
        设置智能体的动作和反应模式。使用BY_ORDER模式确保动作按顺序执行。
        
        参数:
            **kwargs: 额外的初始化参数
        """
        super().__init__(**kwargs)
        self.set_actions([IntentAnalyze])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        """执行意图识别动作
        
        处理用户输入并返回识别结果。
        
        返回:
            Message: 包含识别结果的消息对象
        """
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]  # 获取最近的一条消息
        result = await todo.run(msg.content)  # 运行意图分析

        # 创建并存储结果消息
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
