import re
import os
from datetime import datetime
import sys
import shutil
'''
# @author  : Shiqiding
# @description: 对prompt进行格式检查,可以将格式不对的.md文件输出带文件名为时间戳的.txt文件(作为日志),并打印出test/prompt目录下所有文件的情况
# @version : V1.0
'''
def validate_rule_template(md_file_path):
    try:
        with open(md_file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()

        # 检查是否存在以## 开头后跟汉字的标题
        if not re.search(r'^\#\#\s+[\u4e00-\u9fff]+', md_content, re.MULTILINE):
            return False, "不存在以## 开头的汉字标题"

        # 检查是否存在Prompt部分
        if not re.search(r'^\#\#\#\s+Prompt', md_content, re.MULTILINE):
            return False, "Prompt部分未识别"

        # 检查效果示例部分
        effect_examples = re.findall(r'^\#\#\#\s+效果示例', md_content, re.MULTILINE)
        for example in effect_examples:
            example_index = md_content.find(example)
            next_example_index = md_content.find('### 效果示例', example_index + 1)
            if next_example_index == -1:
                next_example_index = len(md_content)
            example_content = md_content[example_index:next_example_index]

            # 检查 Q：和 A：
            if not re.search(r'####\s+Q[：:]', example_content, re.MULTILINE) or \
               not re.search(r'####\s+A[：:]', example_content, re.MULTILINE):
                return False, "效果示例部分的 Q：或 A：未识别"

        return True, "格式正确"

    except Exception as e:
        return False, str(e)


if __name__ == '__main__':
    folder_path = r"test/prompt"  # 替换为包含规则模板的文件夹路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log_file = f"{timestamp}.txt"  # 为错误日志文件名加上时间戳

    log_folder = '.ci/log'  # 指定日志文件夹路径
    os.makedirs(log_folder, exist_ok=True)  # 创建日志文件夹，如果不存在的话

    log_file_path = os.path.join(log_folder, error_log_file)  # 构建日志文件的完整路径

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.endswith(".md") and filename != "README.md":
                    md_file_path = os.path.join(foldername, filename)
                    result, message = validate_rule_template(md_file_path)
                    if result:
                        print(f"{md_file_path}: {message}")
                    else:
                        log_file.write(f"{md_file_path} 不符合规则模板: {message}\n")
                        print(f"{md_file_path} 不符合规则模板: {message}")
                        sys.exit(1)

    # 使用 shutil.move 将日志文件移动到 .ci/log 文件夹下
    shutil.move(log_file_path, os.path.join('.ci/log', error_log_file))

    # 删除 .ci/log 下的空文件
    for file in os.listdir(log_folder):
        file_path = os.path.join(log_folder, file)
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)
            print(f"Deleted empty log file: {file}")

