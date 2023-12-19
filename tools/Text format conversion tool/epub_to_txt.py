import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text.append(soup.get_text())

    return '\n'.join(text)


epub_path = 'xxxxxxx.epub'  # epub文件所在位置
text = epub_to_text(epub_path)

# 将文本保存到与 EPUB 文件同名但扩展名为 .txt 的文件中
txt_filename = os.path.splitext(epub_path)[0] + '.txt'
with open(txt_filename, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"EPUB 已转换为txt并命名为 {txt_filename}.")
