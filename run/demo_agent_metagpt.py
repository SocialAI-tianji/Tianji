from dotenv import load_dotenv

load_dotenv()

import asyncio
import streamlit as st
import uuid
from streamlit_chat import message

from metagpt.logs import logger

from tianji.agents.metagpt_agents.wendao import WenDao
from tianji.agents.metagpt_agents.qianbianzhe import QianBianZhe
from tianji.agents.metagpt_agents.ruyi import RuYi
from tianji.utils.json_from import SharedDataSingleton
from tianji.utils.common import timestamp_str

# 初始化session_state变量
if "user_id" not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    logger.log(0, "add uuid")
    st.session_state["user_id"] = str(uuid.uuid4())

# 设计思路 给定人设并导入参考聊天话术、历史聊天语料进行聊天。

# async def start(msg):
#     role_wendao = wendao()
#     logger.info(msg)
#     result = await role_wendao.run(msg)

#     sharedData  = SharedDataSingleton.get_instance()
#     json_from_data = sharedData.json_from_data
#     knowledge_key= json_from_data["festival"] + json_from_data["requirement"]
#     print("knowledge_key",knowledge_key)
#     knowledges = getDocumentsListByQuery(query_str=knowledge_key)
#     # print("knowledges:",knowledges,json_from_data)
#     role_qianbianzhe = qianbianzhe()
#     qianjibian_ans = await role_qianbianzhe.run(" ")
#     role_ruyi = ruyi()
#     ruyi_ans = await role_ruyi.run(" ")
#     logger.info(result)
#     print("final ans :\n",qianjibian_ans,ruyi_ans)


async def main():
    first_status_user_history = ""

    startup_guide = """
我是人情世故大模型团队开发的祝福agents。你可以在这里找到一个完整的祝福。我会告诉你怎么写还会针对你的祝福给你生成专属的知识文档。
首先你需要完整的告诉我，比如：

- 你想在什么节日给谁送祝福？
- 这个人是谁呢（是妈妈）？
- 他会有什么愿望呢？
- 你想在什么时候送给他？
- 可以告诉我他的爱好、性格、年龄段、最近的状态。

就像这段：【元旦节下午，我和哥哥一起去图书馆学习。我想给哥哥一个祝福。我的哥哥，一位医学院的学生，正在为即将到来的考试做准备。他今年24岁，对医学充满热情。图书馆里非常安静，我们专心致志地学习。哥哥的爱好是玩篮球，他经常说运动是放松大脑的最佳方式。他总是希望我也能热爱学习，努力追求知识。】

"""

    st.title("人情世故大模型_祝福模块")
    st.markdown(startup_guide)

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []

    task_status = 0

    if user_input := st.chat_input():
        sharedData = SharedDataSingleton.get_instance()

        for first_status_message in sharedData.first_status_message_list:
            message(
                first_status_message["message"],
                is_user=first_status_message["is_user"],
                key=first_status_message["keyname"],
            )

        st.session_state["past"].append(user_input)
        message(st.session_state["past"][-1], is_user=True, key="_user")

        sharedData.first_status_message_list.append(
            {
                "message": st.session_state["past"][-1],
                "is_user": True,
                "keyname": "_user" + str(timestamp_str()),
            }
        )

        # 第一阶段-搜集用户的需求

        if task_status == 0:
            sharedData.first_status_user_history = (
                sharedData.first_status_user_history + "\n" + "user:" + str(user_input)
            )

            role_wendao = WenDao()
            result = await role_wendao.run(sharedData.first_status_user_history)
            first_status_result_list = result.content.split("|")
            if first_status_result_list[0] == "NO":
                sharedData.first_status_user_history = (
                    sharedData.first_status_user_history
                    + "\n"
                    + "assistant:"
                    + str(first_status_result_list[1])
                )
                st.session_state["generated"].append(str(first_status_result_list[1]))

                message(
                    st.session_state["generated"][-1],
                    key=str(len(st.session_state["generated"])),
                )

                sharedData.first_status_message_list.append(
                    {
                        "message": st.session_state["generated"][-1],
                        "is_user": False,
                        "keyname": str(len(st.session_state["generated"]))
                        + timestamp_str(),
                    }
                )
                st.text("请继续输入")
            else:
                task_status = 1
            sharedData.ask_num += 1
            logger.info("第 {} 轮对话".format(sharedData.ask_num))

        if task_status == 1 or sharedData.ask_num > 3:
            sharedData = SharedDataSingleton.get_instance()
            json_from_data = sharedData.json_from_data
            knowledge_key = json_from_data["festival"] + json_from_data["requirement"]

            st.session_state["generated"].append("知识库数据：" + str(knowledge_key))

            message(
                st.session_state["generated"][-1],
                key=str(len(st.session_state["generated"])),
            )

            role_qianbianzhe = QianBianZhe()
            qianjibian_ans = await role_qianbianzhe.run(" ")
            # st.session_state['past'].append("等待中！！！")

            st.session_state["generated"].append(qianjibian_ans.content)
            message(
                st.session_state["generated"][-1],
                key=str(len(st.session_state["generated"])),
            )
            role_ruyi = RuYi()
            ruyi_ans = await role_ruyi.run(" ")

            st.session_state["generated"].append(ruyi_ans.content)
            message(
                st.session_state["generated"][-1],
                key=str(len(st.session_state["generated"])),
            )

    # if st.session_state['generated']:
    #     for i in range(len(st.session_state['generated'])-1, -1, -1):
    #         message(st.session_state["generated"][i], key=str(i))
    #         message(st.session_state['past'][i],
    #                 is_user=True,
    #                 key=str(i)+'_user')


asyncio.run(main())
