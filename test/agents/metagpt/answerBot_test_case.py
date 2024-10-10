from dotenv import load_dotenv

load_dotenv()

import asyncio
import streamlit as st
import uuid
from tianji.agents.metagpt_agents.answerBot import AnswerBot
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.helper_func import *
import copy
import streamlit as st
import uuid

st.set_page_config(layout="wide")


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
    st.session_state["input_texts"].clear()
    st.session_state["selected_options_list"].clear()
    st.session_state["form_count"] = 0
    st.session_state["form_submitted"] = {}
    st.session_state["deleted_forms"].clear()


def initialize_sidebar(scenes, sharedData):
    with st.sidebar:
        st.markdown("回答助手单元测试，请先选择用户意图（用数字表示），以模拟意图识别 agent 的返回值")
        container_all_scenes = st.container(border=True)
        for item in scenes:
            container_all_scenes.write(item)
        st.markdown("用户当前意图：")
        st.session_state["mock_intentReg_ans"] = str(
            st.number_input("Integer", 1, 7, "min", 1)
        )
        container_current_scene = st.container(border=True)
        container_current_scene.write(st.session_state["mock_intentReg_ans"])
        st.button("Clear Chat History", on_click=lambda: on_btn_click(sharedData))


def get_answerBot_ans(sharedData):
    for item_1, item_2 in zip(
        st.session_state["input_texts"], st.session_state["selected_options_list"]
    ):
        _, value_1 = next(iter(item_1.items()))
        _, value_2 = next(iter(item_2.items()))
        sharedData.message_list_for_agent.append({value_2[0]: value_1})

    sharedData.scene_attribute = copy.deepcopy(st.session_state["scene_attr"])
    final_ans = run_async_code(
        async_func,
        role=role_answerBot,
        user_input=str((sharedData.message_list_for_agent)),
    )
    sharedData.chat_history.append(
        {"role": "assistant", "method": "write", "showdata": final_ans}
    )
    sharedData.message_list_for_agent.clear()


def disable():
    st.session_state.disabled = True


# 创建一个标题和一个副标题
st.title("💬 人情世故-回答助手")
st.caption("🚀 根据用户意图以及场景细化要素回答问题的模块")
status_step = 1

role_answerBot = AnswerBot()
json_data = load_json("scene_attribute.json")

if "scene_label" not in st.session_state:
    st.session_state["scene_label"] = ""
if "scene_attr" not in st.session_state:
    st.session_state["scene_attr"] = {}
if "mock_intentReg_ans" not in st.session_state:
    st.session_state["mock_intentReg_ans"] = ""
if "input_texts" not in st.session_state:
    st.session_state["input_texts"] = []
if "selected_options_list" not in st.session_state:
    st.session_state["selected_options_list"] = []
if "form_count" not in st.session_state:
    st.session_state["form_count"] = 0
if "form_submitted" not in st.session_state:
    st.session_state["form_submitted"] = {}
if "deleted_forms" not in st.session_state:
    st.session_state["deleted_forms"] = []

sharedData = SharedDataSingleton.get_instance()
initialize_sidebar(extract_all_types(json_data), sharedData)

with st.container(height=560):
    heading_col1, heading_col2 = st.columns(2, vertical_alignment="top")
    with heading_col1:
        st.caption(" 模拟用户以与大模型的对话，以模拟场景细化助手的返回值（可选）。")
    with heading_col2:
        st.caption(" 模拟场景细化助手提取到的细化要素（必须）。")
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        if st.button("生成输入框和多选框"):
            st.session_state.form_count += 1
        with st.container(height=430, border=True):
            for i in range(st.session_state["form_count"]):
                form_key = f"form_{i}"
                if form_key in st.session_state["deleted_forms"]:
                    continue
                with st.form(
                    key=form_key, enter_to_submit=False, clear_on_submit=False
                ):
                    col_in1, col_in2 = st.columns([7, 3])
                    with col_in1:
                        input_text = st.text_input(
                            f"输入文本 {i + 1}", key=f"input_text_{i}"
                        )

                    with col_in2:
                        options = ["user", "assitant"]
                        selected_options = st.multiselect(
                            f"选择选项 {i + 1}",
                            options,
                            key=f"multiselect_{i}",
                            max_selections=1,
                            default=["user"],
                        )

                    submitted = st.form_submit_button(
                        "提交",
                        disabled=st.session_state["form_submitted"].get(
                            form_key, False
                        ),
                    )

                    if submitted:
                        st.session_state["input_texts"].append({form_key: input_text})
                        st.session_state["selected_options_list"].append(
                            {form_key: selected_options}
                        )
                        st.session_state["form_submitted"][form_key] = True
                        st.rerun()

                delete_button = st.button(f"删除表单 {i + 1}", key=f"delete_button_{i}")

                if delete_button:
                    st.session_state["deleted_forms"].append(form_key)
                    st.session_state["input_texts"] = [
                        entry
                        for entry in st.session_state["input_texts"]
                        if form_key not in entry
                    ]
                    st.session_state["selected_options_list"] = [
                        entry
                        for entry in st.session_state["selected_options_list"]
                        if form_key not in entry
                    ]
                    if form_key in st.session_state["form_submitted"]:
                        del st.session_state["form_submitted"][form_key]
                    st.rerun()

    with col2:
        with st.container(height=430, border=True):
            sharedData.scene_label = st.session_state["mock_intentReg_ans"]
            _, scene_attributes, _ = extract_single_type_attributes_and_examples(
                json_data, sharedData.scene_label
            )
            sharedData.scene_attribute = {attr: "" for attr in scene_attributes}
            st.session_state["scene_attr"] = copy.deepcopy(sharedData.scene_attribute)

            for key in st.session_state["scene_attr"].keys():
                st.session_state["scene_attr"][key] = st.text_input(
                    f"Enter value for {key}",
                    key=f"text_input_{key}",
                    value=st.session_state["scene_attr"].get(key, ""),
                )

with st.container(height=450):
    all_filled = all(value.strip() for value in st.session_state["scene_attr"].values())
    submit_button = st.button(
        "触发 answerBot Agent",
        disabled=not all_filled,
        on_click=lambda: get_answerBot_ans(sharedData),
    )
    with st.container(height=350):
        show_history_st_messages()
