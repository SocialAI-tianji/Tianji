import json

name_list = [
    "姐姐",
    "妹妹",
    "哥哥",
    "弟弟",
    "堂兄",
    "堂妹",
    "表哥",
    "表妹",
    "同学",
    "同事",
    "邻居",
]


def modify_json(json_file):
    # 读取 JSON 数据
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    for name in name_list:
        for item in data:
            for conversation in item["conversation"]:
                if name in conversation["input"]:
                    if "您" in conversation["output"]:
                        conversation["output"] = conversation["output"].replace(
                            "您", "你"
                        )
                    conversation["output"] = conversation["output"].replace("姐姐", "姐")
                    conversation["output"] = conversation["output"].replace("哥哥", "哥")
                    conversation["output"] = conversation["output"].replace("表哥", "哥")
                    conversation["output"] = conversation["output"].replace("表妹", "妹妹")
                    conversation["output"] = conversation["output"].replace("表弟", "弟弟")
                    conversation["output"] = conversation["output"].replace("邻居", "")
                    conversation["output"] = conversation["output"].replace("尊敬的", "")
                    conversation["output"] = conversation["output"].replace("赵大妈", "阿姨")
                    conversation["output"] = conversation["output"].replace("同事", "")
                    print(conversation["output"])

    # 将修改后的 JSON 数据写回文件
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("JSON 文件已更新！")


# 使用该函数
json_file_path = "/root/test/tianji-wishes-test.json"  # 你的 JSON 文件路径
modify_json(json_file_path)
