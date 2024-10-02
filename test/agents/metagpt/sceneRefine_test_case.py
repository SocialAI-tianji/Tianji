from dotenv import load_dotenv

load_dotenv()

import asyncio
import streamlit as st
import uuid
from tianji.agents.metagpt_agents.sceneRefinement import SceneRefine
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.helper_func import *

# 给出针对回答的知识 并用md展示
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
async def async_func(role, user_input):
    result = await role.run(user_input)
    return result.content


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


def on_btn_click(sharedData):
    sharedData.message_list_for_agent.clear()
    sharedData.chat_history.clear()
    sharedData.scene_label = ""
    sharedData.scene_attribute = {}
    st.session_state["scene_label"] = ""
    st.session_state["scene_attr"] = {}


def initialize_sidebar(scenes, sharedData):
    with st.sidebar:
        st.markdown("场景细化助手单元测试，请先选择用户意图（用数字表示），以模拟意图识别 agent 的返回值")
        container_all_scenes = st.container(border=True)
        for item in scenes:
            container_all_scenes.write(item)
        st.markdown("用户当前意图：")
        st.session_state["mock_intentReg_ans"] = str(
            st.number_input("Integer", 1, 7, "min", 1)
        )
        # st.session_state["scene_label"] = sharedData.scene_label
        container_current_scene = st.container(border=True)
        container_current_scene.write(st.session_state["mock_intentReg_ans"])
        st.markdown("当前场景要素：")
        container_scene_attribute = st.container(border=True)
        container_scene_attribute.write(st.session_state["scene_attr"])
        st.button("Clear Chat History", on_click=lambda: on_btn_click(sharedData))


# 创建一个标题和一个副标题
st.title("💬 人情世故-场景细化助手")
st.caption("🚀 识别用户场景里的场景细化要素以及进行提问")
status_step = 1

role_sceneRefine = SceneRefine()
json_data = load_json("scene_attribute.json")

if "scene_label" not in st.session_state:
    st.session_state["scene_label"] = ""
if "scene_attr" not in st.session_state:
    st.session_state["scene_attr"] = {}
if "mock_intentReg_ans" not in st.session_state:
    st.session_state["mock_intentReg_ans"] = ""

sharedData = SharedDataSingleton.get_instance()
initialize_sidebar(extract_all_types(json_data), sharedData)

show_history_st_messages()

# 在Streamlit代码中调用异步函数
if prompt := st.chat_input():
    # 显示历史消息--优化前端效果
    show_one_message(role="user", method="write", showdata="用户问题：", is_add=True)
    show_one_message(role="user", method="write", showdata=prompt, is_add=True)

    sharedData.message_list_for_agent.append({"user": prompt})

    if (
        not sharedData.scene_label
        or sharedData.scene_label != st.session_state["mock_intentReg_ans"]
    ):
        sharedData.scene_label = st.session_state["mock_intentReg_ans"]
        _, scene_attributes, _ = extract_single_type_attributes_and_examples(
            json_data, sharedData.scene_label
        )
        sharedData.scene_attribute = {attr: "" for attr in scene_attributes}

    st.chat_message("assistant").write("正在处理，请稍候...")
    refine_ans = run_async_code(
        async_func,
        role=role_sceneRefine,
        user_input=str((sharedData.message_list_for_agent)),
    )
    st.session_state["scene_attr"] = sharedData.scene_attribute

    if refine_ans != "":
        sharedData.message_list_for_agent.append({"assistant": refine_ans})
        show_one_message(
            role="assistant", method="write", showdata="agent 场景细化助手回答：", is_add=True
        )
        show_one_message(
            role="assistant", method="write", showdata=str(refine_ans), is_add=True
        )
