"""
使用说明:
    该脚本用于将 JSON 文件转换为最终知识库使用的文本语料。

    使用方法:
    python 3-json2txt.py -f <输入文件夹路径> [-o <输出文件夹路径>]

    参数:
    -f --folder: 指定包含所有 JSON 文件的输入文件夹路径。
    -o --output: 指定保存文本文件的输出文件夹路径，默认为输入文件夹路径。
"""

import os
import json
import argparse


def process_json_files(input_folder, output_folder):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {filename}")
                    continue

            # 创建对应的文本文件名
            txt_filename = f"{os.path.splitext(filename)[0]}.txt"
            txt_filepath = os.path.join(output_folder, txt_filename)

            # 写入整个 JSON 文件的内容到文本文件
            with open(txt_filepath, "w", encoding="utf-8") as txt_file:
                for item in data:
                    for key, value in item.items():
                        txt_file.write(f"{key}: {value}\n\n")

            print(f"Processed {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将 JSON 文件转换为文本语料")
    parser.add_argument("-i", "--folder", required=True, help="输入文件夹路径")
    parser.add_argument("-o", "--output", default=None, help="输出文件夹路径，默认为输入文件夹路径")
    args = parser.parse_args()

    output_folder = args.output if args.output else args.folder
    os.makedirs(output_folder, exist_ok=True)  # 确保输出目录存在
    process_json_files(args.folder, output_folder)
