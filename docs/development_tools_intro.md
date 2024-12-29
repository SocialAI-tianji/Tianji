# 天机开发工具介绍

本文档介绍了天机项目中 `tools` 目录下的各种开发工具，这些工具主要用于数据处理、模型训练和提示词工程等任务。每个工具都经过实践检验，能够有效提升开发效率。

## 目录结构

```bash
tools/
├── finetune/          # 模型微调相关工具
│   ├── data_maker/    # 数据制作工具
│   ├── data2txt/      # 数据转换工具
│   └── datajson_refiner/  # 数据清洗工具
├── rag/               # RAG知识库构建工具
└── prompt_maker/      # 提示词工程工具
```
## 快速指南：我想要...

### 1. 构建提示词应用
- 编写和验证提示词模板 → `prompt_maker/prompt_to_json.py`
- 批量处理多个提示词 → `prompt_maker/prompt_to_json_in_bulk.py`
- 检查提示词质量 → `prompt_maker/check_prompt_template_in_bulk.py`
- 测试提示词效果 → `prompt_maker/web_demo.py`

### 2. 构建知识库问答（RAG工具系列）
- 数据获取与预处理：
  - 抓取网页内容 → `rag/url2article.md`
  - 处理长文本分块 → `rag/article2chunk.js`
  
- 数据质量控制：
  - 使用LLM过滤低质量数据 → `rag/0-data_llm_filter.py`
  - 过滤负面样本 → `rag/0-data_llm_filter_negative.py`
  - 过滤过短文本 → `rag/0-data_llm_filter_lesswords.py`
  
- 知识库构建与优化：
  - 抽取整理知识 → `rag/1-get_rag_knowledges.py`
  - 知识聚类分析 → `rag/2-jsonknowledges_kmeans.py`
  - json格式转换工具 → `rag/3-json2txt.py`

### 3. 训练自己的模型（Finetune工具系列）

#### 数据制作工具 (data_maker/)
- 制作祝福语数据：
  - v1版本数据生成 → `get_wish_datav1.py`
  - v2版本增强版本 → `get_wish_datav2.py`
- 合并多个数据集 → `merge_data_json.py`

#### 多媒体数据处理 (everything2data/)
- 视频数据处理：
  - B站视频下载 → `bilibili2download/`
  - 视频转文本 → `video2json/`
- 图像处理：
  - 图片OCR → `jpg2txt.py`
- 通用文本转换：
  - 各类格式转txt → `everything2txt/`

#### 数据清洗与分析 (datajson_refiner/)
- 数据清洗：去重、格式化、质量过滤
- 数据分析：统计特征、质量评估
- 数据修改：批量更新、格式转换

### 4. 常见任务流程示例

#### 构建知识库完整流程
1. 获取原始数据：
   ```bash
   # 抓取网页内容
   node tools/rag/url2article.md
   ```

2. 数据预处理：
   ```bash
   # 分块处理
   node tools/rag/article2chunk.js
   
   # 质量过滤
   python tools/rag/0-data_llm_filter.py
   ```

3. 构建知识库：
   ```bash
   # 数据过滤
   python tools/rag/0-data_llm_filter.py
   
   # 知识抽取
   python tools/rag/1-get_rag_knowledges.py
   
   # 知识聚类
   python tools/rag/2-jsonknowledges_kmeans.pyx

   # json格式转换
   python tools/rag/3-json2txt.py
   ```

#### 模型训练数据准备流程
1. 收集原始数据：
   ```python
   # 下载B站视频转文字
   python tools/finetune/everything2data/bilibili2download/download.py
   
   python tools/finetune/everything2data/video2json/video2text.py 
   ```

2. 数据清洗：
   ```python
   # 数据清洗
   python tools/finetune/datajson_refiner/clean.py
   
   # 合并数据集
   python tools/finetune/data_maker/merge_data_json.py
   ```


以上是天机项目中 `tools` 目录下的各种开发工具，欢迎贡献更多实用工具来改进天机项目！ 