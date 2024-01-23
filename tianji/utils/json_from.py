
import streamlit as st
# shared_data_singleton.py

class SharedDataSingleton:
    _instance = None
    json_from_data = None  # 这是要共享的变量
    first_status_user_history = ""
    first_status_message_list = []
    chat_history = []
    uuid_obj = {}
    ask_num=0

    @classmethod
    def get_instance(cls):
        user_id = ""
        if 'user_id' in st.session_state:
            user_id = st.session_state['user_id']
            #st.write(f"您的会话ID6是: {user_id}")
        #if cls._instance is None:
            #cls._instance = cls()
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
        cls.first_status_user_history = ""
        cls.first_status_message_list = []
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
        "wish": ""
    }

    # 可以添加更多方法来操作 shared_variable
