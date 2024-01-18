'''
Filename: MetaGPT/examples/agent_creator.py
Created Date: Tuesday, September 12th 2023, 3:28:37 pm
Author: garylin2099
'''
import re

from metagpt.const import PROJECT_ROOT, WORKSPACE_ROOT
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger

with open(PROJECT_ROOT / "examples/build_customized_agent.py", "r") as f:
    # use official example script to guide AgentCreator
    MULTI_ACTION_AGENT_CODE_EXAMPLE = f.read()

class CreateAgent(Action):

    PROMPT_TEMPLATE = """
    ### BACKGROUND
    You are using an agent framework called metagpt to write agents capable of different actions,
    the usage of metagpt can be illustrated by the following example:
    ### EXAMPLE STARTS AT THIS LINE
    {example}
    ### EXAMPLE ENDS AT THIS LINE
    ### TASK
    Now you should create an agent with appropriate actions based on the instruction, consider carefully about
    the PROMPT_TEMPLATE of all actions and when to call self._aask()
    ### INSTRUCTION
    {instruction}
    ### YOUR CODE
    Return ```python your_code_here ``` with NO other texts, your code:
    """

    async def run(self, example: str, instruction: str):

        prompt = self.PROMPT_TEMPLATE.format(example=example, instruction=instruction)
        # logger.info(prompt)

        rsp = await self._aask(prompt)

        code_text = CreateAgent.parse_code(rsp)

        return code_text

    @staticmethod
    def parse_code(rsp):
        pattern = r'```python(.*)```'
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else ""
        if not WORKSPACE_ROOT.exists():
            WORKSPACE_ROOT.mkdir(parents=True)
        with open(WORKSPACE_ROOT / "agent_created_agent.py", "w") as f:
            f.write(code_text)
        return code_text

class AgentCreator(Role):
    def __init__(
        self,
        name: str = "Matrix",
        profile: str = "AgentCreator",
        agent_template: str = MULTI_ACTION_AGENT_CODE_EXAMPLE,
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([CreateAgent])
        self.agent_template = agent_template

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        todo = self._rc.todo
        msg = self._rc.memory.get()[-1]

        instruction = msg.content
        code_text = await CreateAgent().run(example=self.agent_template, instruction=instruction)
        msg = Message(content=code_text, role=self.profile, cause_by=todo)

        return msg

if __name__ == "__main__":
    import asyncio

    async def main():

        agent_template = MULTI_ACTION_AGENT_CODE_EXAMPLE

        creator = AgentCreator(agent_template=agent_template)

        # msg = """Write an agent called SimpleTester that will take any code snippet (str)
        #     and return a testing code (str) for testing
        #     the given code snippet. Use pytest as the testing framework."""

        msg = """
        Write an agent called SimpleTester that will take any code snippet (str) and do the following:
        1. write a testing code (str) for testing the given code snippet, save the testing code as a .py file in the current working directory;
        2. run the testing code.
        You can use pytest as the testing framework.
        """
        await creator.run(msg)

    asyncio.run(main())
