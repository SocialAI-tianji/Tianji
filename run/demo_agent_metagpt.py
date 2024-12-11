from dotenv import load_dotenv
load_dotenv()

import asyncio
import streamlit as st
import uuid
from streamlit_chat import message
from metagpt.logs import logger
import os

import sys
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #当前文件夹路径
sys.path.insert(0, module_dir)

from tianji.agents.metagpt_agents.intentRecognition import IntentReg
from tianji.agents.metagpt_agents.answerBot import AnswerBot
from tianji.agents.metagpt_agents.sceneRefinement import SceneRefine
from tianji.agents.metagpt_agents.searcher import Searcher
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.helper_func import has_empty_values, is_number_in_types, timestamp_str, extract_single_type_attributes_and_examples, load_json, extract_all_types
from tianji.agents.metagpt_agents.utils.agent_llm import OpenaiApi as LLMApi
import time

# 初始化session_state变量
if "user_id" not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    logger.log(0, "add uuid")
    st.session_state["user_id"] = str(uuid.uuid4())

def on_btn_click(sharedData):
    sharedData.message_list_for_agent.clear()
    sharedData.chat_history.clear()
    sharedData.scene_label = ""
    sharedData.scene_attribute = {}
    sharedData.extra_query.clear()
    sharedData.search_results = {}
    st.session_state["generated"].clear()
    st.session_state["past"].clear()
    st.session_state["scene_label"] = ""
    st.session_state["scene_attr"] = {}


def flip():
    if st.session_state["check"]:
        st.session_state["enable_se"] = True
    else:
        st.session_state["enable_se"] = False


def initialize_sidebar(scenes, sharedData):
    with st.sidebar:
        st.markdown("我是由人情世故大模型团队开发的多智能体应用，专注于理解您的意图并进一步提问，以提供精准答案。目前，我支持以下场景：")
        container_all_scenes = st.container(border=True)
        for item in scenes:
            container_all_scenes.write(item)
        st.markdown("用户当前意图：")
        container_current_scene = st.container(border=True)
        container_current_scene.write(st.session_state["scene_label"])
        st.markdown("当前场景要素：")
        container_scene_attribute = st.container(border=True)
        container_scene_attribute.write(st.session_state["scene_attr"])
        st.button("Clear Chat History", on_click=lambda: on_btn_click(sharedData))
        st.checkbox(
            "启用网络搜索（确保填写密钥）", value=st.session_state["enable_se"], key="check", on_change=flip
        )


