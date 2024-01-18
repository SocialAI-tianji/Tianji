# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus


from http import HTTPStatus
import random
import streamlit as st
import asyncio
import streamlit as st
from streamlit_chat import message
import asyncio
import os
os.environ["OPENAI_API_KEY"] = "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"  # 填入你自己的OpenAI API key
os.environ["OPENAI_API_MODEL"] = "gpt-3.5-turbo" # 选择你要使用的模型，例如：gpt-4, gpt-3.5-turbo
os.environ["OPENAI_API_BASE"] = "https://api.openai-forward.com/v1"
import sys
sys.path.append("MetaGPT")
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
import uuid

# 初始化session_state变量
if 'user_id' not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    st.session_state['user_id'] = str(uuid.uuid4())
    st.write(f"您的会话ID是: {st.session_state['user_id']}")


# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    st.markdown("## 友情提示")
    "我是人情世故大模型团队开发的祝福agents。你可以在这里找到一个完整的祝福。我会告诉你怎么写，还会针对你的祝福给你生成专属的知识文档。\n 首先你需要完整的告诉我，你想在什么节日给谁送祝福？这个人是谁呢（是妈妈）？他会有什么愿望呢？你想在什么时候送给他？可以告诉我他的爱好、性格、年龄段、最近的状态。\n 就像这段：【元旦节下午，我和哥哥一起去图书馆学习。我想给哥哥一个祝福。我的哥哥，一位医学院的学生，正在为即将到来的考试做准备。他今年24岁，对医学充满热情。图书馆里非常安静，我们专心致志地学习。哥哥的爱好是玩篮球，他经常说运动是放松大脑的最佳方式。他总是希望我也能热爱学习，努力追求知识。】\n请输入你的问题："
    # 创建一个滑块，用于选择最大长度，范围在0到1024之间，默认值为512
    #max_length = st.slider("max_length", 0, 1024, 512, step=1)
    #templature = st.slider("templature", 0, 1024, 512, step=3)
    if st.button('清除历史'):
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
st.title("💬 人情世故大模型")
st.caption("🚀 解决你的烦恼")

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



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
    role_wendao = wendao()
    result = await role_wendao.run(user_input)
    return result.content

async def run_async_qianbianzhe(user_input):
    role_wendao = qianbianzhe()
    result = await role_wendao.run(user_input)
    return result.content

async def run_async_ruyi(user_input):
    role_wendao = ruyi()
    result = await role_wendao.run(user_input)
    return result.content

def json_to_special_str(data):
    result = ""
    for key, value in data.items():
        if value == "":
            value = "无"
        result += f"{key} - {value}<br/>"
    return result

def show_history_st_messages():
    sharedData  = SharedDataSingleton.get_instance()
    for one_message in sharedData.chat_history:
        if one_message['method'] == "json":
            st.chat_message( one_message['role'] ).json( one_message['showdata'] )
        if one_message['method'] == "write":
            st.chat_message( one_message['role'] ).write( one_message['showdata'] )

def show_one_message( role , method="write", showdata="",is_add=False):
    sharedData  = SharedDataSingleton.get_instance()
    if method == "json":
        st.chat_message( role ).json( showdata )
    if method == "write":
        st.chat_message( role ).write( showdata )
    if is_add == True:
        sharedData.chat_history.append({"role": role , "method": method , "showdata": showdata})



status_step = 0
st.chat_message( "assistant" ).write( "小伙伴，请告诉你送祝福的具体需求哟!" )

# 在Streamlit代码中调用异步函数
if prompt := st.chat_input():

    # 显示历史消息--优化前端效果
    show_history_st_messages()

    sharedData  = SharedDataSingleton.get_instance()
    #st.chat_message("user").write(prompt)
    show_one_message( role="user" , method="write" , showdata=prompt , is_add = True)
    
    #st.write(f"您的会话ID2是: {st.session_state['user_id']}")
    
    # 了解用户的需求
    if status_step == 0:
        #st.write(f"您的会话ID3是: {st.session_state['user_id']}")
        # 运行异步代码并获取结果
        sharedData.first_status_user_history = sharedData.first_status_user_history + "\n" + "user:" + str(prompt)
        st.chat_message("assistant").write("正在处理，请稍候...")
        result = run_async_code(run_async_model, sharedData.first_status_user_history)
        show_one_message( role="assistant" , method="write" , showdata="目前阶段的需求汇总如下" , is_add = False)
        show_one_message( role="assistant" , method="json" , showdata=sharedData.json_from_data , is_add = False)
        #st.chat_message("assistant").write("目前阶段的需求汇总如下")
        #st.chat_message("assistant").json( sharedData.json_from_data )

        first_status_result_list = result.split("|")
        if first_status_result_list[0] == "NO":
            #st.chat_message("assistant").write(first_status_result_list[1])
            show_one_message( role="assistant" , method="write" , showdata=first_status_result_list[1]  , is_add = True)
            sharedData.first_status_user_history = sharedData.first_status_user_history + "\n" + "assistant:" + str(first_status_result_list[1])
        else:
            status_step = 1
            #st.chat_message("assistant").write("需求收集完毕，谢谢你")
            show_one_message( role="assistant" , method="write" , showdata="需求收集完毕，谢谢你", is_add = True)
        

    # 读取知识库
    if status_step == 1:
        json_from_data = sharedData.json_from_data
        knowledge_key= json_from_data["festival"] + json_from_data["requirement"]
        st.chat_message("assistant").write("知识库数据："+str(knowledge_key))
        status_step = 2
    # 获取 千机变 答案
    if status_step == 2:
        st.chat_message("assistant").write("正在处理，请稍候...")
        qianjibian_ans = run_async_code(run_async_qianbianzhe, " ")
        st.chat_message("assistant").write("agent 千机变回答："+str(qianjibian_ans))
        status_step = 3

    # 获取 如意 答案
    if status_step == 3:
        st.chat_message("assistant").write("正在处理，请稍候...")
        ruyi_ans = run_async_code(run_async_ruyi, " ")
        st.chat_message("assistant").write("agent 如意回答："+str(ruyi_ans))
        

        


