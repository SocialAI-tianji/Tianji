# Tianji MetaGPT Agent

Tianji MetaGPT Agent 是一个基于MetaGPT框架的多智能体系统，专注于理解用户意图并提供精准的人情世故相关建议。该系统由多个协同工作的智能体组成，每个智能体都有其特定的职责和功能。

在使用之前，你需要进行初始安装和配置：

```
pip install metagpt==0.8.1
```

并进行配置：

```
metagpt --init-config  # 创建 ~/.metagpt/config2.yaml，此时找到位置，随意修改一个key根据您的需求修改它
# windows 可能创建在类似 C:\Users\用户名\.metagpt\config2.yaml 的地址，请注意运行命令后的终端显示
```
注意，这里metagpt有默认的大模型调用，我们使用的是自定义的调用，所以此处可以随便配置中写一个key（但一定要写 否则会报错！）

当然，你也可以选择在metagpt的配置中写入大模型key，然后体验快速开始：
```
metagpt "创建一个 2048 游戏"  # 这将在 ./workspace 创建一个仓库
```

接下来，我们将介绍 Tianji 中 metagpt 的实现，如何实现一个送祝福智能体的串联。

## 核心智能体

### 1. 意图识别智能体 (IntentReg)

代码位置: tianji/agents/metagpt_agents/intentRecognition/role.py

- **职责**：分析用户输入，识别用户意图并映射到预定义场景
- **主要功能**：
  - 分析用户输入的自然语言文本
  - 识别用户当前的意图和需求
  - 将用户问题匹配到预定义的场景类型
  - 输出场景标签供后续处理

- **可用Actions**：  
```python
  class IntentAnalyze(Action):
      """分析用户意图并映射到预定义场景标签
      使用LLM分析用户输入，返回对应的场景类型编号
      """
      name: str = "IntentAnalyze"
```

- **示例**：

```python
  # Input示例
  user_input = "我想给妈妈过生日，该说些什么祝福语？"
  
  # Output示例（带解释）
  scene_label = "4"  # 4表示"送祝福"场景
  # 解释：系统识别到用户想要进行"祝福"活动，且涉及"生日"和"妈妈"这两个关键要素，
  # 因此将其映射到预定义的"送祝福"场景（编号4）
```

### 2. 场景细化智能体 (SceneRefine)

代码位置：tianji/agents/metagpt_agents/sceneRefinement/role.py

- **职责**：提取和完善场景要素
- **主要功能**：
  - 信息抽取：从用户对话中提取场景要素
  - 提问助手：对缺失的场景要素进行提问
  - 场景要素验证：确保所有必要信息完整
- **可用Actions**：
```python
  class sceneRefineAnalyze(Action):
      """提取场景要素
      从用户输入中提取特定场景所需的关键信息
      """
      name: str = "sceneRefineAnalyze"

  class RaiseQuestion(Action):
      """生成补充问题
      针对缺失的场景要素生成自然的追问
      """
      name: str = "RaiseQuestion"
  ```
- **示例**：
```python
  # Input示例（基于上述意图识别结果）
  scene_label = "4"
  user_input = "我想给妈妈过生日，该说些什么祝福语？"
  
  # Output示例（带解释）
  # 1. 首先通过sceneRefineAnalyze提取已有信息：
  scene_attributes = {
      "节日": "生日",
      "对象角色": "妈妈",
      "对象年龄段": "",  # 未提供
      "语言风格": ""     # 未提供
  }
  
  # 2. 然后通过RaiseQuestion生成追问：
  assistant_response = """我理解您想要给妈妈送上生日祝福。为了让祝福更加贴心，
我想了解一下您期望的表达方式：
1. 您想用什么样的语言风格来表达？比如温馨感人、活泼可爱、正式庄重等
2. 您觉得更适合什么样的表达方式？"""
  # 解释：系统发现缺少"语言风格"这个关键要素，因此生成自然的追问，
  # 并提供具体选项帮助用户更好地表达偏好
  ```

### 3. 回答助手智能体 (AnswerBot)

代码位置：tianji/agents/metagpt_agents/answerBot/role.py

- **职责**：基于场景要素生成定制化回答
- **主要功能**：
  - 整合场景信息和用户需求
  - 生成针对性的建议和解答
  - 提供详细的示例和说明
- **可用Actions**：
  ```python
  class AnswerQuestion(Action):
      """生成定制化回答
      基于完整的场景要素，生成符合用户需求的详细回答
      使用模板系统确保回答的结构性和完整性
      """
      name: str = "AnswerQuestion"
  ```
