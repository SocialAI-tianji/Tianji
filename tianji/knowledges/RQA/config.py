# from metagpt.const import METAGPT_ROOT as TIANJI_PATH
class RQA_ST_Liyi_Chroma_Config:
    """
    检索问答增强（RQA）配置文件：
    基于Chroma检索数据库；
    基于Sentence-Transformer词向量模型构建的外挂礼仪（Liyi）知识库。
    """

    # 原始数据位置 online 设置为空
    ORIGIN_DATA = ""
    # 持久化数据库位置，例如 Tianji/tianji/knowledges/liyi/chroma
    PERSIST_DIRECTORY = "/root/code/Tianji/tianji/knowledges/RQA/.storage/chroma/liyi/chroma.sqlite3"  # TIANJI_PATH + "/Tianji/tianji/knowledges/liyi/chroma"
    # Sentence-Transformer词向量模型权重位置
    HF_SENTENCE_TRANSFORMER_WEIGHT = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
