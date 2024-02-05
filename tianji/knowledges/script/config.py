class RQA_ST_Liyi_Chroma_Config:
    """
    检索问答增强（RQA）配置文件：
    基于Chroma检索数据库；
    基于Sentence-Transformer词向量模型构建的外挂礼仪（Liyi）知识库。
    """

    # 原始数据位置
    ORIGIN_DATA = ""
    # 持久化数据库位置，例如 Tianji/tianji/knowledges/liyi/chroma
    PERSIST_DIRECTORY = ""
    # Sentence-Transformer词向量模型权重位置
    HF_SENTENCE_TRANSFORMER_WEIGHT = ""
