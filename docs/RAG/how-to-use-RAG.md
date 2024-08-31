# RAG 对话系统

这是一个基于检索增强生成（RAG）的对话系统，使用 Gradio 构建用户界面。系统可以根据用户提供的知识库回答问题，支持文件夹和网页两种数据源。

## 主要特点

- 使用自定义的智谱AI（ZhipuAI）LLM 和 Embedding 模型
- 支持 HuggingFace 和 ZhipuAI 两种 Embedding 选项
- 可选择文件夹或网页作为知识库数据源
- 可自定义文本分块大小、缓存路径等参数
- 使用 Chroma 作为向量数据库
- 提供友好的 Gradio 用户界面

## 使用方法

1. 安装依赖：
   pip install -r requirements.txt

1. 设置环境变量：
   在 `.env` 文件中设置必要的 API 密钥等信息。

1. 运行程序：
   python run/demo_rag_langchain_onlinellm.py

1. 在 Gradio 界面中：

- 选择 Embedding 模型（HuggingFace 或 ZhipuAI）
- 设置文本块大小
- 指定缓存和数据库路径
- 选择数据源类型（文件夹或网页）
- 提供数据路径
- 点击"初始化数据库"按钮
- 在聊天框中输入问题并开始对话

## 注意事项

- 初始化数据库可能需要一些时间，请耐心等待
- 如遇到异常，错误信息会显示在文本输入框中
- 本系统使用自定义的智谱AI（ZhipuAI）LLM 和 Embedding 模型，需要相应的 API 密钥

## 主要函数

- `create_embeddings`: 创建 Embedding 模型
- `create_vectordb`: 创建或加载向量数据库
- `initialize_chain`: 初始化 RAG 链
- `handle_question`: 处理用户问题
- `update_settings`: 更新设置并初始化模型
