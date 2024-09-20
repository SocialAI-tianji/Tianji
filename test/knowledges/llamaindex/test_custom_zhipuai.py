from llama_index.core.chat_engine import SimpleChatEngine
from tianji.knowledges.llamaindex_onlinellm.models import ZhipuLLM

# 使用自定义的ZhipuLLM模型
llm = ZhipuLLM()

# 配置聊天引擎
chat_engine = SimpleChatEngine.from_defaults(llm=llm)

# 与模型进行聊天（非流式）
response = chat_engine.chat("说一些关于春节的深刻的话")
print(response)

# 与模型进行流式聊天
streaming_response = chat_engine.stream_chat("说一些关于春节的浪漫的话")
for token in streaming_response.response_gen:
    print(token, end="", flush=True)
print()  # 打印一个换行符
