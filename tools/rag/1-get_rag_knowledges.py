"""
使用说明:
    该脚本用于从指定文件夹中的文本文件提取信息并生成知识语料的JSON格式。

    使用方法:
    python get_rag_knowledges.py -f <输入文件夹路径> -o <输出JSON文件路径> -m <模型类型> [-d]

    参数:
    -f --folder_path: 指定文本文件所在的输入文件夹路径。
    -o --output_file: 指定生成的JSON文件路径。
    -m --model: 指定使用的模型类型，可选值为 "zhipu", "deepseek", "local"。默认为 "zhipu"。
    -d --debug: 启用调试模式，打印每一个llm输出的结果。

    输出 JSON 的内部样式参考:
    {
        "该段落标题":"段落的总结1. 2. 3."
    }
    {
        "该段落标题":"段落的总结1. 2. 3."
    }
"""

import json
import os
import argparse
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from openai import OpenAI  # 导入 deepseek 的 OpenAI
from tqdm import tqdm  # 导入 tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer  # 导入 Hugging Face 的库
from loguru import logger
from tianji import TIANJI_PATH

load_dotenv()

SUMMARY_PROMPT = """
你是一个知识库语聊准备能手，你需要把我给你的内容总结成陈述句的知识语料,用于知识库检索，你在总结时需要注意下列要求：
- 全部使用中文回复.
- 如果遇到里面提到几步法，你要合在一个回答里面.
- 如果里面提到人名或者是作者名 需要忽略或者代称.
- 文中涉及关注公众号\微信之类的,需要忽略.
- 总结后需要涵盖全方面,变为类似知识条款的参考，不要分点分1、2、3！！！只需要是一大段一大段的知识库整理.
总结只返回条款内容。需要总结的原文如下：
"""

TITLE_PROMPT = """
请为以下内容总结一个简短的主题或标题，不超过20个字,只要关注内容,不能有任何人名相关：
"""


def get_summary(content, model_type="zhipu", debug=False):
    return get_llm_response(SUMMARY_PROMPT + content, model_type, debug)


def get_title(content, model_type="zhipu", debug=False):
    return get_llm_response(TITLE_PROMPT + content, model_type, debug)


def get_llm_response(prompt, model_type="zhipu", debug=False):
    if model_type == "deepseek":
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE")
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个知识库语料准备能手，你会把文章的重点整理成一大段话"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            top_p=0.8,
        )
        res = response.choices[0].message.content
    elif model_type == "local":
        model_name = "internlm/internlm2_5-7b-chat"
        cache_dir = os.path.join(TIANJI_PATH, "temp", "local_llm")
        device = "cuda"  # 设备设置
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

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            inputs.input_ids, max_new_tokens=50, max_length=12800, temperature=0.1
        )
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(inputs.input_ids, outputs)
        ]

        res = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    else:
        client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": prompt,  # 这里传递 prompt
                    "temperature": 0.1,
                },
            ],
        )
        res = response.choices[0].message.content

    if debug:
        logger.info(f"Generated result: {res}")

    return res.strip()


def process_file(file_path, model_type, debug=False):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        title = get_title(content, model_type, debug)
        summary = get_summary(content, model_type, debug)
        return {title: summary}  # 使用生成的主题作为key


def main():
    parser = argparse.ArgumentParser(description="从文本文件夹提取信息并生成知识语料的JSON格式")
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
    parser.add_argument(
        "-d", "--debug", action="store_true", help="启用调试模式，打印每一个llm输出的结果"
    )
    args = parser.parse_args()

    txt_folder_path = args.folder_path
    output_file_path = args.output_file
    model_type = args.model
    debug = args.debug
    error_file_path = os.path.join(TIANJI_PATH, "temp", "knowledge_error_files.txt")

    filenames = os.listdir(txt_folder_path)
    all_knowledge_data = []
    for filename in tqdm(filenames, desc="处理文件"):
        file_path = os.path.join(txt_folder_path, filename)
        try:
            knowledge_data = process_file(file_path, model_type, debug)
            if debug:
                logger.info(f"当前结果: {knowledge_data}")
            all_knowledge_data.append(knowledge_data)
        except Exception as e:
            try:
                knowledge_data = process_file(file_path, model_type, debug)
                if debug:
                    logger.info(f"重试结果: {knowledge_data}")
                all_knowledge_data.append(knowledge_data)
            except Exception as e:
                with open(error_file_path, "a", encoding="utf-8") as error_file:
                    logger.error(f"错误！{e}")
                    error_file.write(file_path + "\n")
            continue

    with open(output_file_path, "w", encoding="utf8") as f:
        json.dump(all_knowledge_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
