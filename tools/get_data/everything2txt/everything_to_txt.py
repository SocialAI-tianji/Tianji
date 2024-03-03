import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2
import docx
from striprtf.striprtf import rtf_to_text

'''
# @author  : Shiqiding
# @description: 本脚本目前支持 '.pdf', '.docx', '.epub', '.md', '.rtf','.fb2' 6种文件转换到txt
# @version : V1.0

1.python版本为3.9
2.使用前请运行以下命令 pip install -r requirements.txt去安装对应的包
3.执行脚本前先确定文件目录input_directory和output_directory的位置，并将文件导入到input_directory目录中
4.之后使用 py .\everything_to_txt.py执行脚本

'''
# 文件输入输出目录
input_directory = 'example'
output_directory = 'output'
def process_file(file_path, output_directory):
    # Identify the file format by its extension and call the appropriate conversion function
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension in ['.pdf', '.docx', '.epub', '.md', '.rtf','.fb2']:  # Add other formats as needed
        text = convert_to_txt(file_path)
        save_text_to_file(file_path, text, output_directory)
    else:
        print(f"Unsupported file format for file: {file_path}")

def save_text_to_file(original_file_path, text, output_directory):
    if text is not None:
        txt_filename = os.path.splitext(os.path.basename(original_file_path))[0] + '.txt'
        output_file_path = os.path.join(output_directory, txt_filename)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"File has been converted and saved as {output_file_path}.")
    else:
        print(f"Failed to convert file: {original_file_path}")

def convert_to_txt(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return pdf_to_txt(file_path)
    elif file_extension == '.docx':
        return docx_to_txt(file_path)
    elif file_extension == '.epub':
        return epub_to_txt(file_path)
    elif file_extension == '.md':
        return md_to_txt(file_path)
    elif file_extension == '.rtf':
        return rtf_to_txt(file_path)
    elif file_extension == '.fb2':
        return fb2_to_txt(file_path)
    else:
        print(f"不支持文件格式: {file_extension}")
        return None

def pdf_to_txt(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = [page.extract_text() for page in reader.pages]
    return '\n'.join(text)

def docx_to_txt(docx_path):
    doc = docx.Document(docx_path)
    text = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(text)

def epub_to_txt(epub_path):
    book = epub.read_epub(epub_path)
    text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text.append(soup.get_text())
    return '\n'.join(text)

def md_to_txt(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        text = file.readlines()
    return ''.join(text)

def rtf_to_txt(rtf_path):
    with open(rtf_path, 'r', encoding='utf-8') as file:
        rtf_content = file.read()
    text = rtf_to_text(rtf_content)
    return text

def fb2_to_txt(fb2_path):
    with open(fb2_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
        text = soup.get_text()
    return text

def process_files_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path):
            process_file(file_path, output_directory)

process_files_in_directory(input_directory, output_directory)

