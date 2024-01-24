import re
import os
import sys
import argparse

'''
# author  : Shiqiding
# description: 本脚本用于CI检查prompt格式是否正确
# version : V1.0
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
    parser = argparse.ArgumentParser(description='Check Markdown file format.')
    parser.add_argument('file_path', help='Path to the Markdown file to be checked')
    args = parser.parse_args()

    flag, message = validate_rule_template(md_file_path=args.file_path)
    if flag == False:
        print("格式错误，" + message)
        sys.exit(1)
    else:
        print(message)



