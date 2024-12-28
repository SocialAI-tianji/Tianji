"""
用于将训练好的LoRA权重合并到原始模型中并保存完整模型。
将LoRA模型与基础模型合并,生成一个完整的模型用于部署。
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel

mode_path = "/home/temp/qwen/Qwen2___5-14B-Instruct"
lora_path = '/home/output/Qwen2.5_instruct_lora_qwen/Qwen2.5-14B-Instruct_20241222_194654/checkpoint-612' # 这里改称你的 lora 输出对应 checkpoint 地址
save_dir = "/home/tianji-wish2-14b"

tokenizer = AutoTokenizer.from_pretrained(mode_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(mode_path, device_map="auto",torch_dtype=torch.bfloat16, trust_remote_code=True).eval()
model = PeftModel.from_pretrained(model, model_id=lora_path)
model = model.merge_and_unload()
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print("保存成功！") 