from dotenv import load_dotenv
load_dotenv()

import asyncio
import uuid
import copy
import os
from typing import Optional, Tuple
from tianji.agents.metagpt_agents.answerBot import AnswerBot
from tianji.agents.metagpt_agents.searcher import Searcher
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.helper_func import load_json, extract_all_types, extract_single_type_attributes_and_examples
import json

# 异步代码执行函数
def run_async_code(async_function, *args, **kwargs):
    """执行异步函数并返回结果。"""
    return asyncio.run(async_function(*args, **kwargs))

async def async_func(role, user_input):
    """异步调用角色的 run 方法。"""
    result = await role.run(user_input)
    try:
        return result.content
    except:
        return ""

class ChatSession:
    def __init__(self, default_input: str):
        self.user_id = str(uuid.uuid4())
        print(f"您的会话ID是: {self.user_id}")
        self.sharedData = SharedDataSingleton.get_instance()
        self.role_answerBot = AnswerBot()
        self.role_searchBot = Searcher()
        self.json_data = load_json("scene_attribute.json")

        # 初始化状态变量
        self.scene_label = ""
        self.scene_attribute = {}
        self.mock_intentReg_ans = ""
        self.input_texts = []
        self.selected_options_list = []
        self.form_count = 0
        self.form_submitted = {}
        self.deleted_forms = []
        self.enable_answerBot = False
        self.searcher_result = []
        self.answerBot_result_with_searcher = []

        # 设置默认输入
        self.default_input = default_input

    def on_btn_click(self):
        """重置会话状态。"""
        self.sharedData.message_list_for_agent.clear()
        self.sharedData.chat_history.clear()
        self.sharedData.scene_label = ""
        self.sharedData.scene_attribute = {}
        self.scene_label = ""
        self.scene_attribute = {}
        self.input_texts.clear()
        self.selected_options_list.clear()
        self.form_count = 0
        self.form_submitted = {}
        self.deleted_forms.clear()
        self.searcher_result.clear()
        self.answerBot_result_with_searcher.clear()
        print("聊天历史已清除。")

    def flip(self, check: bool):
        """切换 answerBot 的启用状态。"""
        self.enable_answerBot = check
        print(f"AnswerBot 已 {'启用' if check else '禁用'}。")

    def initialize_sidebar(self):
        """初始化用户意图和相关选项。"""
        print("搜索引擎助手单元测试，请先选择用户意图（用数字表示），以模拟意图识别 agent 的返回值")
        scenes = extract_all_types(self.json_data)
        for item in scenes:
            print(f"- {item}")
        # 使用默认输入，设置用户意图为4（送祝福）
        self.mock_intentReg_ans = "4"  # 修改为字符串"4"
        print(f"用户当前意图：{self.mock_intentReg_ans}")
        self.on_btn_click()  # 默认清空历史
        # 启用 AnswerBot
        self.flip(True)

    def show_history_messages(self):
        """显示聊天历史。"""
        for one_message in self.sharedData.chat_history:
            if one_message["method"] == "json":
                print(f"{one_message['role']} (JSON): {json.dumps(one_message['showdata'], indent=2)}")
            if one_message["method"] == "write":
                print(f"{one_message['role']}: {one_message['showdata']}")

    def show_one_message(self, role, method="write", showdata="", is_add=False):
        """显示单个消息并可选择添加到聊天历史。"""
        if method == "json":
            print(f"{role} (JSON): {json.dumps(showdata, indent=2)}")
        elif method == "write":
            print(f"{role}: {showdata}")
        if is_add:
            self.sharedData.chat_history.append(
                {"role": role, "method": method, "showdata": showdata}
            )

    def get_answerBot_ans(self, add_chat_history=True):
        """获取 AnswerBot 的回答。"""
        for item_1, item_2 in zip(self.input_texts, self.selected_options_list):
            _, value_1 = next(iter(item_1.items()))
            _, value_2 = next(iter(item_2.items()))
            self.sharedData.message_list_for_agent.append({value_2[0]: value_1})

        self.sharedData.scene_attribute = copy.deepcopy(self.scene_attribute)
        final_ans = run_async_code(
            async_func,
            role=self.role_answerBot,
            user_input=str(self.sharedData.message_list_for_agent),
        )
        self.sharedData.message_list_for_agent.clear()
        if add_chat_history:
            self.sharedData.chat_history.append(
                {"role": "assistant", "method": "write", "showdata": final_ans}
            )
        else:
            return final_ans

    def get_searcherBot_ans(self):
        """获取 SearcherBot 的回答。"""
        for item_1, item_2 in zip(self.input_texts, self.selected_options_list):
            _, value_1 = next(iter(item_1.items()))
            _, value_2 = next(iter(item_2.items()))
            self.sharedData.message_list_for_agent.append({value_2[0]: value_1})
        run_async_code(
            async_func,
            role=self.role_searchBot,
            user_input=str(self.sharedData.message_list_for_agent),
        )

    def generate_forms_with_default_input(self):
        """生成输入框和多选框，并使用默认输入。"""
        form_key = f"form_{self.form_count}"
        if form_key in self.deleted_forms:
            return
        input_text = self.default_input
        options = ["user", "assistant"]
        selected_option = "assistant"  # 根据需要选择，默认选择 'assistant'

        self.input_texts.append({form_key: input_text})
        self.selected_options_list.append({form_key: [selected_option]})
        self.form_submitted[form_key] = True
        self.form_count += 1
        print(f"表单已提交，输入内容: '{input_text}', 选项: '{selected_option}'")

    def set_scene_attributes_with_default_input(self):
        """设置场景细化要素。"""
        self.scene_label = self.mock_intentReg_ans
        _, scene_attributes, _ = extract_single_type_attributes_and_examples(
            self.json_data, self.scene_label
        )
        self.scene_attribute = {attr: "" for attr in scene_attributes}

        # 根据默认输入填充 scene_attribute
        # 这里根据送祝福场景的要素进行设置
        self.scene_attribute['对象年龄段'] = '20岁'
        self.scene_attribute['语言风格'] = '小红书风格'
        self.scene_attribute['对象角色'] = '姐姐'
        self.scene_attribute['节日'] = '生日'
        self.sharedData.scene_attribute = copy.deepcopy(self.scene_attribute)
        print(f"场景细化要素已设置: {self.scene_attribute}")

    def trigger_searcher_agent(self):
        """触发 searcher Agent 并处理结果。"""
        all_filled = all(value.strip() for value in self.scene_attribute.values())

        if not all_filled:
            print("请填写所有场景细化要素后再触发 searcher Agent。")
            return
        self.get_searcherBot_ans()
        urls = []
        filtered_result = []
        for item in self.sharedData.search_results.values():
            if "url" in item:
                urls.append(item["url"])
            if "filtered_content" in item:
                filtered_result.append(item["filtered_content"])

        delimiter = "==== 搜索结果: ====\n"
        urls_str = "   ".join(urls)
        filtered_result_str = "\n".join([f"{delimiter}{item}" for item in filtered_result])

        sa_res1 = "生成的额外查询：" + str(self.sharedData.extra_query)
        sa_res2 = "搜索引擎返回的网页为：\n" + urls_str
        sa_res3 = "判断需要进一步查询的网页为：" + str(self.sharedData.filter_weblist)
        sa_res4 = "从搜索结果提取到的资讯：\n" + filtered_result_str

        self.searcher_result.extend([sa_res1, sa_res2, sa_res3, sa_res4])

        print("\n--- Searcher Agent 结果 ---")
        for res in self.searcher_result:
            print(res)

        if self.enable_answerBot:
            final_ans = self.get_answerBot_ans(add_chat_history=False)
            self.answerBot_result_with_searcher.append(final_ans)

            self.sharedData.search_results.clear()
            self.get_answerBot_ans()

            print("\n--- AnswerBot 结果 ---")
            print(final_ans)

    def run(self):
        """主运行流程，使用默认输入自动执行所有步骤。"""
        self.initialize_sidebar()
        self.generate_forms_with_default_input()
        self.set_scene_attributes_with_default_input()
        self.trigger_searcher_agent()
        self.show_history_messages()

        # 显示带有搜索引擎结果的 AnswerBot 结果
        print("\n--- 带有搜索引擎结果的 AnswerBot ---")
        for item in self.answerBot_result_with_searcher:
            self.show_one_message(role="assistant", method="write", showdata=item, is_add=False)

        # 显示默认的 AnswerBot 聊天历史
        print("\n--- 默认的 AnswerBot 聊天历史 ---")
        self.show_history_messages()

# 示例主程序运行
if __name__ == "__main__":
    # 设置默认输入
    default_input = "祝我姐姐生日快乐 20岁 小红书风格"
    session = ChatSession(default_input=default_input)
    session.run()