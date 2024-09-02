"""
使用说明:
    该脚本用于创建一个简单的 Gradio 界面，用于浏览、删除和查看指定文件夹中的 Markdown 文件, 你也可以直接让大模型帮忙 review.

    使用方法:
    python 3-data_check_gradio.py -f <文件夹路径>

    参数:
    -f --folder_path: 指定 Markdown 文件所在的文件夹路径。
"""

import gradio as gr
import os
import glob
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser(description="指定 Markdown 文件所在的文件夹")
parser.add_argument(
    "-f", "--folder_path", type=str, default="audio_md_full", help="Markdown 文件夹路径"
)
args = parser.parse_args()

# 获取文件夹中所有 .md 文件的路径
md_files = glob.glob(os.path.join(args.folder_path, "*.md"))
current_index = 0


def read_md_file(index):
    if 0 <= index < len(md_files):
        with open(md_files[index], "r", encoding="utf-8") as file:
            content = file.read()
        return content
    return "没有更多文件。"


def next_md():
    global current_index
    current_index += 1
    if current_index >= len(md_files):
        current_index = 0  # 如果到达最后一个文件，则循环到第一个文件
    return (
        read_md_file(current_index),
        md_files[current_index],
        current_index,
        remaining_files_count(),
    )


def prev_md():
    global current_index
    current_index -= 1
    if current_index < 0:
        current_index = len(md_files) - 1  # 如果到达第一个文件，则循环到最后一个文件
    return (
        read_md_file(current_index),
        md_files[current_index],
        current_index,
        remaining_files_count(),
    )


def delete_md():
    global current_index
    if 0 <= current_index < len(md_files):
        os.remove(md_files[current_index])
        del md_files[current_index]
        if current_index >= len(md_files):
            current_index = 0  # 如果删除的是最后一个文件，则调整索引
        return (
            read_md_file(current_index),
            md_files[current_index] if md_files else "没有更多文件。",
            current_index,
            remaining_files_count(),
        )
    return "没有更多文件。", "", -1, 0


def show_current_md():
    return (
        read_md_file(current_index),
        md_files[current_index],
        current_index,
        remaining_files_count(),
    )


def remaining_files_count():
    return len(md_files)


# 创建 Gradio 界面
with gr.Blocks() as demo:
    with gr.Row():
        prev_button = gr.Button("上一页")
        next_button = gr.Button("下一页")
        delete_button = gr.Button("删除")
    md_display = gr.Markdown(value=show_current_md()[0], elem_id="md_display")
    file_name_display = gr.Textbox(
        value=md_files[current_index], label="当前文件", interactive=False
    )
    index_display = gr.Textbox(
        value=str(current_index), label="当前索引", interactive=False
    )
    count_display = gr.Textbox(
        value=str(remaining_files_count()), label="剩余文件数量", interactive=False
    )

    prev_button.click(
        fn=prev_md,
        outputs=[md_display, file_name_display, index_display, count_display],
    )
    next_button.click(
        fn=next_md,
        outputs=[md_display, file_name_display, index_display, count_display],
    )
    delete_button.click(
        fn=delete_md,
        outputs=[md_display, file_name_display, index_display, count_display],
    )

# 固定 Markdown 显示框的大小
demo.css = """
#md_display {
    height: 400px;
    overflow: auto;
    resize: none;
}
"""

# 启动 Gradio 应用程序
demo.launch()
