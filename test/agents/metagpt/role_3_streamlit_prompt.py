from dotenv import load_dotenv

load_dotenv()

import asyncio
import json
from typing import Optional, Any

from metagpt.actions import Action
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from metagpt.logs import logger

from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.knowledge_tool import (
    get_docs_list_query_openai,
    get_docs_list_query_zhipuai,
)
from tianji.utils.common_llm_api import LLMApi
from tianji.agents.metagpt_agents.ruyi import RuYi
from tianji.agents.metagpt_agents.qianbianzhe import QianBianZhe
from tianji.agents.metagpt_agents.wendao import WenDao

KNOWLEDGE_PATH = r"/Users/fengzetao/Workspace/Github/SocialAI/Tianji/tianji/knowledges/04-Wishes/knowledges.txt"
SAVE_PATH = r"/Users/fengzetao/Workspace/Github/SocialAI/Tianji/temp"


# 给出针对回答的知识 并用md展示
class WriteMarkDown(Action):
    # 这是对json中每个key的解释：
    # 语言场景（scene），目前的聊天场合，比如工作聚会。
    # 节日（festival），对话目前背景所在的节日，比如生日。
    # 聊天对象角色（role），目前谈话的对象，主要是第三人称。例如和爸爸聊天对象就是爸爸。
    # 聊天对象年龄段（age），和role相关，就是聊天对象的年龄段，例如中老年。
    # 聊天对象职业（career）， 和role相关，就是聊天对象的职业，例如教师。
    # 聊天对象状态（state），和role相关，就是聊天对象的健康状态，例如身体健康。
    # 聊天对象性格（character），和role相关，就是聊天对象的性格特点，例如开朗健谈。
    # 时间（time），和role相关，就是聊天对话时间段，如傍晚。
    # 聊天对象爱好（hobby），和role相关，就是聊天对象的兴趣爱好，例如下象棋。
    # 聊天对象愿望（wish），和role相关，就是聊天对象目前的愿望是什么，例如果希望家庭成员平安。

    name: str = "WriteMarkDown"

    knowledge: str = ""
    json_from_data: Optional[dict] = SharedDataSingleton.get_instance().json_from_data

    async def run(self, instruction: str):
        json_from_data: Optional[
            dict
        ] = SharedDataSingleton.get_instance().json_from_data
        knowledge_key = json_from_data["festival"] + json_from_data["requirement"]
        knowledge = get_docs_list_query_zhipuai(
            query_str=knowledge_key,
            loader_file_path=KNOWLEDGE_PATH,
            persist_directory=SAVE_PATH,
            k_num=5,
        )
        print("knowledge:\n", knowledge)
        PROMPT_TEMPLATE: str = f"""
            你是一个{json_from_data["festival"]}的祝福大师。
            你需要写一段关于如何写{json_from_data["festival"]}{json_from_data["requirement"]}的思路总结。目前了解到这段{json_from_data["festival"]}{json_from_data["requirement"]}是在{json_from_data["scene"]}送给{json_from_data["role"]}的。
            你写的总结需要考虑如何认同{json_from_data["role"]}的愿望：{json_from_data["wish"]}。
            你需要考虑如何对{json_from_data["role"]}写符合{json_from_data["scene"]}的语言场景的祝福。
            你需要考虑如何对{json_from_data["role"]}写符合{json_from_data["festival"]}的节日氛围的祝福。
            你还可以根据{json_from_data["role"]}的年龄段：{json_from_data["age"]}，职业：{json_from_data["career"]}，状态：{json_from_data["state"]}，性格：{json_from_data["character"]}，当前的时间段：{json_from_data["time"]}，爱好：{json_from_data["hobby"]}作为素材，告诉我怎么用到祝福里。

            你还可以以{knowledge}为参考。

            经过思考后，告诉我怎么完成{json_from_data["festival"]}{json_from_data["requirement"]}，并整理成md结构的文档。

            """
        prompt = PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await LLMApi()._aask(prompt)
        rsp = rsp.replace("```markdown", "").replace("```", "")
        logger.info("回复生成：\n" + rsp)

        return rsp


# 如何写 如意如意如我心意
class RuYi(Role):
    name: str = "RuYi"
    profile: str = "Stylize"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([WriteMarkDown])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)

        return msg


# 新增代码，便于区分

