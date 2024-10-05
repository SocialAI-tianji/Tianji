"""
使用说明：
该脚本用于将指定文件夹中的所有mp3文件转录为文本文件，并保存为md格式。

使用前请确保：
1. 已安装faster_whisper库
2. 已配置好CUDA环境
3. 设置好输入文件夹(input_folder)和输出文件夹(output_folder)路径

使用方法：
1. 设置input_folder为包含mp3文件的文件夹路径
2. 设置output_folder为保存转录结果的文件夹路径
3. 运行脚本

注意事项：
- 脚本会自动跳过已存在的输出文件，避免重复转录
"""

from faster_whisper import WhisperModel
import os
from tqdm import tqdm

input_folder = ""  # 请在此处设置输入文件夹路径
output_folder = ""  # 请在此处设置输出文件夹路径
model_size = "large-v2"  # 或使用 "large-v3"

model = WhisperModel(model_size, device="cuda", compute_type="bfloat16")

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有mp3文件
for filename in tqdm(os.listdir(input_folder)):
    if filename.endswith(".mp3"):
        input_file_path = os.path.join(input_folder, filename)
        output_file_name = f"{os.path.splitext(filename)[0]}.md"
        output_file_path = os.path.join(output_folder, output_file_name)

        # 检查输出文件是否已存在
        if os.path.exists(output_file_path):
            print(f"文件 {output_file_name} 已存在，跳过转录。")
            continue

        # 进行转录
        try:
            segments, info = model.transcribe(
                input_file_path,
                beam_size=5,
                language="zh",
                condition_on_previous_text=False,
            )
            full_text = ", ".join(segment.text for segment in segments)

            # 保存转录结果到输出文件
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(full_text)

            print(f"已保存转录结果到 {output_file_name}")
        except Exception as e:
            print(f"转录文件 {input_file_path} 时出错: {e}")
