"""
使用说明:
    该脚本用于清理指定文件夹中的 Markdown 文件，去除时间戳和无关内容，并将清理后的内容保存到另一个文件夹。

    使用方法:
    python 2-timemd2fullmd.py -f <输入文件夹路径> -o <输出文件夹路径>

    参数:
    -f --folder_path: 指定 Markdown 文件所在的输入文件夹路径。
    -o --output_folder_path: 指定清理后 Markdown 文件的输出文件夹路径。
"""

import glob
import os
import re
import argparse


def extract_clean_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Remove time stamps and < No Speech > markers
    cleaned_text = re.sub(r"\[\d+,\d{2}:\d{2}\]\s*< No Speech >", "", content)
    cleaned_text = re.sub(r"\[\d+,\d{2}:\d{2}\]", "", cleaned_text)
    cleaned_text = re.sub(r"< No Speech >", "", cleaned_text)

    # Remove any additional non-content text
    cleaned_text = re.sub(r"<video.*?>.*?</video>", "", cleaned_text, flags=re.DOTALL)
    cleaned_text = re.sub(
        r"Texts generated.*?\.srt\)", "", cleaned_text, flags=re.DOTALL
    )

    cleaned_text = re.sub(
        r"Mark the sentences.*?subtitle context\.", "", cleaned_text, flags=re.DOTALL
    )
    cleaned_text = re.sub(r"- \[.*?\]\s*", "", cleaned_text)
    cleaned_text = re.sub(r"<-- Mark if you are done editing\.\s*\.", "", cleaned_text)
    # Clean up remaining spaces and newlines
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    # Remove spaces around punctuation
    cleaned_text = re.sub(r"\s([.,!?;:])", r"\1", cleaned_text)
    cleaned_text = re.sub(r"([.,!?;:])\s", r"\1", cleaned_text)

    # Replace remaining spaces with commas where appropriate
    formatted_text = re.sub(r"(\S)\s+(\S)", r"\1,\2", cleaned_text)
    # Ensure no comma follows a period
    formatted_text = re.sub(r"\。,", "。", formatted_text)
    # Remove special characters except for punctuation and alphanumeric
    formatted_text = re.sub(r"[^\w\s.,!?;:]", "", formatted_text)
    return formatted_text


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="清理指定文件夹中的 Markdown 文件")
    parser.add_argument(
        "-f", "--folder_path", type=str, default="./audio_md", help="输入 Markdown 文件夹路径"
    )
    parser.add_argument(
        "-o",
        "--output_folder_path",
        type=str,
        default="./audio_md_full",
        help="输出 Markdown 文件夹路径",
    )
    args = parser.parse_args()

    input_folder_path = args.folder_path
    output_file_directory = args.output_folder_path
    path = glob.glob(os.path.join(input_folder_path, "*"))
    length = len(path)

    if not os.path.exists(output_file_directory):
        os.mkdir(output_file_directory)

    for i in range(length):
        input_file_path = path[i]
        output_file_name = os.path.basename(input_file_path)
        extracted_text = extract_clean_text(input_file_path)
        output_file_path = os.path.join(output_file_directory, output_file_name)
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(extracted_text)
