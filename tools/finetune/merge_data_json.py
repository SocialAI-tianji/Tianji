import os
import json

"""
本脚本用于合并 merge `get_wish_datas.py` 文件产生的多份数据 json 文件
"""

def extract_and_merge_conversations(folder_path, output_file):
    all_conversations = []

    # 遍历指定文件夹
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # 打开并读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 提取需要的字段
                for item in data:
                    for conversation in item['conversation']:
                        extracted = {
                            'system': conversation['system'],
                            'input': conversation['input'],
                            'output': conversation['output']
                        }
                        # 将每个对话包装在一个 'conversation' 键中，并作为独立对象加入列表
                        all_conversations.append({'conversation': [extracted]})

    # 将合并后的所有对话数据写入一个新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_conversations, file, ensure_ascii=False, indent=4)


# 使用示例
folder_path = 'tianji_wishes_datasets_new'  # 要扫描的文件夹路径
output_file = 'tianji_wishes_datasets_new.json'     # 输出文件的名称和路径
extract_and_merge_conversations(folder_path, output_file)