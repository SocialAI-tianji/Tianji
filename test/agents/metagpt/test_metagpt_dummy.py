import asyncio
import re
import subprocess
from dotenv import load_dotenv
load_dotenv()
import fire

from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from tianji.agents.metagpt_agents.utils.agent_llm import ZhipuApi as LLMApi

class SimpleCalculator(Action):
    """一个简单的计算Action"""
    name: str = "SimpleCalculator"
    
    async def run(self, instruction: str) -> str:
        """执行简单的加法运算
        Args:
            instruction: 格式为"数字1 + 数字2"的字符串
        Returns:
            计算结果的字符串
        """
        try:
            # 解析输入
            print(f"当前run ： {type(instruction)},{instruction}")
            num1, num2 = map(int, instruction.split('+'))
            result = f"{num1} + {num2} = {num1 + num2}"
            logger.info(f"计算结果: {result}")
            return result
        except Exception as e:
            error_msg = f"计算错误: {str(e)}"
            logger.error(error_msg)
            return error_msg

class CalculatorAssistant(Role):
    """计算助手角色
    
    ReAct 循环的模式，目前支持 REACT、BY_ORDER、PLAN_AND_ACT 3种模式，
    默认使用 REACT 模式。在 _set_react_mode 方法中有相关说明。简单来说，BY_ORDER 模式按照指定的 Action 顺序执行。
    PLAN_AND_ACT 则为一次思考后执行多个动作，即 _think -> _act -> act -> ...，
    而 REACT 模式按照 ReAct 论文中的思考——行动循环来执行，即 _think -> _act -> _think -> _act -> ...。
    """
    name: str = "Calculator"
    profile: str = "一个简单的计算助手，负责计算两个数字的和"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleCalculator])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        print(f"当前_act ： {type(self.rc.todo)},{self.rc.todo}")

        msg = self.get_memories(k=1)[0]  # 获取最近的消息
        result = await todo.run(msg.content)
        
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        return msg

def run_example(msg: str):
    """运行单个计算示例"""
    role = CalculatorAssistant()
    logger.info(f"输入: {msg}")
    result = asyncio.run(role.run(msg))
    logger.info(f"结果: {result}")
    print("-" * 50)

def main():
    """运行多个计算示例"""
    # 基本加法示例
    run_example("5 + 3")
    
    # 大数加法示例
    run_example("1234 + 5678")
    
    # 负数加法示例
    run_example("-10 + 5")
    
    # 错误输入示例
    run_example("abc + def")
    
    # 零的加法示例
    run_example("0 + 100")

if __name__ == "__main__":
    fire.Fire(main)