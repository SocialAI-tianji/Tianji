# This Python file uses the following encoding: utf-8
import json
import re
import os
'''
# @author  : Shiqiding
# @description: 本脚本支持将批量将.md写的规定prompt格式转换为规定格式的json
# @version : V2.0

promptpath为.md格式的prompt路径，具体格式参考仓库里的prompt格式部分

输出的json例子如下：
[
    {
        "id": 4,
        "name": "对长辈",
        "test_system": "你现在是一个精通言语表达、热爱他人、尊重长辈、富有文采的中国晚辈，今天是一个节日，你要去面见亲朋好友，请针对不同对象、不同节日，不同场合，准备见面问好的话术表达节日的问候。下面我将给出节日和见面对象及场合的具体信息，请你根据这些信息，以我的角度准备问候语，字数30字以内。要求：简洁、简短、真诚、有趣、礼貌，尝试藏头诗、顺口溜等多种趣味形式，请加入俏皮话，有趣的内容来增加趣味性。信息为：对象：_____，对象特点：______，节日：_____，场合：_____。请写3条供我选择。\n用户输入\n对象：_____，对象特点：______，节日：_____，场合：_____。\n### 效果示例",
        "example": [
            {
                "input": "对象：英语老师，对象特点：活泼开朗，新潮，爱开玩笑，节日：教师节，场合：庆祝教师节联欢会。",
                "output": "亲爱的英语老师，教师节到了，感谢您的教诲，您的课堂永远充满活力和笑声！\n超酷英语老师，教师节快乐！您的课堂总是妙趣横生，让我们深受启发。\n敬爱的老师，教师节到了，感谢您不仅教英语，还教我们快乐和幽默。愿您天天开\n\n### 效果示例"
            },
            {
                "input": "对象：妈妈；对象特点：温柔体贴，热心肠；节日：母亲节，场合：母亲节当天。",
                "output": "亲爱的妈妈，母亲节快乐！您的温柔和热心让我们感受到无尽的爱和关怀。\n慈爱的妈妈，母亲节到啦！谢谢您一直以来的疼爱，您是我生命中最伟大的女神！\n亲爱的妈妈，母亲节当天，祝您幸福满满，像您一样温柔体贴的人，值得所有的爱和祝福。"
            }
        ]
    }
]

id： prompt所属大类
name:子标题
test_system:prompt内容
input:用户输入
output:对应输出

'''
folder_path = os.environ.get('folder_path')
#folder_path = r"C:\Users\yhd\PycharmProjects\Tianji\test\prompt\yiyan_prompt"  # 替换成您的文件夹路径
output_path=os.environ.get('output_path')

def md_file_to_json_with_examples(file_path,id,heading):
    """
    从给定的文件路径读取Markdown文件，并按指定格式将其内容转换为JSON格式。
    此版本处理同一提示中的多个Q&A对，并将它们分组到“example”下。

    参数：
    file_path（str）：Markdown文件的路径。

    返回：
    json_object（str）：JSON格式的字符串。
    """
    if(heading==""):
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()

        blocks = re.split(r'###\s+Prompt\s*[:：]?\s*\n', md_content, flags=re.IGNORECASE)

        blocks = blocks[1:]
        json_list = []

        for block in blocks:
            test_system_part = block.split('#### Q：')[0].strip()

            qa_pairs = re.findall(r'#### Q：(.*?)#### A：(.*?)(?=#### Q：|$)', block, re.DOTALL)
            if (qa_pairs == []):
                qa_pairs = re.findall(r'#### Q:(.*?)#### A:(.*?)(?=#### Q:|$)', block, re.DOTALL)

            examples = []
            for qa_pair in qa_pairs:
                input_text = qa_pair[0].strip()
                output_text = qa_pair[1].strip()

                example_obj = {
                    "id":id,
                    "name":"无标题",
                    "input": input_text,
                    "output": output_text
                }
                examples.append(example_obj)

            json_obj = {
                # "name":name,
                "test_system": test_system_part,
                "example": examples
            }
            json_list.append(json_obj)

        return json.dumps(json_list, indent=4, ensure_ascii=False)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()

        pattern = rf'\n(?={re.escape(heading)} [^\#\n]+)'
        sections = re.split(pattern, md_content)

        json_list = []

        for section in sections:

            pattern = rf'{re.escape(heading)}\s*(.*?)\s*\n'
            title_match = re.match(pattern, section)
            section_title = title_match.group(1).strip() if title_match else "无标题"

            # 提取该部分的内容
            section_content = section[len(title_match.group(0)):] if title_match else section
            blocks = re.split(r'###\s+Prompt\s*[:：]?\s*\n', section_content,flags=re.IGNORECASE)

            blocks = blocks[1:]

            for block in blocks:

                test_system_part = block.split('#### Q：')[0].strip()
                test_system_part= re.sub(r'#.*', '', test_system_part)
                qa_pairs = re.findall(r'#### Q：(.*?)#### A：(.*?)(?=#### Q：|$)', block, re.DOTALL)
                if (qa_pairs == []):
                    qa_pairs = re.findall(r'#### Q:(.*?)#### A:(.*?)(?=#### Q:|$)', block, re.DOTALL)

                examples = []
                for qa_pair in qa_pairs:

                    input_text = qa_pair[0].strip()
                    input_text=re.sub(r'#.*', '', input_text)
                    output_text = qa_pair[1].strip()
                    output_text= re.sub(r'#.*', '', output_text)

                    example_obj = {
                        "input": input_text,
                        "output": output_text
                    }
                    examples.append(example_obj)

                json_obj = {
                    "id":id,
                    "name":section_title,
                    "system_prompt": test_system_part,
                    "example": examples
                }
                json_list.append(json_obj)

        return json.dumps(json_list, indent=4, ensure_ascii=False)


def replace_english_colons_with_chinese(md_file_path):

    try:

        with open(md_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()


        file_contents = re.sub(r':', '：', file_contents)


        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write(file_contents)

    except Exception as e:
        print(f"发生错误：{str(e)}")
    return md_file_path

def find_first_heading(md_file_path):
    # 打开并读取Markdown文件
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    match = re.search(r'^\s*(#{1,2})(?!\#)\s', content, re.MULTILINE)

    if match:
        return '#' * len(match.group(1))
    else:
        return ""


if __name__ == '__main__':

    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(".md"):
                if filename == "README.md":
                    continue
                promptpath=os.path.join(foldername, filename)
                filepath =replace_english_colons_with_chinese(promptpath)
                print(filepath)
                heading = find_first_heading(filepath)
                print("此文档的heading使用的是 "+heading)
                filename=os.path.basename(filepath)
                id =int(filename[:2])
                print("处理文档为 " + filename+" 该文档属于第"+str(id)+"大类")
                json_output = md_file_to_json_with_examples(filepath,id=id,heading=heading)
                input_dir, input_file = os.path.split(promptpath)
                input_file_base, _ = os.path.splitext(input_file)

                #output_path = r"C:\Users\yhd\PycharmProjects\Tianji\tianji\prompt"

                # 使用正则表达式提取所需路径
                match = re.search(r'/prompt(.*)/[^/]+$', promptpath)
                if match:
                    # 提取的路径
                    extracted_path = match.group(1)
                    # 构造最终路径
                    json_file_output_path = output_path + extracted_path + "/"
                else:
                    json_file_output_path = "无法匹配路径"
                json_file_output = os.path.join(json_file_output_path, input_file_base + ".json")
                with open(json_file_output, 'w', encoding='utf-8') as file:
                    json.dump(json.loads(json_output), file, ensure_ascii=False, indent=4)
                print(json_output)