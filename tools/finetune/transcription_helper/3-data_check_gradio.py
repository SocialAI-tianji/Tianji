import gradio as gr
import os
import glob

# 指定 Markdown 文件所在的文件夹
folder_path = "audio_md_full"

# 获取文件夹中所有 .md 文件的路径
md_files = glob.glob(os.path.join(folder_path, "*.md"))
current_index = 0

def read_md_file(index):
    if 0 <= index < len(md_files):
        with open(md_files[index], 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    return "No more files."

def next_md():
    global current_index
    current_index += 1
    if current_index >= len(md_files):
        current_index = 0  # 如果到达最后一个文件，则循环到第一个文件
    return read_md_file(current_index), md_files[current_index], current_index

def prev_md():
    global current_index
    current_index -= 1
    if current_index < 0:
        current_index = len(md_files) - 1  # 如果到达第一个文件，则循环到最后一个文件
    return read_md_file(current_index), md_files[current_index], current_index

def delete_md():
    global current_index
    if 0 <= current_index < len(md_files):
        os.remove(md_files[current_index])
        del md_files[current_index]
        if current_index >= len(md_files):
            current_index = 0  # 如果删除的是最后一个文件，则调整索引
        return read_md_file(current_index), md_files[current_index] if md_files else "No more files", current_index
    return "No more files.", "", -1

def show_current_md():
    return read_md_file(current_index), md_files[current_index], current_index

# 创建 Gradio 界面
with gr.Blocks() as demo:
    with gr.Row():
        prev_button = gr.Button("Previous")
        next_button = gr.Button("Next")
        delete_button = gr.Button("Delete")
    md_display = gr.Markdown(value=show_current_md()[0], elem_id="md_display")
    file_name_display = gr.Textbox(value=md_files[current_index], label="Current File", interactive=False)
    index_display = gr.Textbox(value=str(current_index), label="Current Index", interactive=False)

    prev_button.click(fn=prev_md, outputs=[md_display, file_name_display, index_display])
    next_button.click(fn=next_md, outputs=[md_display, file_name_display, index_display])
    delete_button.click(fn=delete_md, outputs=[md_display, file_name_display, index_display])

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