import json
import random


def add_holiday_greetings_to_input(json_file):
    scenes = ["生日", "春节", "元宵节", "端午节", "七夕节", "中秋节", "重阳节", "除夕", "腊八节", "周年纪念"]

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        for conversation in item["conversation"]:
            for scene in scenes:
                if scene in conversation["input"]:
                    role = conversation["input"].split(scene)[0][1:]
                    if "," not in conversation["input"]:
                        # print(conversation['input'],role)
                        prefix_list = [
                            f"我想祝{role}{scene}快乐",
                            f"我想给{role}{scene}祝福",
                            f"我想送{role}{scene}祝福",
                            f"送祝福给{role} {scene}",
                            f"我想祝福{role}{scene}快乐",
                            f"祝{role}{scene}快乐",
                            f"送祝福给{role}{scene}",
                            f"祝福{role}{scene}快乐",
                        ]
                        input_result = random.choice(prefix_list)
                        conversation["input"] = input_result
                        continue
                        # print(input_result)
                        # if '风格' in conversation['input']:
                        #     style = conversation['input'].split(',')[1]
                        #     prefix_list = [f'我想祝{role}{scene}快乐',
                        #                    f'我想给{role}{scene}祝福',
                        #                    f'我想送{role}{scene}祝福',
                        #                    f'送祝福给{role} {scene}',
                        #                    f'我想祝福{role}{scene}快乐',
                        #                    f'祝{role}{scene}快乐',
                        #                    f'送祝福给{role}{scene}',
                        #                    f'祝福{role}{scene}快乐',
                        #                    f'祝福{role}{scene}',
                        #                    ]
                        #     input_result = random.choice(prefix_list) + ',' + style
                        #     conversation['input'] = input_result
                        #     # print(input_result)
                        continue
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("JSON 文件已更新，特定节日表达input！")


# 使用该函数
json_file_path = "/root/test/tianji-wishes-test.json"  # 你的 JSON 文件路径
add_holiday_greetings_to_input(json_file_path)
