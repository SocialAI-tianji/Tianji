"""
使用说明:
    该脚本用于检查指定文件夹中的 Markdown 文件是否符合指定的主题要求，并将不符合要求的文件移动到输出文件夹中。

    使用方法:
    python 3-data_llm_filter.py -i <输入文件夹路径> -o <输出文件夹路径> -t <主题要求> [-d] [-m <模型类型>]

    参数:
    -i --input_folder: 指定包含 Markdown 文件的输入文件夹路径。
    -o --output_folder: 指定不符合主题要求的 Markdown 文件的输出文件夹路径。
    -t --theme: 指定主题相关的内容。比如 "敬酒/酒文化/喝酒/酒席"
    -d --debug: 启用调试模式，打印每一个llm输出的结果。
    -m --model: 指定使用的模型，默认为 'internlm/internlm2_5-7b-chat'。
"""
import os
import argparse
from tqdm import tqdm
import shutil
from dotenv import load_dotenv
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer
from zhipuai import ZhipuAI
from openai import OpenAI

load_dotenv()


class LLMProcessor:
    def __init__(
        self, model_type, model_name=None, api_key=None, cache_dir=None, device="cuda"
    ):
        self.model_type = model_type
        if model_type == "local":
            self.model, self.tokenizer = self.load_local_model(model_name, cache_dir)
            self.device = device
        elif model_type == "zhipuai":
            self.client = ZhipuAI(api_key=api_key)
        elif model_type == "openai":
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE")
            )
            self.model_name = os.getenv("OPENAI_API_MODEL")

    def load_local_model(self, model_name, cache_dir):
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
        return model, tokenizer

    def process_message(self, system_message, user_message, debug=False):
        if self.model_type == "local":
            text = self.tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                tokenize=False,
                add_generation_prompt=True,
            )
            inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs.input_ids, max_length=12800, temperature=0.2
            )
            generated_ids = [
                output_ids[len(input_ids) :]
                for input_ids, output_ids in zip(inputs.input_ids, outputs)
            ]
            result = self.tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0].strip()
        elif self.model_type == "zhipuai":
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
            response = self.client.chat.completions.create(
                model="glm-4-air",
                messages=messages,
                temperature=0.1,  # 设置温度为0.1
            )
            result = response.choices[0].message.content
        elif self.model_type == "openai":
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=2048,
                temperature=0.1,
            )
            result = response.choices[0].message.content
        return result


def check_theme(processor, summary, theme, debug=False):
    system_message = "你是一个检查专家。如果文档涉及任意一个主题内的元素就返回true。 如果是明星、特定广告、重复内容也只是返回 false。请只返回 true 或 false，不需要返回任何其他返回值."
    user_message = f"主题是:{theme}\n\n需要检查的文档如下：{summary}"
    result = processor.process_message(system_message, user_message, debug=debug)

    if_true = "true" in result
    if debug:
        logger.info(f"Generated result: {result} , {if_true}")
    return if_true


def main():
    parser = argparse.ArgumentParser(description="检查Markdown文件是否符合指定主题")
    parser.add_argument(
        "-i", "--input_folder", type=str, required=True, help="输入Markdown文件夹路径"
    )
    parser.add_argument(
        "-o", "--output_folder", type=str, required=True, help="输出文件夹路径"
    )
    parser.add_argument("-t", "--theme", type=str, required=True, help="主题要求的内容")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="启用调试模式，打印每一个llm输出的结果"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="internlm/internlm2_5-7b-chat",
        help="指定使用的模型类型",
    )
    parser.add_argument(
        "-type",
        "--model_type",
        type=str,
        choices=["local", "zhipuai", "openai"],
        required=True,
        help="选择模型类型",
    )
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder
    theme = args.theme
    debug = args.debug
    model_name = args.model
    model_type = args.model_type
    
    api_key = os.getenv("ZHIPUAI_API_KEY")
    error_log_path = os.path.join(output_folder, "error_log.txt")

    cache_dir = os.path.join(os.getenv("TIANJI_PATH", ""), "temp", "local_llm")
    processor = LLMProcessor(
        model_type, model_name=model_name, api_key=api_key, cache_dir=cache_dir
    )

    os.makedirs(output_folder, exist_ok=True)

    for filename in tqdm(os.listdir(input_folder), desc="处理文件"):
        if filename.endswith(".md"):
            input_file_path = os.path.join(input_folder, filename)
            try:
                with open(input_file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                is_relevant = check_theme(processor, content, theme, debug)
                if not is_relevant:
                    output_file_path = os.path.join(output_folder, filename)
                    shutil.move(input_file_path, output_file_path)  # 移动不符合要求的文件
            except Exception as e:
                with open(error_log_path, "a", encoding="utf-8") as error_log:
                    error_log.write(f"处理失败: {filename}, 错误: {str(e)}\n")


if __name__ == "__main__":
    main()
