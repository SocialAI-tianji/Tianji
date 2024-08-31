"""
使用说明:
    本脚本用于生成针对不同对象和场景的祝福语，你可以在 main 函数部分修改配置，运行不同的祝福语生成

    使用方法:
    python get_wish_datas.py

    参数:
    无需参数配置，直接运行脚本即可生成祝福语。
"""

from zhipuai import ZhipuAI
import time
import json
import random
import datetime

# zhipuai
# 此处填写您自己的APIKey
# zhipu_api_key = ""
# client = ZhipuAI(api_key=zhipu_api_key)
# def get_data_zhipu(content):
#     response = client.chat.completions.create(
#         model="glm-4",  # 填写需要调用的模型名称
#         messages=[
#             {"role": "system", "content": "你现在是一个精通言语表达、热爱他人、尊重长辈、富有文采的送祝福大师，请你编辑一条文本，表示对应场景的祝福语"},
#             {"role": "user",
#              "content": content,
#              "temperature": 1} # 多样化输出
#         ],
#     )
#     res = response.choices[0].message.content
#     return res

# deepseek
from openai import OpenAI

deepseek_key = ""  # 此处填写deepseek的key
client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/v1")


def get_data_ds(content):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你现在是一个精通言语表达、热爱他人、尊重长辈、富有文采的送祝福大师，请你编辑一条文本，表示对应场景的祝福语",
            },
            {"role": "user", "content": content, "temperature": 1},  # 多样化输出
        ],
    )
    res = response.choices[0].message.content
    return res


# 可利用大模型补充不同对象  当前28种
name_list = [
    "赵老师",
    "大舅",
    "大伯",
    "李总",
    "邻居赵大妈",
    "母亲",
    "姐姐",
    "妹妹",
    "哥哥",
    "弟弟",
    "爷爷",
    "奶奶",
    "外公",
    "外婆",
    "伯母",
    "叔叔",
    "阿姨",
    "堂兄",
    "堂妹",
    "表哥",
    "表妹",
    "导师",
    "同学",
    "同事",
    "领导",
    "邻居",
    "老板",
    "医生",
]

# 可利用大模型补充对应场景 当前18种
scenes = [
    "生日",
    "春节",
    "元宵节",
    "端午节",
    "七夕节",
    "中秋节",
    "重阳节",
    "除夕",
    "腊八节",
    "谈判顺利",
    "乔迁新居",
    "周年纪念",
    "新婚快乐",
    "家庭和睦",
    "比赛取得好成绩",
    "发财",
    "工作升职 ",
    "康复",
]

# 可利用大模型补充不同风格，加入更多 fewshot 造出更好的数据
styles = {
    "小红书": {
        "style_temple": "小红书风格，每条加入1-2个emoji表情包来增加趣味性。\n### 注意，你要参考下列句子的艺术风格进行祝福语撰写（注意！只看造句风格），祝福语结尾都带上语气助词词，参考句子为：{} ###",
        "if_example": True,
        "examples": [
            "默念你的名,祝你前途云蒸霞蔚，灿若星河。愿你度过的叫吉时，得到的叫如愿！",
            "希望你岁末将至，敬颂冬绥，平安喜乐，万事胜意。",
            "希望你不用奔赴大海，也能看到春暖花开；不用颠沛流离，也能遇到一生所伴！",
            "祝我们好在春夏秋冬,祝你阔谈，祝你烂漫，祝你和自己相约在风里，此后只剩欢愉。",
            "希望你可以明确地爱，直接的厌恶，真诚的喜欢，站在太阳下的坦荡，大声无愧地称赞自己，学会爱自己！",
            "前方荣光万丈，身后温暖一方，凡是过往，皆为序章。",
            "愿所念之人 平安喜乐。愿所想之事 顺心如意！",
        ],
    },
    "正常": {"style_temple": "正常风格，有礼貌即可", "if_example": False, "examples": []},
    "严肃": {
        "style_temple": "商业严肃风格，要求用在职场或长辈祝福上，显得有礼貌、干练,句子可以长一些",
        "if_example": False,
        "examples": [],
    },
}

random_finalprompt_sentence = [
    "",  # 默认情况
    "回答中可以不出现对象称谓和场景信息，也不用出现“愿你”“祝你”（对自己的长辈需要出现对象称谓和祝你），",
    "回答中可以不出现对象称谓和场景信息，",
    "回答中不用出现“愿你”“祝你”",
]
final_prompt = """
该祝福语字数小于 {} 字。 \n
请根据对象称谓及场景，写出符合对象的身份和场景气氛的祝福文案。要求的风格是：{} \n，注意不要有标题混在其中，对象称谓是：{}，祝福场景是：{}。 \n
{} 根据不同对象用不同的语气（尊敬、诙谐搞笑、亲近），请直接返回祝福文本，不要说任何其他话：
"""

if __name__ == "__main__":
    # 在此处进行配置
    roop_count = 2  # 循环次数
    now_count = 0  # 当前生成数目
    stylename = "小红书"  # 风格名称：小红书、正常、严肃
    output_number_limit = 50  # 限制回答输出长度，严肃的100，普通的小于20

    for roop in range(roop_count):
        conversations = []
        for name in name_list:
            for scene in scenes:
                try:
                    if styles[stylename]["if_example"]:
                        style_prompt = styles[stylename]["style_temple"].format(
                            random.choice(styles[stylename]["examples"])
                        )
                    else:
                        style_prompt = styles[stylename]["style_temple"]
                    input_prompt = final_prompt.format(
                        output_number_limit,
                        style_prompt,
                        name,
                        scene,
                        random.choice(random_finalprompt_sentence),
                    )

                    response = get_data_ds(input_prompt)
                    now_count += 1

                    if "\n" in str(response):
                        response = str(response).split("\n")[0]

                    print(name, scene, "response:", response)
                    print("当前生成数目：", now_count)
                    if stylename == "正常":
                        # 默认不加风格指定
                        _input_prompt = f"祝{name}{scene}"
                    else:
                        _input_prompt = f"祝{name}{scene},{stylename}风格"
                    print("input:", _input_prompt)

                    conversation = {
                        "conversation": [
                            {
                                "system": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福",
                                "src_input": input_prompt,
                                "style_name": stylename,
                                "input": _input_prompt,
                                "output": str(response).replace('"', ""),
                            }
                        ]
                    }

                    # 将对话加入到列表中
                    conversations.append(conversation)
                except Exception as e:
                    print(e)
                    continue

        now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f"./wishes_{stylename}_{now_time}.json"
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(conversations, f, ensure_ascii=False, indent=4)