- **示例**：
```python
  # Input示例
  scene_attributes = {
      "节日": "生日",
      "对象角色": "妈妈",
      "对象年龄段": "中年",
      "语言风格": "温馨感人"
  }
  
  # Output示例（带解释）
  answer = """亲爱的妈妈，生日快乐！
感谢您这些年来的养育之恩，是您的爱让我茁壮成长。
愿您永远健康快乐，我会一直陪伴在您身边。
祝您生日快乐，幸福安康！"""
  # 解释：系统根据场景要素生成了回答：
  # 1. 使用"温馨感人"的语言风格
  # 2. 包含了对母亲养育之恩的感谢
  # 3. 表达了对未来的美好祝愿
  # 4. 整体风格温情脉脉，适合中年妈妈
```

### 4. 搜索助手智能体 (Searcher)

代码位置：tianji/agents/metagpt_agents/searcher/role.py

- **职责**：通过网络搜索补充回答内容
- **主要功能**：
  - 查询扩展：生成相关搜索查询
  - 网络搜索：使用搜索引擎获取相关信息
  - 结果筛选：判断和筛选有价值的网页内容
  - 内容提取：抓取和过滤网页内容
  - 结果整合：将搜索结果整合到回答中
- **可用Actions**：
  ```python
  class QueryExpansion(Action):
      """生成扩展查询
      基于用户输入生成多个相关的搜索查询
      """
      name: str = "queryExpansion"

  class WebSearch(Action):
      """执行网络搜索
      使用搜索引擎获取相关网页内容
      """
      name: str = "WebSearch"

  class SelectResult(Action):
      """筛选搜索结果
      判断哪些搜索结果值得进一步分析
      """
      name: str = "selectResult"

  class SelectFetcher(Action):
      """抓取网页内容
      获取筛选后的网页的具体内容
      """
      name: str = "selectFetcher"

  class FilterSelectedResult(Action):
      """过滤和提取信息
      从网页内容中提取有价值的信息
      """
      name: str = "FilterSelectedResult"
  ```
- **示例**：
  ```python
  # Input示例
  query = "妈妈生日祝福语温馨感人"
  
  # Output示例（带解释）
  # 1. QueryExpansion生成多个相关查询：
  expanded_queries = [
      "母亲生日祝福语大全",
      "感人的生日祝福妈妈",
      "写给妈妈的生日祝福"
  ]
  # 解释：系统基于原始查询，生成多个相关查询以获取更全面的信息。
  
  # 2. WebSearch调用网络搜索API的结果:
  search_results = {
      0: {
          "url": "https://example.com/birthday-wishes",
          "title": "暖心的母亲生日祝福语" #网页标题
          "summ": "暖心的母亲生日祝福语分别为...", #网络搜索api返回的网页内容片段。
      }
  }
  # 解释："summ" 字段通常是网络内容里的前xx个字符，并不会包含整个网页里的内容。

  # 3. SelectResult返回的结果：
  filter_weblist= [0,2,6,8] 
  # 解释：判断需要进一步爬取的网页（以索引形式表示），过滤与当前主题无关的网页。

  # 4. SelectFetcher返回的结果：
  search_results = {
      0: {
          "url": "https://example.com/birthday-wishes",
          "title": "暖心的母亲生日祝福语",
          "summ": "暖心的母亲生日祝福语...",
          "content": "..." #网页内容
      }
  }
  # 解释：调用request模块爬取网页内容，考虑到大模型的token限制，目前只取网页内容里的前1024个字符，赋值到 "content" 字段中。

  # 5. FilterSelectedResult筛选后的结果:
  search_results = {
      0: {
          "url": "https://example.com/birthday-wishes",
          "title": "暖心的母亲生日祝福语",
          "summ": "暖心的母亲生日祝福语...",
          "content": "...",
          "filtered_content"："..." #精选的生日祝福内容
      }
  }
  # 解释：对 "content" 字段里的内容进行提纯以及过滤，筛选出最相关的内容，过滤掉广告和无关信息，赋值到 "filtered_content" 字段中。

  
  ```

## 工作流程

1. **意图识别**：
   - 接收用户输入
   - 分析意图
   - 匹配预定义场景

2. **场景细化**：
   - 提取场景要素
   - 检查信息完整性
   - 必要时向用户提问补充信息

3. **答案生成**：
   - 基于场景要素生成初步回答
   - 如果启用搜索功能：
     - 扩展搜索查询
     - 获取网络资源
     - 筛选相关内容
     - 整合搜索结果
   - 生成最终回答

## 使用示例

```python
from tianji.agents.metagpt_agents.intentRecognition import IntentReg
from tianji.agents.metagpt_agents.answerBot import AnswerBot
from tianji.agents.metagpt_agents.sceneRefinement import SceneRefine
from tianji.agents.metagpt_agents.searcher import Searcher

# 初始化智能体
role_intentReg = IntentReg()
role_sceneRefine = SceneRefine()
role_answerBot = AnswerBot()
role_search = Searcher()

# 使用智能体
intent_ans = await role_intentReg.run(user_input)
refine_ans = await role_sceneRefine.run(user_input)
final_ans = await role_answerBot.run(user_input)
search_results = await role_search.run(user_input)
```

