"""
这个脚本用于对模型进行LoRA微调训练。
主要功能:
1. 加载祝福语数据集并进行预处理
2. 配置和加载模型
3. 应用LoRA进行参数高效微调
4. 训练模型生成个性化的祝福语
"""

from datasets import Dataset
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer
)
from modelscope import snapshot_download, AutoModel
import torch
from peft import LoraConfig, TaskType, get_peft_model
import os
from datetime import datetime

# =========================
# 路径配置部分
# =========================
PATH_CONFIG = {
    "json_input": "/home/merged.json",                        # 数据集JSON文件路径
    "model_cache_dir": "/home/temp",                           # 模型下载缓存目录
    "model_repo": "qwen/Qwen2.5-14B-Instruct",                  # 此处可指定任意模型仓库名称,自动下载缓存至缓存目录
    
    "training_output_base_dir": "/home/output",                # 基础训练输出目录
    "training_job_name": "Qwen2.5_instruct_lora",             # 训练任务名称
}

# =========================
# 动态生成带时间戳的训练输出目录
# =========================
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
training_output_dir = os.path.join(
    PATH_CONFIG["training_output_base_dir"],
    f"{PATH_CONFIG['training_job_name']}_{PATH_CONFIG['model_repo']}_{current_datetime}"
)

# 如果需要，可以创建目录（Trainer 会自动创建，但提前创建可以避免权限问题）
os.makedirs(training_output_dir, exist_ok=True)

# =========================
# 数据准备部分
# =========================
# 检查输入文件是否存在
if not os.path.exists(PATH_CONFIG["json_input"]):
    raise FileNotFoundError(f"输入的JSON文件不存在: {PATH_CONFIG['json_input']}")

# 将JSON文件转换为CSV文件
df = pd.read_json(PATH_CONFIG["json_input"])
ds = Dataset.from_pandas(df)
print("数据样本:", ds[:3])

# =========================
# 模型和分词器加载部分
# =========================
# 获取模型版本，默认使用 "master"
model_revision = PATH_CONFIG.get("model_revision", "master")

# 下载模型
model_dir = snapshot_download(
    PATH_CONFIG["model_repo"],
    cache_dir=PATH_CONFIG["model_cache_dir"],
    revision=model_revision
)

# 自动生成 MODEL_PATH
MODEL_PATH = model_dir  # snapshot_download 返回的是下载后模型的路径

print(f"模型已下载到: {MODEL_PATH}")

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    use_fast=False,
    trust_remote_code=True
)

# =========================
# 数据处理函数
# =========================
def process_func(example):
    MAX_LENGTH = 1024  # Llama分词器会将一个中文字切分为多个token，因此需要放开一些最大长度，保证数据的完整性
    instruction = tokenizer(
        f"<|im_start|>system\n你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福<|im_end|>\n"
        f"<|im_start|>user\n{example['instruction'] + example['input']}<|im_end|>\n"
        f"<|im_start|>assistant\n",
        add_special_tokens=False
    )
    response = tokenizer(
        f"{example['output']}",
        add_special_tokens=False
    )
    input_ids = instruction["input_ids"] + response["input_ids"] + [tokenizer.pad_token_id]
    attention_mask = instruction["attention_mask"] + response["attention_mask"] + [1]  # eos token也要关注
    labels = [-100] * len(instruction["input_ids"]) + response["input_ids"] + [tokenizer.pad_token_id]
    
    # 截断处理
    if len(input_ids) > MAX_LENGTH:
        input_ids = input_ids[:MAX_LENGTH]
        attention_mask = attention_mask[:MAX_LENGTH]
        labels = labels[:MAX_LENGTH]
    
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels
    }

# 应用数据处理函数
tokenized_id = ds.map(process_func, remove_columns=ds.column_names)

# 示例解码
print("示例解码 (input_ids):", tokenizer.decode(tokenized_id[0]['input_ids']))
print("示例解码 (labels):", tokenizer.decode([x for x in tokenized_id[1]["labels"] if x != -100]))

# =========================
# 模型加载和配置部分
# =========================
# 加载模型
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16
)

# 启用梯度检查点
model.enable_input_require_grads()
print(f"Model dtype: {model.dtype}")

# 配置LoRA
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=False,  # 训练模式
    r=32,                  # LoRA秩
    lora_alpha=16,         # LoRA alpha
    lora_dropout=0.1       # Dropout比例
)

# 应用LoRA配置
model = get_peft_model(model, config)
model.print_trainable_parameters()

# =========================
# 训练配置和执行部分
# =========================
# 设置训练参数，使用动态生成的训练输出目录
args = TrainingArguments(
    output_dir=training_output_dir,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    logging_steps=10,
    num_train_epochs=3,
    save_steps=100, 
    learning_rate=1e-4,
    save_on_each_node=True,
    gradient_checkpointing=True
)

# 初始化Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_id,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True),
)

# 开始训练
trainer.train()

print(f"训练完成，输出保存在: {training_output_dir}")