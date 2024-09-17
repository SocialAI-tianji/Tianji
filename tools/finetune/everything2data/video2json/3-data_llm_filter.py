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
from transformers import AutoModelForCausalLM, AutoTokenizer
from tianji import TIANJI_PATH
from loguru import logger


class LLMProcessor:
    def __init__(self, model_name, cache_dir, device="cuda"):
        self.model, self.tokenizer = self.load_local_model(model_name, cache_dir)
        self.device = device

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

    def process_message(
        self,
        system_message,
        user_message,
        max_length=12800,
        temperature=0.2,
        debug=False,
    ):
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs.input_ids, max_length=max_length, temperature=temperature
        )
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(inputs.input_ids, outputs)
        ]
        result = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ].strip()
        if debug:
            logger.info(f"Generated result: {result}")
        return result


def check_summary(processor, content, debug=False):
    system_message = "你是一个文档总结专家。你需要总结给定的Markdown文件内容，提取出文档的重要中心思想。请用简短一段连贯的话总结文档内容。"
    user_message = content + "\n\n你的总结是:"
    return processor.process_message(system_message, user_message, debug=debug)


def check_theme(processor, summary, theme, debug=False):
    system_message = "你是一个文档主题检查专家。你需要检查给定的文档总结是否符合指定的主题要求。请根据总结内容进行判断：1. 文档内容是否与指定主题相关。如果文档符合以上标准，请返回 true；否则返回 false。请只返回 true 或 false，不需要返回任何其他返回值."
    user_message = f"主题是:{theme}\n\n需要检查的文档总结如下：{summary}"
    result = processor.process_message(
        system_message, user_message, debug=debug
    ).lower()
    return result == "true"


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
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder
    theme = args.theme
    debug = args.debug
    model_name = args.model
    error_log_path = os.path.join(output_folder, "error_log.txt")

    cache_dir = os.path.join(TIANJI_PATH, "temp", "local_llm")
    processor = LLMProcessor(model_name, cache_dir)

    os.makedirs(output_folder, exist_ok=True)

    for filename in tqdm(os.listdir(input_folder), desc="处理文件"):
        if filename.endswith(".md"):
            input_file_path = os.path.join(input_folder, filename)
            try:
                with open(input_file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                summary = check_summary(processor, content, debug)
                is_relevant = check_theme(processor, summary, theme, debug)
                if not is_relevant:
                    output_file_path = os.path.join(output_folder, filename)
                    shutil.move(input_file_path, output_file_path)  # 移动不符合要求的文件
            except Exception as e:
                with open(error_log_path, "a", encoding="utf-8") as error_log:
                    error_log.write(f"处理失败: {filename}, 错误: {str(e)}\n")


if __name__ == "__main__":
    main()
