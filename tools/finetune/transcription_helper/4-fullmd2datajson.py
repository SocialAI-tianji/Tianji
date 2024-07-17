import json
import os

SYSTEM_PROMPT = """
你是一个信息抽取能手，你需要把我给你的内容做成QA对，模拟人和大模型的对话，你的回复要满足下列要求：
- 全部使用中文回复
- 基于材料主题返回5条符合的QA对，但不要重复说相同问题，
- 如果遇到里面提到几步法，你要合在一个回答里面
- 基于材料返回详细的解释。
- 提问要模拟用户在这个知识点的提问主题下进行对话、提问要做到口语化并尽可能简单且不要涉及到具体的人，提问最好大于5个字少于0个字（格式类似：......怎么办，......为什么？），而回答应非常详细可分点回答、需要长回答详细紧扣我给你的东西，
- 因为我给你的材料是语音转文本，可能有错误，你要在基于上下文理解的基础上帮忙修复。
- 不要提到任何作者信息，只需要结合内容回答抽取。
- 最后只需要返回json list,严格遵守返回为json list格式：[{"input": ,"output": },{"input": ,"output": }]
需要抽取的原文如下：
"""

# 
# 设置 zhipuai API 的密钥
from zhipuai import ZhipuAI
def get_data_ds(content):
    client = ZhipuAI(api_key=key) # 请填写您自己的APIKey
    response = client.chat.completions.create(
      model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # 系统消息，通常用于设置上下文或系统角色
            {"role": "user", "content": content, "temperature": 0.7}  # 用户消息，包含输入内容和输出多样性参数
        ]
        #stream=True,
        )
    res = response.choices[0].message.content
    return res

txt_folder_path = "txt地址"  # fullmd 的文件夹地址
output_file_path = './xxxxxxx.json' # 保存 json 名
error_file_path = "./tianji_qa_error_files.txt"

all_qadata = []
count = 0
for filename in os.listdir(txt_folder_path):
    print(f"\n\n当前处理第{count}个txt文件 {filename}\n")
    file_path = os.path.join(txt_folder_path, filename)  # 获取文件完整路径
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # 读取文件内容
            llm_reply = get_data_ds("<<开始>>"+f"当前文件主题为{filename}"+content+"<<结束>>")
            json_text = llm_reply.replace(' ','').replace('\n','').replace('```','').replace('json','',1)
            json_text = json_text.strip()
            qadata = json.loads(json_text)
            print("当前结果:\n",qadata)
            all_qadata.extend(qadata)
    except Exception as e:
        # 重试一次
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()  # 读取文件内容
                llm_reply = get_data_ds("<<开始>>"+f"当前文件主题为{filename}"+content+"<<结束>>")
                json_text = llm_reply.replace(' ','').replace('\n','').replace('```','').replace('json','',1)
                json_text = json_text.strip()
                qadata = json.loads(json_text)
                print("当前结果:\n",qadata)
                all_qadata.extend(qadata)   
        except Exception as e:
            # 如果处理过程中出现异常，记录错误文件地址
            with open(error_file_path, "a", encoding='utf-8') as error_file:
                print("错误！",e)
                print("错误！",json_text)
                error_file.write(file_path+'\n')
        continue
    count += 1
with open(output_file_path, "w", encoding='utf8') as f:
    json.dump(all_qadata, f, ensure_ascii=False, indent=4)
