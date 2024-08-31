import os
from paddleocr import PaddleOCR

"""
# @author  : Shiqiding
# @description: 批量处理jpg图片进行文字OCR后转txt
# @version : V1.0

1.python版本为3.9
2.使用前请 pip install paddlepaddle 并 pip install paddleocr
3.执行前请把文件夹路径directory_path转换为图片所在的文件夹路径(可以是多层文件夹，如果是多层，请输入最上层的路径）
4. py batch_ocr.py执行脚本
"""
# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# 替换为您的图片文件夹路径
directory_path = "C:\\Users\\yhd\\Desktop\\XHS_Spyder\\datas_search"


def process_image(img_path):
    """处理单个图片并将结果保存到文本文件中"""
    try:
        result = ocr.ocr(img_path, cls=True)
        if result is not None:
            # 提取文本
            txts = [line[1][0] for line in result[0]]
            # 创建输出文件路径
            output_file_path = os.path.splitext(img_path)[0] + ".txt"
            # 将文本写入文件
            with open(output_file_path, "w", encoding="utf-8") as file:
                for text in txts:
                    file.write(text + "\n")
            print(f"文本已成功写入到 {output_file_path}")
        else:
            print(f"未能从 {img_path} 中提取文本。")
    except Exception as e:
        print(f"处理图片 {img_path} 时出现错误: {e}")


def process_directory(directory):
    """遍历并处理目录及其所有子目录下的.jpg图片"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".jpg"):
                img_path = os.path.join(root, file)
                process_image(img_path)


process_directory(directory_path)
