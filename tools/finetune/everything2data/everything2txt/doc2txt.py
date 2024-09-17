"""
使用说明:
    该脚本用于将指定文件夹中的 DOC 和 DOCX 文件转换为 TXT 文件，并将转换后的文件保存到另一个文件夹。

    使用方法:
    python convert_docs_to_txt.py -s <源文件夹路径> -d <目标文件夹路径>

    参数:
    -s --source_folder: 指定 DOC 和 DOCX 文件所在的源文件夹路径。
    -d --destination_folder: 指定转换后 TXT 文件的保存文件夹路径。
"""

import os
import sys
from docx import Document
import argparse


def convert_docs_to_txt(source_folder, destination_folder):
    # 检查目标文件夹是否存在
    if not os.path.exists(source_folder):
        print("目标文件夹不存在。请提供有效的目标文件夹路径。")
        exit()

    # 创建保存 TXT 文件的目标文件夹
    os.makedirs(destination_folder, exist_ok=True)

    # 遍历目标文件夹中的所有 DOC 文件
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".doc") or file_name.endswith(".docx"):
            doc_file = os.path.join(source_folder, file_name)
            txt_file = os.path.join(
                destination_folder, os.path.splitext(file_name)[0] + ".txt"
            )

            # 使用 python-docx 库打开 DOC 文件
            document = Document(doc_file)

            # 逐段写入 TXT 文件
            with open(txt_file, "w", encoding="utf-8") as txt:
                for paragraph in document.paragraphs:
                    txt.write(paragraph.text)
                    txt.write("\n")

            print(f"已将 {file_name} 转换为 {os.path.basename(txt_file)}")

    print("转换完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将指定文件夹中的 DOC 和 DOCX 文件转换为 TXT 文件")
    parser.add_argument("-s", "--source_folder", type=str, required=True, help="源文件夹路径")
    parser.add_argument(
        "-d", "--destination_folder", type=str, required=True, help="目标文件夹路径"
    )
    args = parser.parse_args()

    convert_docs_to_txt(args.source_folder, args.destination_folder)
