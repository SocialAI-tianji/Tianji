import os
from dotenv import load_dotenv
from tianji.knowledges.langchain_onlinellm.models import SiliconFlowLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio

load_dotenv()


def test_call():
    model = SiliconFlowLLM()
    question = "今天天气如何"
    response = model._call(question)
    print(response)


async def test_langchain_api():
    prompt = ChatPromptTemplate.from_messages(
        [("system", "你是一个助手"), ("human", "{input}")]
    )

    llm = SiliconFlowLLM()
    chain = prompt | llm

    idx = 0
    async for event in chain.astream_events({"input": "你好！"}, version="v1"):
        print(event)
        idx += 1
        if idx > 7:
            break


async def main():
    test_call()
    await test_langchain_api()


if __name__ == "__main__":
    asyncio.run(main())