async def main():
    role_intentReg = IntentReg()
    role_sceneRefine = SceneRefine()
    role_answerBot = AnswerBot()
    role_search = Searcher()

    st.write(f"您的会话ID是: {st.session_state['user_id']}")
    st.title("人情世故大模型")
    json_data = load_json("scene_attribute.json")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "enable_se" not in st.session_state:
        st.session_state["enable_se"] = False
    if "scene_label" not in st.session_state:
        st.session_state["scene_label"] = ""
    if "scene_attr" not in st.session_state:
        st.session_state["scene_attr"] = {}

    sharedData = SharedDataSingleton.get_instance()
    initialize_sidebar(extract_all_types(json_data), sharedData)

    # 显示历史对话记录
    for first_status_message in sharedData.chat_history:
        message(
            first_status_message["message"],
            is_user=first_status_message["is_user"],
            key=first_status_message["keyname"],
        )

    if user_input := st.chat_input():
        st.session_state["past"].append(user_input)
        message(st.session_state["past"][-1], is_user=True, key="_user")

        sharedData.message_list_for_agent.append({"user": st.session_state["past"][-1]})

        sharedData.chat_history.append(
            {
                "message": st.session_state["past"][-1],
                "is_user": True,
                "keyname": "user" + str(timestamp_str()),
            }
        )

        # 运行意图识别 agent
        intent_ans = (
            await role_intentReg.run(str(sharedData.message_list_for_agent))
        ).content

        # 目前不支持的场景
        if intent_ans == "None":
            st.warning("此模型只支持回答关于人情世故的事项，已调用 API 为你进行单轮回答。")
            rsp = await LLMApi()._aask(prompt=user_input)
            sharedData.message_list_for_agent.clear()
            st.session_state["generated"].append(rsp)
            sharedData.chat_history.append(
                {
                    "message": st.session_state["generated"][-1],
                    "is_user": False,
                    "keyname": "assistant" + str(timestamp_str()),
                }
            )
            message(st.session_state["generated"][-1], is_user=False)

        # 模型返回未知的场景标签
        elif not is_number_in_types(json_data, int(intent_ans)):
            st.warning("模型发生幻觉，请重新提问")
            sharedData.message_list_for_agent.clear()
            time.sleep(3)

        else:
            # 确认用户意图后：
            if not sharedData.scene_label or sharedData.scene_label != intent_ans:
                sharedData.scene_label = intent_ans
                st.session_state["scene_label"] = sharedData.scene_label
                # 提取对应场景所需要的场景要素
                _, scene_attributes, _ = extract_single_type_attributes_and_examples(
                    json_data, sharedData.scene_label
                )
                sharedData.scene_attribute = {attr: "" for attr in scene_attributes}

            sharedData.scene_label = intent_ans
            st.session_state["scene_label"] = sharedData.scene_label

            # 运行场景细化 agent
            refine_ans = (
                await role_sceneRefine.run(str(sharedData.message_list_for_agent))
            ).content

            st.session_state["scene_attr"] = sharedData.scene_attribute
            # 用户提供的场景要素不全，场景细化 agent 进行提问
            if refine_ans != "":
                st.session_state["generated"].append(refine_ans)
                sharedData.message_list_for_agent.append(
                    {"assistant": st.session_state["generated"][-1]}
                )
                sharedData.chat_history.append(
                    {
                        "message": st.session_state["generated"][-1],
                        "is_user": False,
                        "keyname": "assistant" + str(timestamp_str()),
                    }
                )
                message(st.session_state["generated"][-1], is_user=False)

            # 用户提供的场景要素齐全，运行回答助手 agent
            if not has_empty_values(sharedData.scene_attribute):
                final_ans = (
                    await role_answerBot.run(str(sharedData.message_list_for_agent))
                ).content
                st.session_state["generated"].append(final_ans)
                sharedData.chat_history.append(
                    {
                        "message": st.session_state["generated"][-1],
                        "is_user": False,
                        "keyname": "assistant" + str(timestamp_str()),
                    }
                )
                message(st.session_state["generated"][-1], is_user=False)

                # 如果开启已网络搜索助手 agent ，运行 agent
                if st.session_state["enable_se"] is True:
                    with st.spinner("启用搜索引擎，请稍等片刻... 如有报错，请检查密钥是否填写正确"):
                        await role_search.run(str(sharedData.message_list_for_agent))

                    sa_res1 = "生成的额外查询：" + str(sharedData.extra_query)
                    st.session_state["generated"].append(sa_res1)
                    sharedData.chat_history.append(
                        {
                            "message": st.session_state["generated"][-1],
                            "is_user": False,
                            "keyname": "assistant" + str(timestamp_str()),
                        }
                    )
                    message(st.session_state["generated"][-1], is_user=False)
                    time.sleep(0.01)

                    # 显示网页网址
                    urls = []
                    for item in sharedData.search_results.values():
                        if "url" in item:
                            urls.append(item["url"])
                    urls = " ".join(urls)
                    sa_res2 = "搜索引擎返回的网页为：\n" + urls
                    st.session_state["generated"].append(sa_res2)
                    sharedData.chat_history.append(
                        {
                            "message": st.session_state["generated"][-1],
                            "is_user": False,
                            "keyname": "assistant" + str(timestamp_str()),
                        }
                    )
                    message(st.session_state["generated"][-1], is_user=False)
                    time.sleep(0.01)

                    sa_res3 = "判断需要进一步查询的网页为" + str(sharedData.filter_weblist)
                    st.session_state["generated"].append(sa_res3)
                    sharedData.chat_history.append(
                        {
                            "message": st.session_state["generated"][-1],
                            "is_user": False,
                            "keyname": "assistant" + str(timestamp_str()),
                        }
                    )
                    message(st.session_state["generated"][-1], is_user=False)
                    time.sleep(0.01)

                    # 以网络搜索助手 agent 的结果为基础，再次运行回答助手 agent
                    final_ans_sa = (
                        await role_answerBot.run(str(sharedData.message_list_for_agent))
                    ).content
                    final_ans_sa = "基于搜素引擎的回答：" + final_ans_sa
                    st.session_state["generated"].append(final_ans_sa)
                    sharedData.chat_history.append(
                        {
                            "message": st.session_state["generated"][-1],
                            "is_user": False,
                            "keyname": "assistant" + str(timestamp_str()),
                        }
                    )
                    message(st.session_state["generated"][-1], is_user=False)

                # 回答完成，清除所有 agent 环境中的数据。
                sharedData.message_list_for_agent.clear()
                sharedData.scene_label = ""
                sharedData.scene_attribute = {}
                sharedData.extra_query.clear()
                sharedData.search_results = {}

        st.rerun()


asyncio.run(main())
