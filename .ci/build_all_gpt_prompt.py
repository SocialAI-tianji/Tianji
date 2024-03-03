import os
import json
'''
# @author  : Shiqiding
# @description: 本脚本支持合并gpt_prompt
# @version : V1.0

'''
# 指定要合并的JSON文件所在文件夹路径
#folder_path = r'C:\Users\yhd\PycharmProjects\TianjiOrignal\tianji\prompt\gpt_prompt'
folder_path = os.environ.get('gpt_folder_path')
# 指定要保存合并后JSON文件的路径
#output_json_path = r'C:\Users\yhd\PycharmProjects\TianjiOrignal\tianji\prompt\gpt_prompt\all_gpt_prompt.json'
output_json_path = os.environ.get('gpt_output_json_path')
# 初始化一个空的JSON列表，用于存储所有JSON数据
merged_data = []

# 定义一个递归函数来遍历文件夹及其子文件夹下的所有JSON文件
def merge_json_files(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                json_file_path = os.path.join(root, filename)
                with open(json_file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    merged_data.extend(json_data)

# 清空 output_json_path 文件中的所有文本内容并写入一个空的 JSON 数组
with open(output_json_path, 'w', encoding='utf-8') as output_file:
    output_file.write('[]')

# 调用递归函数以遍历文件夹及其子文件夹下的所有JSON文件
merge_json_files(folder_path)



# 将合并后的数据保存到新的JSON文件中
with open(output_json_path, 'w', encoding='utf-8') as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print(f'合并完成，合并后的JSON文件已保存至: {output_json_path}')

