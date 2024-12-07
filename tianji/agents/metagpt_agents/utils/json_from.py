"""
这是一个单例模式的共享数据类，用于在多个智能体之间共享数据。
主要功能:
1. 维护每个用户会话的独立数据实例
2. 存储场景标签、属性、搜索结果等会话状态
3. 保存用户的聊天历史和消息列表
4. 通过uuid区分不同用户的数据
"""

import streamlit as st


class SharedDataSingleton:
    _instance = None
    json_from_data = None  # 这是要共享的变量
    message_list_for_agent = []
    filter_weblist = []
    scene_label = ""
    scene_attribute = {}
    extra_query = []
    search_results = {}
    chat_history = []
    uuid_obj = {}
    ask_num = 0

    @classmethod
    def get_instance(cls):
        user_id = ""
        if "user_id" in st.session_state:
            user_id = st.session_state["user_id"]
        ret_cls_obj = {}
        if user_id == "":
            ret_cls_obj = cls()
            ret_cls_obj = SharedDataSingleton._new_init(ret_cls_obj)
        else:
            if user_id in SharedDataSingleton.uuid_obj:
                pass
            else:
                ret_cls_obj = cls()
                ret_cls_obj = SharedDataSingleton._new_init(ret_cls_obj)
                SharedDataSingleton.uuid_obj[user_id] = ret_cls_obj

            ret_cls_obj = SharedDataSingleton.uuid_obj[user_id]
        return ret_cls_obj

    def _new_init(cls):
        cls._instance = None
        cls.json_from_data = None  # 这是要共享的变量
        cls.message_list_for_agent = []
        cls.scene_attribute = {}
        cls.scene_label = ""
        cls.extra_query = []
        cls.search_results = {}
        cls.chat_history = []
        cls.uuid_obj = {}
        return cls

    def __init__(self):
        if SharedDataSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        # 可以在这里初始化共享变量
        SharedDataSingleton.json_from_data = {
            "requirement": "",
            "scene": "",
            "festival": "",
            "role": "",
            "age": "",
            "career": "",
            "state": "",
            "character": "",
            "time": "",
            "hobby": "",
            "wish": "",
        }

    # 可以添加更多方法来操作 shared_variable
