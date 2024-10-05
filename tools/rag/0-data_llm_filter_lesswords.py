# 该脚本将会遍历一个文件夹中的所有 md 文件，将少于20个汉字的内容全部移动到指定的输出文件夹中

import os
import shutil
import re


def count_chinese_chars(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def move_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".md"):
            input_file_path = os.path.join(input_folder, filename)
            with open(input_file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if count_chinese_chars(content) < 120:
                output_file_path = os.path.join(output_folder, filename)
                shutil.move(input_file_path, output_file_path)
                print(f"已移动: {filename}")


if __name__ == "__main__":
    input_folder = ""  # 替换为实际输入文件夹路径
    output_folder = ""  # 替换为实际输出文件夹路径
    move_files(input_folder, output_folder)
