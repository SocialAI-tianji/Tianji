"""
使用说明:
    本脚本用于生成针对不同对象和场景的祝福语，你可以在 main 函数部分修改配置，运行不同的祝福语生成

    使用方法:
    python get_wish_datas.py

    参数:
    无需参数配置，直接运行脚本即可生成祝福语。

其中读取参考json格式可参考如下：

{
  "1": "写这段话的时候我的眼眶有点湿润。还记得去年这个时候，你刚刚经历了人生最低谷，我们抱在一起哭了好久。但你知道吗？正是那个时候，我真正认识到了你的坚强。一年过去了，看着你重新振作起来，重拾对生活的热爱，我真的好感动。你总说自己不够优秀，但在我眼里，你就是最棒的！今天是你的生日，我想说的话太多太多，但最重要的是：谢谢你让我成为你生命中的一部分。",
  "2": "生日快乐呀！还记得去年这时候我们在奶茶店许愿吗，你说要成为最棒的设计师，现在看看，你真的做到啦！虽然中间遇到好多困难，熬了好多个夜，但是每次看你皱着眉头改方案的样子，我就知道你一定能成功。以后的路我还要一直陪着你走呢，记得请我喝奶茶哦！爱你，生日快乐！",
}

"""

import time
import json
import random
import datetime
from openai import OpenAI
import os
# OpenAI API配置
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key,base_url=os.getenv("OPENAI_API_BASE"))

def get_data_openai(content):
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {
                "role": "system", 
                "content": "你现在是一个精通言语表达、富有文采的文案改写送祝福大师，请你编辑一条文本，表示对应场景的祝福语，严格参考我给你的例句风格"
            },
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=4096,
        temperature=0.8  # 多样化输出
    )
    res = response.choices[0].message.content
    return res

def load_examples(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [v for v in data.values()]

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
    # "七夕节",
    "中秋节",
    "重阳节",
    "除夕",
    "腊八节",
    # "谈判顺利",
    "乔迁新居",
    # "周年纪念",
    # "新婚快乐",
    "家庭和睦",
    # "比赛取得好成绩",
    "发财赚钱",
    "工作升职 ",
    "康复",
]

# 加载白话和文艺风格的例子
colloquial_examples = load_examples('3-数据制造/白话故事书信.json')
literary_examples = load_examples('3-数据制造/文艺祝福短文.json')
xiaohongshu_examples = load_examples('3-数据制造/小红书风格.json')
classical_examples = load_examples('3-数据制造/文言文.json')
freestyle_examples = load_examples('3-数据制造/放飞自我风格.json')
longtext_examples = load_examples('3-数据制造/祝福长文.json')
poem_examples = load_examples('3-数据制造/诗词赋.json')

# 可利用大模型补充不同风格，加入更多 fewshot 造出更好的数据
styles = {
    "小红书": {
        "style_temple": "你是一名大学生，用大学生的语气说话，你需要严格参考例句风格，每条加入1-2个emoji表情包来增加趣味性。参考风格如下：{} ###",
        "if_example": True,
        "examples": xiaohongshu_examples
    },
    "正常": {"style_temple": "正常风格，有礼貌即可", "if_example": False, "examples": []},
    "严肃": {
        "style_temple": "严肃风格，语气要非常官方正式，不要用书信格式，这个是微信短信，可以写长一些，需要涉及到自身和对方联系，多举几个经历的事情，感谢对方，展望未来",
        "if_example": False,
        "examples": [],
    },
    "白话": {
        "style_temple": "白话风格，要求语言朴实自然，亲切随和。\n### 注意，你要参考下列句子的语言风格进行祝福语撰写（注意！只看造句风格），同时需要根据说话对象适当改写（如果该节日要素和对方身份不合适，需要及时调整到正常的话题)参考句子为：{} ###",
        "if_example": True,
        "examples": colloquial_examples
    },
    "文艺": {
        "style_temple": "文艺风格，严格参考我给你的例子\n### 注意，你要参考下列句子的文艺风格进行祝福语撰写（注意！只看造句风格），参考句子为：{} ###", 
        "if_example": True,
        "examples": literary_examples
    },
    "文言文": {
        "style_temple": "文言文风格，严格参考我给你的例子\n### 注意，你要参考下列句子的文言文风格进行祝福语撰写（注意！只看造句风格），严格参考句子：{} ###", 
        "if_example": True,
        "examples": classical_examples
    },
    "放飞自我": {
        "style_temple": "搞笑、搞笑、搞笑、随意、放飞自我的风格，严格参考我给你的例子参考句子为：{}", 
        "if_example": True,
        "examples": freestyle_examples
    },
    "祝福长文": {
        "style_temple": "祝福长文风格，严格参考我给你的例子参考句子为：{} ", 
        "if_example": True,
        "examples": longtext_examples
    },
    "诗词赋": {
        "style_temple": "诗词赋风格，严格参考我给你的例子参考句子和句子长度为：{} ", 
        "if_example": True,
        "examples": poem_examples
    }
}

random_finalprompt_sentence = [
    "",  # 默认情况
    "回答中可以不出现对象称谓和场景信息，也不用出现\"愿你\"或\"祝你\"（对自己的长辈需要出现对象称谓和祝你），",
    "回答中可以不出现对象称谓和场景信息，",
    "回答中不用出现\"愿你\"或\"祝你\",",
]
final_prompt = """
该祝福语字数小于 {} 字。 \n
请根据对象称谓及场景，写出符合对象的身份和场景气氛的祝福文案。要求的风格是：{} \n，注意不要有标题混在其中，对象称谓是：{}，祝福场景是：{}。 \n
{} 根据不同对象用不同的语气（尊敬、诙谐搞笑、亲近），可以结合带上符合对方身份可能和自己有过的一些联系和帮助，或者对方的特色；最后请直接返回祝福文本，不要说任何其他话：
"""

if __name__ == "__main__":
    # 在此处进行配置
    roop_count = 2  # 循环次数
    now_count = 0  # 当前生成数目
    stylename = "诗词赋"  # 风格名称：小红书、正常、严肃、白话、文艺、文言文、放飞自我、祝福长文、诗词赋
    output_number_limit = 2000  # 限制回答输出长度，严肃的100，普通的小于20
    save_file_path = f"./wishes_{stylename}_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json"

    for roop in range(roop_count):
        conversations = []
        for name in name_list:
            for scene in scenes:
                try:
                    if styles[stylename]["if_example"]:
                        examples = random.sample(styles[stylename]["examples"], 2)
                        style_prompt = styles[stylename]["style_temple"].format(
                            "\n".join(examples)
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
                
                    response = get_data_openai(input_prompt)
                    now_count += 1

                    # if "\n" in str(response):
                    #     response = str(response).split("\n")[0]

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

        with open(save_file_path, "w", encoding="utf8") as f:
            json.dump(conversations, f, ensure_ascii=False, indent=4)
