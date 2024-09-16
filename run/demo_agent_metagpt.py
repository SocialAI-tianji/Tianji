from dotenv import load_dotenv

load_dotenv()

import asyncio
import streamlit as st
import uuid
from streamlit_chat import message

from metagpt.logs import logger

from tianji.agents.metagpt_agents.intentRecognition import IntentReg
from tianji.agents.metagpt_agents.answerBot import AnswerBot
from tianji.agents.metagpt_agents.sceneRefinement import sceneRefine
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.common import timestamp_str
from tianji.utils.helper_for_agent import *
from tianji.utils.common_llm_api import LLMApi
import time

# 初始化session_state变量
if "user_id" not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    logger.log(0, "add uuid")
    st.session_state["user_id"] = str(uuid.uuid4())

def on_btn_click(sharedData):
    sharedData.message_list_for_agent.clear()
    sharedData.first_status_message_list.clear()
    sharedData.scene_label=""
    sharedData.scene_attribute={}
    st.session_state["generated"].clear()
    st.session_state["past"].clear()


def initialize_sidebar(scenes,sharedData):
    with st.sidebar:
        st.markdown("我是由人情世故大模型团队开发的多智能体应用，专注于理解您的意图并进一步提问，以提供精准答案。目前，我支持以下场景：")
        container_all_scenes = st.container(border=True)
        for item in scenes:
            container_all_scenes.write(item)
        st.markdown("用户当前意图：")
        container_current_scene=st.container(border=True)
        container_current_scene.write(sharedData.scene_label)
        st.markdown("当前场景要素：")
        container_scene_attribute=st.container(border=True)
        container_scene_attribute.write(sharedData.scene_attribute)
        st.button("Clear Chat History", on_click=lambda: on_btn_click(sharedData))

async def main():

    role_intentReg=IntentReg()
    role_sceneRefine=sceneRefine()
    role_answerBot=AnswerBot()

    st.write(f"您的会话ID是: {st.session_state['user_id']}")
    st.title("人情世故大模型")
    json_data=load_json("scene_attribute.json")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    
    sharedData = SharedDataSingleton.get_instance()
    initialize_sidebar(extract_all_types(json_data),sharedData)
    for first_status_message in sharedData.first_status_message_list:
        message(
            first_status_message["message"],
            is_user=first_status_message["is_user"],
            key=first_status_message["keyname"],
        )

    if user_input := st.chat_input():
        st.session_state["past"].append(user_input)
        message(st.session_state["past"][-1], is_user=True, key="_user")

        sharedData.message_list_for_agent.append(
                    {
                        "user": st.session_state["past"][-1]              
                    }
                )
        
        sharedData.first_status_message_list.append(
            {
                "message": st.session_state["past"][-1],
                "is_user": True,
                "keyname": "user" + str(timestamp_str()),
            })
        
        intent_ans= (await role_intentReg.run(str(sharedData.message_list_for_agent))).content

        if intent_ans == "None":
            st.warning("此模型只支持回答关于人情世故的事项，已调用 API 为你进行单轮回答。")
            rsp = await LLMApi()._aask(prompt=user_input, temperature=1.00)
            sharedData.message_list_for_agent.clear()
            st.session_state["generated"].append(rsp)
            sharedData.first_status_message_list.append(
                {
                    "message": st.session_state["generated"][-1],
                    "is_user": False,
                    "keyname": "assistant" + str(timestamp_str()),
                })
            message(st.session_state["generated"][-1], is_user=False)

        elif not is_number_in_types(json_data,int(intent_ans)):
            st.warning("模型发生幻觉，请重新提问")
            sharedData.message_list_for_agent.clear()
            
        else:
            if not sharedData.scene_label or sharedData.scene_label!=intent_ans:
                _,scene_attributes,_ = extract_single_type_attributes_and_examples(json_data,intent_ans)
                sharedData.scene_attribute = {attr: "" for attr in scene_attributes}

            sharedData.scene_label=intent_ans 

            refine_ans= (await role_sceneRefine.run(str(sharedData.message_list_for_agent))).content

            if refine_ans!="":
                st.session_state["generated"].append(refine_ans)
                sharedData.message_list_for_agent.append(
                                {
                                    "assistant": st.session_state["generated"][-1]              
                                }
                            )
                sharedData.first_status_message_list.append(
                {
                    "message": st.session_state["generated"][-1],
                    "is_user": False,
                    "keyname": "assistant" + str(timestamp_str()),
                })
                message(st.session_state["generated"][-1], is_user=False)

            if not has_empty_values(sharedData.scene_attribute):
                final_ans = (await role_answerBot.run(str(sharedData.message_list_for_agent))).content
                st.session_state["generated"].append(final_ans)
                sharedData.first_status_message_list.append(
                {
                    "message": st.session_state["generated"][-1],
                    "is_user": False,
                    "keyname": "assistant" + str(timestamp_str()),
                })
                message(st.session_state["generated"][-1], is_user=False)
                sharedData.message_list_for_agent.clear()
                sharedData.scene_label=""
        st.rerun()
asyncio.run(main())
