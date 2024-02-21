# Agent 使用说明
一共包含3个步骤：

1. 准备数据
2. 构建embdding数据库
3. 根据自定义embdding数据库，实现Agent智能体

# 数据准备
参考[text](Tianji/tianji/knowledges/RQA/script/process_data.py)

# 构建embdding数据库
填写配置文件
```python
# 原始数据位置 online 设置为空
ORIGIN_DATA = ""
# 持久化数据库位置，例如 chroma/liyi/
PERSIST_DIRECTORY = ""
# Sentence-Transformer词向量模型权重位置
HF_SENTENCE_TRANSFORMER_WEIGHT = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```
运行脚本，基于Chroma构建向量数据库
```python
python Tianji/tianji/knowledges/RQA/emb.py
```

# 运行Agent智能体Demo
```python 
python Tianji/run/tianji_rqa_demo.py
```