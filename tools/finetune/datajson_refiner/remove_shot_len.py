import json


def clean_short_len_data(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    filtered_data = []
    for conversation_group in data:
        keep_conversation = True  # 假设这个conversation_group是有效的
        for conversation in conversation_group["conversation"]:
            if len(conversation["output"]) < 10:  # 小于这个长度的都是无效输出，删除
                print(conversation["output"])
                keep_conversation = False
                break
        if keep_conversation:
            filtered_data.append(conversation_group)
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(filtered_data, file, indent=4, ensure_ascii=False)


output_file_path = "/root/test/tianji-wishes-test.json"

clean_short_len_data(output_file_path)
