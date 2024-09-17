"""
使用说明:
    本脚本用于从指定的文本文件夹中提取信息，并将其转换为QA对的JSON格式。

    使用方法:
    python 4-fullmd2datajson.py -f <输入文件夹路径> -o <输出文件路径> -m <模型类型>

    参数:
    -f --folder_path: 指定包含文本文件的文件夹路径。
    -o --output_file: 指定输出的JSON文件路径。
    -m --model: 指定使用的模型类型，支持 'zhipu'、'deepseek' 或 'local'，默认为 'zhipu'。
"""

import json
import os
import argparse
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from openai import OpenAI  # 导入 deepseek 的 OpenAI
from tqdm import tqdm  # 导入 tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer  # 导入 Hugging Face 的库

load_dotenv()  # 从环境变量加载API密钥

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


def get_data_ds(content, model_type="zhipu"):
    if model_type == "deepseek":
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE")
        )  # 使用 deepseek
        response = client.chat.completions.create(
            model="deepseek-chat",  # 使用 deepseek 模型
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": content,
                    "temperature": 0.3,
                },
            ],
        )
    elif model_type == "local":
        # 使用 Hugging Face 加载本地模型
        model_name = "internlm/internlm2_5-7b-chat"  # 替换为实际模型名称
        cache_dir = os.path.join(os.getenv("TIANJI_PATH"), "temp", "local_llm")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            load_in_4bit=True,
            cache_dir=cache_dir,
            trust_remote_code=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, cache_dir=cache_dir, trust_remote_code=True
        )

        # 准备输入
        inputs = tokenizer(SYSTEM_PROMPT + content, return_tensors="pt").to("cuda")

        # 生成响应
        outputs = model.generate(inputs.input_ids, max_new_tokens=50, max_length=8096)
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(inputs.input_ids, outputs)
        ]

        res = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    else:
        client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))  # 使用 zhipu
        response = client.chat.completions.create(
            model="glm-4-flash",  # 使用 zhipu 模型
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": content,
                    "temperature": 0.7,
                },
            ],
        )
        res = response.choices[0].message.content
    return res


def process_file(file_path, model_type):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()  # 读取文件内容
        llm_reply = get_data_ds(
            "<<开始>>" + f"当前文件主题为{os.path.basename(file_path)}" + content + "<<结束>>",
            model_type=model_type,
        )
        json_text = (
            llm_reply.replace(" ", "")
            .replace("\n", "")
            .replace("```", "")
            .replace("json", "", 1)
        )
        json_text = json_text.strip()
        qadata = json.loads(json_text)
        return qadata


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="从文本文件夹提取信息并生成QA对的JSON格式")
    parser.add_argument(
        "-f", "--folder_path", type=str, required=True, help="输入文本文件夹路径"
    )
    parser.add_argument(
        "-o", "--output_file", type=str, required=True, help="输出JSON文件路径"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="zhipu",
        choices=["zhipu", "deepseek", "local"],
        help="使用的模型类型",
    )
    args = parser.parse_args()

    txt_folder_path = args.folder_path  # fullmd 的文件夹地址
    output_file_path = args.output_file  # 保存 json 名
    model_type = args.model  # 获取模型类型
    error_file_path = os.path.join(
        os.path.dirname(output_file_path), "tianji_qa_error_files.txt"
    )  # 将错误文件路径保存到输出文件夹

    all_qadata = []
    filenames = os.listdir(txt_folder_path)  # 获取文件列表
    for filename in tqdm(filenames, desc="处理文件"):  # 使用 tqdm 显示进度条
        file_path = os.path.join(txt_folder_path, filename)  # 获取文件完整路径
        try:
            qadata = process_file(file_path, model_type)
            print("当前结果:\n", qadata)
            all_qadata.extend(qadata)
        except Exception as e:
            # 重试一次
            try:
                qadata = process_file(file_path, model_type)
                print("当前结果:\n", qadata)
                all_qadata.extend(qadata)
            except Exception as e:
                # 如果处理过程中出现异常，记录错误文件地址
                with open(error_file_path, "a", encoding="utf-8") as error_file:
                    print("错误！", e)
                    error_file.write(file_path + "\n")
            continue

    with open(output_file_path, "w", encoding="utf8") as f:
        json.dump(all_qadata, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