# 新增代码，便于区分----->Start
import streamlit as st
import uuid


# 定义一个执行异步代码的函数
def run_async_code(async_function, *args, **kwargs):
    # 创建一个新的事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # 运行异步任务直到完成，并返回结果
        return loop.run_until_complete(async_function(*args, **kwargs))
    finally:
        # 关闭事件循环
        loop.close()


# 定义一个异步函数
async def run_async_model(user_input):
    role_wendao = WenDao()
    result = await role_wendao.run(user_input)
    return result.content


async def run_async_qianbianzhe(user_input):
    role_qianbianzhe = QianBianZhe()
    result = await role_qianbianzhe.run(user_input)
    return result.content


async def run_async_ruyi(user_input):
    role_ruyi = RuYi()
    result = await role_ruyi.run(user_input)
    return result.content


def json_to_special_str(data):
    result = ""
    for key, value in data.items():
        if value == "":
            value = "无"
        result += f"{key} - {value}<br/>"
    return result


def show_history_st_messages():
    sharedData = SharedDataSingleton.get_instance()
    for one_message in sharedData.chat_history:
        if one_message["method"] == "json":
            st.chat_message(one_message["role"]).json(one_message["showdata"])
        if one_message["method"] == "write":
            st.chat_message(one_message["role"]).write(one_message["showdata"])


def show_one_message(role, method="write", showdata="", is_add=False):
    sharedData = SharedDataSingleton.get_instance()
    if method == "json":
        st.chat_message(role).json(showdata)
    if method == "write":
        st.chat_message(role).write(showdata)
    if is_add is True:
        sharedData.chat_history.append(
            {"role": role, "method": method, "showdata": showdata}
        )


# 初始化session_state变量
if "user_id" not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    st.session_state["user_id"] = str(uuid.uuid4())
    st.write(f"您的会话ID是: {st.session_state['user_id']}")


# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    markdown_con = """
    ## 友情提示
    这是为了优化人情世故大模型--如意角色(Ruyi)功能，思考祝福语的生成策略和评价。
    参考案例：
    ```json
    {
        "requirement": "给爷爷送祝福",
        "scene": "家庭庆祝生日",
        "festival": "中秋节",
        "role": "爷爷",
        "age": "老年",
        "career": "钓鱼爱好者",
        "state": "最近身体状态不好",
        "character": "经验丰富",
        "time": "晚上",
        "hobby": "钓鱼",
        "wish": "希望我能学会欣赏艺术的美",
        "style": "老年人版"
    }
    ```
    """
    st.markdown(markdown_con)
    "这是为了优化人情世故大模型--如意角色(Ruyi)功能。"
    # 创建一个滑块，用于选择最大长度，范围在0到1024之间，默认值为512
    # max_length = st.slider("max_length", 0, 1024, 512, step=1)
    # templature = st.slider("templature", 0, 1024, 512, step=3)
    if st.button("清除历史"):
        st.session_state.messages = []
        # 获取新的需求收集对象
        status_step = 0
        shareData = SharedDataSingleton.get_instance()
        shareData._instance = None
        shareData.json_from_data = None  # 这是要共享的变量
        shareData.first_status_user_history = ""
        shareData.first_status_message_list = []
        shareData.chat_history = []
# 创建一个标题和一个副标题
st.title("💬 人情世故-如意")
st.caption("🚀 优化 思考祝福语的生成策略和评价 的模块")
st.chat_message("assistant").write("你需要直接将生成的祝福语或者案例祝福语给我，我帮你进行深度分析。")
status_step = 1

# 在Streamlit代码中调用异步函数
if prompt := st.chat_input():
    # 显示历史消息--优化前端效果
    show_history_st_messages()

    sharedData = SharedDataSingleton.get_instance()
    json_prompt = json.loads(prompt)

    show_one_message(role="user", method="write", showdata="JSON格式化内容如下：", is_add=True)
    show_one_message(role="user", method="json", showdata=json_prompt, is_add=True)

    sharedData.json_from_data = json_prompt
    json_from_data = sharedData.json_from_data

    st.chat_message("assistant").write("正在处理，请稍候...")
    ruyi_ans = run_async_code(run_async_ruyi, " ")
    st.chat_message("assistant").write("agent 如意回答：" + str(ruyi_ans))
