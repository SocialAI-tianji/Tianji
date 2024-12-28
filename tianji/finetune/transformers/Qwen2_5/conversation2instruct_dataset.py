"""
用于将对话格式的数据转换为指令格式的数据集。
将conversation格式的JSON文件转换为instruction-input-output格式。

原始JSON格式示例:
{
    "conversation": [
        {
            "input": "写一段关于春天的文字",
            "output": "半山映入晨光时，便算是醒了。五月的黎明，是最温柔的。隔着纱帘都能闻见木槿的清香，伴着叮当的风铃声，仿佛整个世界都在等待一场美好的相遇。"
        }
    ]
}

转换后的JSON格式示例:
[
    {
        "instruction": "写一段关于春天的文字",
        "input": "",
        "output": "半山映入晨光时，便算是醒了。五月的黎明，是最温柔的。隔着纱帘都能闻见木槿的清香，伴着叮当的风铃声，仿佛整个世界都在等待一场美好的相遇。"
    }
]
"""

def transform_json(original_data):
    transformed_data = []
    
    for item in original_data:
        if "conversation" not in item:
            continue
            
        for conv in item["conversation"]:
            # 跳过没有必要的数据
            if not all(key in conv for key in ["input", "output"]):
                continue
                
            # 创建新的数据结构
            new_item = {
                "instruction": conv["input"],
                "input": "",  # 设置为空字符串
                "output": conv["output"]
            }
            
            transformed_data.append(new_item)
            
    return transformed_data

def convert_conversation_to_instruct(input_path, output_path):
    # 读取原始JSON文件
    with open(input_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    # 转换数据
    transformed_data = transform_json(original_data)

    # 保存转换后的JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=4)

# 使用示例：
import json

if __name__ == "__main__":
    input_path = "/path/to/original.json"
    output_path = "/path/to/transformed.json"
    convert_conversation_to_instruct(input_path=input_path, output_path=output_path)