"""
使用前先安装 pip install python-docx --upgrade

python版本为3.10

使用方法为  `python convert_docs_to_txt.py doc来源文件夹 txt目标文件夹`
"""
import os
import sys
from docx import Document


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
    if len(sys.argv) != 3:
        print("请提供当前文件夹路径和目标文件夹路径作为命令行参数。")
        print("示例: python convert_docs_to_txt.py 源文件夹路径 目标文件夹路径")
        exit()

    current_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    convert_docs_to_txt(current_folder, destination_folder)
