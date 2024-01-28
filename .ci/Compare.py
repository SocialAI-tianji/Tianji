# This Python file uses the following encoding: utf-8
import os
import datetime
import sys

'''
# @author  : Shiqiding
# @description: 拿到最近的两个error_log,对比是否有差异，差异的部分即为增量，如果其中有不符合规则模板的，则打印出来(目前还是滞后判断)
# @version : V1.0
'''
def get_closest_files(directory):
    now = datetime.datetime.now()
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    files.sort(key=lambda x: abs(now - datetime.datetime.strptime(x.split('.')[0], '%Y%m%d_%H%M%S')))
    return files[:2] if len(files) >= 2 else files

def read_file(directory, filename):
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
        return file.readlines()


def compare_files(directory, file1, file2):
    content1 = read_file(directory, file1)
    content2 = read_file(directory, file2)

    # 比较文件的行数
    len1, len2 = len(content1), len(content2)
    if len1 > len2:
        # 如果第一个文件行数更多，打印多出的行
        return ''.join(content1[len2:])
    elif len2 > len1:
        # 如果第二个文件行数更多，打印多出的行
        return ''.join(content2[len1:])
    else:
        # 行数相同
        return "两个文件的行数相同，没有多余的行。"


directory = r'.ci'  # 替换为你的文件夹路径
closest_files = get_closest_files(directory)
if __name__ == '__main__':
    if len(closest_files) == 2:
        difference = compare_files(directory, closest_files[0], closest_files[1])

        # 检查difference中是否包含特定字样
        if "不符合规则模板" in difference:
            print(difference)
        else:
            print("比较结果中没有发现不符合规则模板的字样。")
    else:
        print("没有足够的文件进行比较。")



