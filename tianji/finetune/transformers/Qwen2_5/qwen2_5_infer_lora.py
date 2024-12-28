"""
用于测试Qwen2.5模型的LoRA微调效果。
通过不同风格的祝福语生成来验证模型的生成能力。
包括:放飞自我、长文、诗词赋、白话、文言文、文艺等多种风格。
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel

mode_path = "/home/temp/qwen/Qwen2___5-14B-Instruct"
lora_path = '/home/output/Qwen2.5_instruct_lora_qwen/Qwen2.5-14B-Instruct_20241222_194654/checkpoint-612' # 这里改称你的 lora 输出对应 checkpoint 地址

# 加载tokenizer
tokenizer = AutoTokenizer.from_pretrained(mode_path, trust_remote_code=True)

# 加载模型
model = AutoModelForCausalLM.from_pretrained(mode_path, device_map="auto",torch_dtype=torch.bfloat16, trust_remote_code=True).eval()

# 加载lora权重
model = PeftModel.from_pretrained(model, model_id=lora_path)

prompt = "祝姐姐生日快乐，放飞自我风格"
inputs = tokenizer.apply_chat_template([{"role": "system", "content": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"},{"role": "user", "content": prompt}],
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       ).to('cuda')
gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1, "temperature":0.8}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


prompt = "祝哥哥圣诞快乐，祝福长文风格"
inputs = tokenizer.apply_chat_template([{"role": "system", "content": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"},{"role": "user", "content": prompt}],
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       ).to('cuda')
gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1, "temperature":0.8}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

prompt = "祝爷爷春节快乐，诗词赋风格"
inputs = tokenizer.apply_chat_template([{"role": "system", "content": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"},{"role": "user", "content": prompt}],
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       ).to('cuda')
gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1, "temperature":0.8}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


prompt = "祝朋友中秋快乐，白话风格"
inputs = tokenizer.apply_chat_template([{"role": "system", "content": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"},{"role": "user", "content": prompt}],
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       ).to('cuda')
gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1, "temperature":0.8}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


prompt = "祝领导春节快乐，文言文风格"
inputs = tokenizer.apply_chat_template([{"role": "system", "content": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"},{"role": "user", "content": prompt}],
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       ).to('cuda')
gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1, "temperature":0.8}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))



prompt = "祝朋友新年快乐，文艺风格"
inputs = tokenizer.apply_chat_template([{"role": "system", "content": "你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福"},{"role": "user", "content": prompt}],
                                       add_generation_prompt=True,
                                       tokenize=True,
                                       return_tensors="pt",
                                       return_dict=True
                                       ).to('cuda')
gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1, "temperature":0.8}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))