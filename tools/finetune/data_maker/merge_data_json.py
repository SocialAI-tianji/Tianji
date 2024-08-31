"""
使用说明:
    本脚本用于合并 `get_wish_datas.py` 文件产生的多份数据 json 文件。

    使用方法:
    python merge_data_json.py -f <输入文件夹路径> -o <输出文件路径>

    参数:
    -f --folder_path: 指定 JSON 文件所在的输入文件夹路径。
    -o --output_file: 指定合并后 JSON 文件的输出文件路径。
"""
import os
import json
import argparse
import glob


def extract_and_merge_conversations(folder_path, output_file):
    all_conversations = []

    # 遍历指定文件夹
    for filename in glob.glob(os.path.join(folder_path, "*.json")):
        # 打开并读取JSON文件
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            # 提取需要的字段
            for item in data:
                for conversation in item["conversation"]:
                    extracted = {
                        "system": conversation["system"],
                        "input": conversation["input"],
                        "output": conversation["output"],
                    }
                    # 将每个对话包装在一个 'conversation' 键中，并作为独立对象加入列表
                    all_conversations.append({"conversation": [extracted]})

    # 将合并后的所有对话数据写入一个新的JSON文件
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_conversations, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="合并 JSON 文件")
    parser.add_argument(
        "-f", "--folder_path", type=str, required=True, help="输入 JSON 文件夹路径"
    )
    parser.add_argument(
        "-o", "--output_file", type=str, required=True, help="输出 JSON 文件路径"
    )
    args = parser.parse_args()

    extract_and_merge_conversations(args.folder_path, args.output_file)
