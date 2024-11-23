"""
使用说明：
本脚本演示了如何使用SiliconFlow的嵌入模型进行文本检索。

主要功能:
1. 使用SiliconFlow的嵌入模型
2. 创建向量索引
3. 进行文本检索和相似度匹配
"""

import time
from llama_index.core.schema import Document
from llama_index.core.response.pprint_utils import pprint_source_node
from llama_index.core import Settings, VectorStoreIndex
from tianji.knowledges.llamaindex_onlinellm.models import SiliconFlowEmbeddings

# 设置嵌入模型
Settings.embed_model = SiliconFlowEmbeddings()
Settings.chunk_size = 2048  # chunk_size大小

# 准备示例数据
texts = ["北京", "上海", "广州", "深圳", "苹果", "香蕉", "橙子", "葡萄", "足球", "篮球", "网球", "乒乓球"]
documents = [Document(text=txt) for txt in texts]

# 构建索引
index = VectorStoreIndex.from_documents(documents)

# 作为检索器
ES = index.as_retriever(similarity_top_k=5)

# 示例查询
示例查询 = ["一线城市", "水果", "球类运动", "中国城市"]

print("以下是一些示例查询及其结果：")
for query in 示例查询:
    print(f"\n查询: {query}")
    print("─" * 40)
    start_time = time.time()
    res = ES.retrieve(query)
    cost_time = time.time() - start_time
    print(f"耗时: {cost_time*1000:.2f}毫秒")
    for idx, result in enumerate(res):
        pprint_source_node(result)

# 句子匹配测试
print("\n句子匹配测试：")
句子查询 = [
    "我想去中国的大城市旅游",
    "我想吃一些新鲜的水果",
    "我喜欢看各种球类比赛",
    "我想尝试一些不同口味的水果",
    "中国南方和北方的大城市有什么区别",
    "哪些球类运动适合室内进行",
]

for query in 句子查询:
    print(f"\n查询: {query}")
    print("─" * 40)
    start_time = time.time()
    res = ES.retrieve(query)
    cost_time = time.time() - start_time
    print(f"耗时: {cost_time*1000:.2f}毫秒")
    for idx, result in enumerate(res):
        pprint_source_node(result)