## 支持的场景类型

系统支持多种人情世故相关的场景，包括但不限于：

- 如何说对话
- 化解尴尬场合
- 矛盾与冲突应对
- 送礼礼仪文化
- 送祝福

每个场景都有其特定的属性要素，如：
- 语言场景
- 对象角色
- 对象性格
- 对象情绪
- 时间等

您可以通过以下文件研究 MetaGPT 的实现:

### 基础测试用例

* `test/agents/metagpt/test_metagpt_dummy.py`: 简单的计算器助手示例,展示了基本的 Action 和 Role 实现
* `test/agents/metagpt/test_WebSearch.py`: 基于 Tavily API 的网页搜索示例

### 场景化测试

* `test/agents/metagpt/intentReg_test_case.py`: 意图识别助手的测试用例
* `test/agents/metagpt/sceneRefine_test_case.py`: 场景细化助手的测试用例
* `test/agents/metagpt/answerBot_test_case.py`: 回答助手的测试用例
* `test/agents/metagpt/searcher_test_case.py`: 搜索助手的测试用例

## 配置要求

- Python 3.8+
- MetaGPT框架
- 必要的API密钥（用于LLM和搜索功能）

## 注意事项

1. 使用搜索功能需要配置相应的API密钥:
   - 在 .env 文件中配置 TAVILY_API_KEY
   - 可以从 https://app.tavily.com/ 获取 API key
   - 示例配置:
     ```
     TAVILY_API_KEY=your-tavily-api-key
     ```
   - 搜索功能的使用可以参考 searcher_test_case.py:
     ```python
     # 初始化搜索智能体
     role_searchBot = Searcher()
     
     # 执行搜索
     search_results = await role_searchBot.run(user_input)
     
     # 搜索结果包含:
     # - extra_query: 生成的额外查询
     # - urls: 搜索返回的网页
     # - filter_weblist: 需要进一步查询的网页
     # - filtered_content: 从搜索结果提取的资讯
     ```
2. 场景要素必须完整才能生成最终答案
3. 网络搜索结果会自动过滤无关内容
4. 系统专注于人情世故相关问题的解答


## 扩展指南：自定义Action和Role

在了解了基本的使用方法后,让我们来看看如何扩展系统的功能。通过自定义Action和Role,我们可以根据实际需求构建更加个性化的智能体系统。详细代码可以参考 [test/agents/metagpt/test_metagpt_dummy.py](../../test/agents/metagpt/test_metagpt_dummy.py)

### 1. 自定义Action

首先让我们从最基础的构建块 - Action开始。Action代表了智能体可以执行的具体操作,就像人类的各种技能一样。要创建自己的Action,我们需要继承MetaGPT提供的`Action`基类:

```python
from metagpt.actions import Action

class SimpleCalculator(Action):
    """定义Action的示例"""
    name: str = "SimpleCalculator"  # Action的名称
    
    async def run(self, instruction: str) -> str:
        """实现具体的操作逻辑
        Args:
            instruction: 输入参数
        Returns:
            执行结果
        """
        try:
            num1, num2 = map(int, instruction.split('+'))
            result = f"{num1} + {num2} = {num1 + num2}"
            return result
        except Exception as e:
            return f"计算错误: {str(e)}"
```

### 2. 自定义Role

Role代表一个具有特定功能的智能体。创建自定义Role需要：

1. 继承`Role`基类
2. 设置基本属性
3. 配置Action列表
4. 设置反应模式

```python
from metagpt.roles.role import Role, RoleReactMode

class CalculatorAssistant(Role):
    """定义Role的示例"""
    name: str = "Calculator"  # Role的名称
    profile: str = "一个简单的计算助手"  # Role的描述
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 设置该Role可以使用的Action列表
        self.set_actions([SimpleCalculator])
        # 设置反应模式
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)
```

### 3. 反应模式说明

Role支持三种反应模式：

- **REACT模式**：按照"思考-行动"循环执行 (`_think -> _act -> _think -> _act`)
- **BY_ORDER模式**：按照指定的Action顺序依次执行
- **PLAN_AND_ACT模式**：先思考后执行多个动作 (`_think -> _act -> act -> ...`)

### 4. 使用示例

```python
async def main():
    # 创建Role实例
    calculator = CalculatorAssistant()
    
    # 运行Role并获取结果
    result = await calculator.run("5 + 3")
    print(f"计算结果: {result}")

# 使用asyncio运行
import asyncio
asyncio.run(main())
```

### 5. 注意事项

1. Action的`run`方法必须是异步的（使用`async`定义）
2. Role的反应模式会影响Action的执行顺序和方式
3. 确保正确处理异常情况
4. 建议在Action中添加适当的日志记录
5. Role可以配置多个Action，根据需要选择合适的反应模式

通过这种方式，你可以创建自己的智能体系统，实现特定的功能需求。

