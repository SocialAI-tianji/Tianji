# 如何复刻天机项目

本教程将指导你如何参考天机项目的架构，创建属于自己的垂直领域AI应用。我们将从Prompt工程、RAG知识库和Agent开发三个方面详细说明。

## 整体规划

在开始之前，你需要：

1. 确定目标领域（例如：租房助手、育儿顾问等）
2. 规划技术路线（Prompt/RAG/Agent/微调）
3. 设计系统架构
4. 准备数据收集计划

## 一、基于Prompt的应用开发

### 1. 提示词模板设计

你可以参考 `tools/prompt_maker` 目录下的工具，进行提示词模板的设计：

- 使用 `prompt_to_json.py` 编写和验证提示词模板
- 使用 `prompt_to_json_in_bulk.py` 批量处理多个提示词
- 使用 `check_prompt_template_in_bulk.py` 检查提示词质量
- 使用 `web_demo.py` 测试提示词效果

### 2. 提示词验证与优化
1. 使用上述工具进行提示词验证
2. 进行多轮测试和优化
3. 整理提示词模板库

### 3. 应用封装
1. 参考 `tianji/prompt` 目录结构
2. 实现提示词管理系统
3. 开发Web界面（参考 `run/tianji_prompt_webui.py`）

## 二、构建RAG知识库应用

### 1. 数据收集
1. 确定知识来源（网页、文档、专业书籍等）
2. 使用 `tools/rag` 工具进行数据抓取：
   - 使用 `url2article.md` 抓取网页内容
   - 使用 `article2chunk.js` 处理长文本分块
3. 进行初步数据清洗

### 2. 知识库构建
1. 使用 `tools/rag` 工具进行数据过滤：
   - 使用 `0-data_llm_filter.py` 过滤低质量数据
   - 使用 `0-data_llm_filter_negative.py` 过滤负面样本
   - 使用 `0-data_llm_filter_lesswords.py` 过滤过短文本
2. 使用 `1-get_rag_knowledges.py` 抽取整理知识
3. 使用 `2-jsonknowledges_kmeans.py` 进行知识聚类分析
4. 使用 `3-json2txt.py` 进行格式转换

### 3. 应用开发
1. 参考 `tianji/knowledges` 目录结构
2. 实现问答系统
3. 优化答案生成质量

## 三、开发Agent应用

### 1. 角色设计
1. 定义Agent的职责和能力
2. 设计交互流程，可参考以下角色：
   - IntentReg: 意图识别
   - SceneRefine: 场景细化
   - AnswerBot: 回答生成
   - Searcher: 信息搜索
3. 规划工具使用，可参考

### 2. 实现核心功能
1. 参考 `tianji/agents` 目录结构
2. 可参考实现以下组件：
   - 意图识别（参考 `test/agents/metagpt/intentReg_test_case.py`）
   - 场景细化（参考 `test/agents/metagpt/sceneRefine_test_case.py`）
   - 回答生成（参考 `test/agents/metagpt/answerBot_test_case.py`）
   - 搜索功能（参考 `test/agents/metagpt/searcher_test_case.py`）

### 3. 应用集成
1. 实现Web界面
2. 添加必要的API
3. 进行功能测试

## 注意事项

1. 使用搜索功能需要配置相应的API密钥：
   - 在 .env 文件中配置 TAVILY_API_KEY
   - 可以从 https://app.tavily.com/ 获取 API key

2. 开发过程中建议参考以下测试用例：
   - `test/agents/metagpt/test_metagpt_dummy.py`: 基本的Action和Role实现示例
   - `test/agents/metagpt/test_WebSearch.py`: 网页搜索示例

3. 系统要求：
   - Python 3.8+
   - MetaGPT框架
   - 必要的API密钥
