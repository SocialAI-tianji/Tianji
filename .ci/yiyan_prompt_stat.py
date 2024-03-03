import json
import matplotlib.pyplot as plt
import os
import shutil
'''
# @author  : Shiqiding
# @description: 统计yiyan prompt
# @version : V1.0

'''
all_yiyan_json_path = os.environ.get('all_yiyan_json')
#all_yiyan_json_path=r'C:\Users\yhd\PycharmProjects\TianjiOrignal\tianji\prompt\yiyan_prompt\all_yiyan_prompt.json'
# 打开 JSON 文本文件并加载数据
with open(all_yiyan_json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 统计不同 ID 下的 JSON 个数
id_counts = {}
for item in data:
    id = item.get("id")
    if id in id_counts:
        id_counts[id] += 1
    else:
        id_counts[id] = 1

# 提取 ID 和对应的计数
ids = list(id_counts.keys())
counts = list(id_counts.values())

# 将 ID 转换为横坐标标签
labels = []
for id in ids:
    if id == 1:
        labels.append("Etiquette")
    elif id == 2:
        labels.append("Hospitality")
    elif id == 3:
        labels.append("Gifting")
    elif id == 4:
        labels.append("Wishes")
    elif id == 5:
        labels.append("Communication")
    elif id == 6:
        labels.append("Awkwardness")
    elif id == 7:
        labels.append("Conflict")
    else:
        labels.append(str(id))

# 将 ID 转换为整数索引
id_indices = list(range(len(ids)))



# 绘制柱状图
plt.bar(id_indices, counts)
plt.xlabel('Category')  # 修改横坐标标签
plt.ylabel('Number of valid prompts')

# 旋转横坐标标签，以避免重叠
plt.xticks(id_indices, labels, rotation=45, ha='right')

# 在每个柱状图上标识数字
for i, count in enumerate(counts):
    plt.text(id_indices[i], count, str(count), ha='center', va='bottom')

plt.title('yiyan prompt statistics')

# 保存为 PNG 图片文件
plt.savefig('yiyan_prompt_statistics.png', bbox_inches='tight')

shutil.move('yiyan_prompt_statistics.png', '.ci/yiyan_prompt_statistics.png')

# 显示图形
plt.show()