from dotenv import load_dotenv
load_dotenv()
import asyncio
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import json
from tianji.utils.json_from import SharedDataSingleton
from tianji.agents.wendao_agent import wendao
from tianji.agents.ruyi_agent import ruyi
# json_from_data = {
#             "requirement": "祝福",
#             "scene": "家庭聚会",
#             "festival": "元旦",
#             "role": "妈妈",
#             "age": "中老年人",
#             "career": "小学教师",
#             "state": "身体欠佳",
#             "character": "开朗",
#             "time": "傍晚",
#             "hobby": "广场舞",
#             "wish": "家庭成员平安"
#         }

# 设计思路 给定人设并导入参考聊天话术、历史聊天语料进行聊天。
class ansWrite(Action):
    
    # 这是对json中每个key的解释：
    # 语言场景（scene），目前的聊天场合，比如工作聚会。
    # 节日（festival），对话目前背景所在的节日，比如生日。
    # 聊天对象角色（role），目前谈话的对象，主要是第三人称。例如和爸爸聊天对象就是爸爸。
    # 聊天对象年龄段（age），和role相关，就是聊天对象的年龄段，例如中老年。
    # 聊天对象职业（career）， 和role相关，就是聊天对象的职业，例如教师。
    # 聊天对象状态（state），和role相关，就是聊天对象的健康状态，例如身体健康。
    # 聊天对象性格（character），和role相关，就是聊天对象的性格特点，例如开朗健谈。
    # 时间（time），和role相关，就是聊天对话时间段，如傍晚。
    # 聊天对象爱好（hobby），和role相关，就是聊天对象的兴趣爱好，例如下象棋。
    # 聊天对象愿望（wish），和role相关，就是聊天对象目前的愿望是什么，例如果希望家庭成员平安。
    
    def __init__(self, name="read_and_ana", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        sharedData: SharedDataSingleton  = SharedDataSingleton.get_instance()
        json_from_data: {} = sharedData.json_from_data
        knowledge: str = ""
        PROMPT_TEMPLATE: str = f"""
        你是一个{json_from_data["festival"]}的祝福大师。
        你需要写一段：{json_from_data["requirement"]}。这段{json_from_data["festival"]}{json_from_data["requirement"]}是在{json_from_data["scene"]}送给{json_from_data["role"]}的。
        你写的祝福需要认同{json_from_data["role"]}的愿望：{json_from_data["wish"]}。
        你写的祝福需要符合{json_from_data["role"]}的语言场景：{json_from_data["scene"]}。
        你写的祝福需要符合{json_from_data["role"]}的节日氛围：{json_from_data["festival"]}。
        你还可以根据{json_from_data["role"]}的年龄段：{json_from_data["age"]}，职业：{json_from_data["career"]}，状态：{json_from_data["state"]}，性格：{json_from_data["character"]}，当前的时间段：{json_from_data["time"]}，爱好：{json_from_data["hobby"]}作为资料参考。



        你还可以以{knowledge}为参考。

        经过思考后，将这些信息整理成一段完整的{json_from_data["requirement"]}。

        """
        print("json_from_data####################################",json_from_data)




        # knowledges = ""
        prompt = PROMPT_TEMPLATE.format(instruction=instruction)
        print(prompt)
        rsp = await self._aask(prompt)
        print("回复生成：",rsp)
        return rsp

# 设计思路 根据当前状态和聊天与恋爱相关性等综合打分。给出当前回合的打分情况
class stylize(Action):
    PROMPT_TEMPLATE = """
    你是一个萌妹，对任何人说话都很温柔客气。你很聪明礼貌。你喜欢发一些颜文字表情。大家都很喜欢你。
    请用自己的语气改写{instruction}
    """
    def __init__(self, name="rerask", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        print("风格化：",rsp)
        return rsp


# 千变者 以自己的身份回答问题
class qianbianzhe(Role):
    def __init__(
        self,
        name: str = "qianbianzhe",
        profile: str = "stylize",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([ansWrite,stylize])
        print("byorder")
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        # By choosing the Action by order under the hood
        # todo will be first SimpleWriteCode() then SimpleRunCode()
        todo = self._rc.todo

        msg = self.get_memories(k=1)[0] # find the most k recent messagesA
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self._rc.memory.add(msg)
        return msg




# 新增代码，便于区分

# 新增代码，便于区分----->Start
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


# 初始化session_state变量
if 'user_id' not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    st.session_state['user_id'] = str(uuid.uuid4())
    st.write(f"您的会话ID是: {st.session_state['user_id']}")


# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    markdown_con = '''
    ## 友情提示
    这是为了优化人情世故大模型--千变者 功能。  
    参考案例：
    ```json
    {
        "requirement": "给爷爷送祝福",
        "scene": "家庭庆祝生日",
        "festival": "中秋节",
        "role": "爷爷",
        "age": "老年",
        "career": "钓鱼爱好者",
        "state": "最近身体状态不好",
        "character": "经验丰富",
        "time": "晚上",
        "hobby": "钓鱼",
        "wish": "希望我能学会欣赏艺术的美",
        "style": "老年人版"
    }
    ```
    '''
    st.markdown(markdown_con)
    "这是为了优化人情世故大模型--千变者 功能，用于结合JSON需求生成祝福语。"    
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
st.title("💬 人情世故-千变者")
st.caption("🚀 优化 结合完整JSON需求生成祝福 的模块")
st.chat_message( "assistant" ).write( "你需要复制左边的JSON内容，然后修改对应的Key值，然后发送给我，我将满足你的需求。" )
status_step = 1

# 在Streamlit代码中调用异步函数
if prompt := st.chat_input():
    # 显示历史消息--优化前端效果
    show_history_st_messages()

    sharedData  = SharedDataSingleton.get_instance()
    json_prompt = json.loads(prompt)

    show_one_message( role="user" , method="write" , showdata="JSON格式化内容如下：" , is_add = True)
    show_one_message( role="user" , method="json" , showdata=json_prompt , is_add = True)

    
    sharedData.json_from_data = json_prompt
    json_from_data = sharedData.json_from_data
    knowledge_key= json_from_data["festival"] + json_from_data["requirement"]
    st.chat_message("assistant").write("知识库数据："+str(knowledge_key))


    st.chat_message("assistant").write("正在处理，请稍候...")
    qianjibian_ans = run_async_code(run_async_qianbianzhe, " ")
    st.chat_message("assistant").write("agent 千机变回答："+str(qianjibian_ans))

    