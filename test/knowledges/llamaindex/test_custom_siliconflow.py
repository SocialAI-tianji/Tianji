from llama_index.core.chat_engine import SimpleChatEngine
from tianji.knowledges.llamaindex_onlinellm.models import SiliconFlowLLM

# 使用自定义的SiliconFlowLLM模型
llm = SiliconFlowLLM()

# 配置聊天引擎
chat_engine = SimpleChatEngine.from_defaults(llm=llm)

# 与模型进行聊天（非流式）
response = chat_engine.chat("请说明你是谁")
print(response)

# 与模型进行流式聊天
streaming_response = chat_engine.stream_chat("请说明你是谁")
for token in streaming_response.response_gen:
    print(token, end="", flush=True)
print()  # 打印一个换行符
