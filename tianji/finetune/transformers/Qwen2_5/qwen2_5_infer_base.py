"""
测试运行微调后的送祝福大模型
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from tianji import TIANJI_PATH
import os
from modelscope import snapshot_download

# download model 根据显卡情况选择，推荐使用 7b 或 14b 模型
download_path = os.path.join(TIANJI_PATH, "temp","tianji-wish2")
snapshot_download("sanbuphy/tianji-wish2-3b", cache_dir=download_path)

mode_path = os.path.join(download_path, "sanbuphy", "tianji-wish2-3b")

tokenizer = AutoTokenizer.from_pretrained(mode_path)
model = AutoModelForCausalLM.from_pretrained(mode_path, device_map="auto",torch_dtype=torch.bfloat16, trust_remote_code=True).eval()

# 定义不同风格的祝福语测试样例
test_cases = [
    {
        "prompt": "祝姐姐生日快乐，放飞自我风格",
        "description": "放飞自我风格的生日祝福"
    },
    {
        "prompt": "祝哥哥圣诞快乐，祝福长文风格", 
        "description": "长文风格的圣诞祝福"
    },
    {
        "prompt": "祝爷爷春节快乐，诗词赋风格",
        "description": "诗词赋风格的春节祝福"
    }
]

# 统一的系统提示语
system_prompt = "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"

# 统一的生成参数配置
gen_kwargs = {
    "max_length": 2500,
    "do_sample": True,
    "top_k": 1,
    "temperature": 0.7
}

# 遍历测试样例生成祝福语
for case in test_cases:
    print(f"\n===== 测试 {case['description']} =====")
    print(f"输入提示: {case['prompt']}\n")
    
    inputs = tokenizer.apply_chat_template(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case['prompt']}
        ],
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True
    ).to('cuda')
    
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"模型回复:\n{response}\n")
        print("="*50)