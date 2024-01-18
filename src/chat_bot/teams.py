import os
os.environ["OPENAI_API_KEY"] = "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"  # 填入你自己的OpenAI API key
os.environ["OPENAI_API_MODEL"] = "gpt-3.5-turbo" # 选择你要使用的模型，例如：gpt-4, gpt-3.5-turbo
os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"


# 项目名称：人情世故大模型
# 项目描述：
import streamlit as st
from streamlit_chat import message
import asyncio
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import json
from role_1 import wendao
from role_2 import qianbianzhe
from role_3 import ruyi
from json_from import SharedDataSingleton
from knowledge_tool import getDocumentsListByQuery

# 设计思路 给定人设并导入参考聊天话术、历史聊天语料进行聊天。


# async def start(msg):
#     role_wendao = wendao()
#     logger.info(msg)
#     result = await role_wendao.run(msg) 

#     sharedData  = SharedDataSingleton.get_instance()
#     json_from_data = sharedData.json_from_data
#     knowledge_key= json_from_data["festival"] + json_from_data["requirement"]
#     print("knowledge_key",knowledge_key)
#     knowledge = getDocumentsListByQuery(query_str=knowledge_key)
#     # print("knowledge:",knowledge,json_from_data)
#     role_qianbianzhe = qianbianzhe()
#     qianjibian_ans = await role_qianbianzhe.run(" ")
#     role_ruyi = ruyi()
#     ruyi_ans = await role_ruyi.run(" ")
#     logger.info(result)
#     print("final ans :\n",qianjibian_ans,ruyi_ans)

async def main():
    # 对话导入 
    # msg = "test"
    # msg = """元旦节下午，我和哥哥一起去图书馆学习。我像给哥哥一个祝福。我的哥哥，一位医学院的学生，正在为即将到来的考试做准备。他今年24岁，对医学充满热情。图书馆里非常安静，我们专心致志地学习。哥哥的爱好是玩篮球，他经常说运动是放松大脑的最佳方式。他总是希望我也能热爱学习，努力追求知识。"""
    st.markdown("#### 人情世故大模型_祝福模块")
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    user_input=st.text_input("我是人情世故大模型团队开发的祝福agents。你可以在这里找到一个完整的祝福。我会告诉你怎么写，还会针对你的祝福给你生成专属的知识文档。\n 首先你需要完整的告诉我，你想在什么节日给谁送祝福？这个人是谁呢（是妈妈）？他会有什么愿望呢？你想在什么时候送给他？可以告诉我他的爱好、性格、年龄段、最近的状态。\n 就像这段：【元旦节下午，我和哥哥一起去图书馆学习。我想给哥哥一个祝福。我的哥哥，一位医学院的学生，正在为即将到来的考试做准备。他今年24岁，对医学充满热情。图书馆里非常安静，我们专心致志地学习。哥哥的爱好是玩篮球，他经常说运动是放松大脑的最佳方式。他总是希望我也能热爱学习，努力追求知识。】\n请输入你的问题：",key='input')
    if user_input:
        st.session_state['past'].append(user_input)
        message(st.session_state['past'][-1], 
                    is_user=True, 
                    key='_user')
        role_wendao = wendao()
        # logger.info(msg)
        result = await role_wendao.run(user_input) 
        sharedData  = SharedDataSingleton.get_instance()
        json_from_data = sharedData.json_from_data
        knowledge_key= json_from_data["festival"] + json_from_data["requirement"]
        st.session_state['generated'].append("知识库数据："+str(knowledge_key))
        message(st.session_state["generated"][-1], key=str(len(st.session_state["generated"])))

        role_qianbianzhe = qianbianzhe()
        qianjibian_ans = await role_qianbianzhe.run(" ")
        # st.session_state['past'].append("等待中！！！")

        st.session_state['generated'].append("agent 千机变回答："+str(qianjibian_ans))
        message(st.session_state["generated"][-1], key=str(len(st.session_state["generated"])))
        role_ruyi = ruyi()
        ruyi_ans = await role_ruyi.run(" ")
        
        st.session_state['generated'].append("agent 如意回答："+str(ruyi_ans))
        message(st.session_state["generated"][-1], key=str(len(st.session_state["generated"])))

    # if st.session_state['generated']:
    #     for i in range(len(st.session_state['generated'])-1, -1, -1):
    #         message(st.session_state["generated"][i], key=str(i))
    #         message(st.session_state['past'][i], 
    #                 is_user=True, 
    #                 key=str(i)+'_user')
    
asyncio.run(main())
