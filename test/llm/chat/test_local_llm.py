# 参考文档
# https://huggingface.co/docs/transformers/index

from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from dotenv import load_dotenv
from tianji import TIANJI_PATH

load_dotenv(dotenv_path=TIANJI_PATH)

device = "cuda"  # the device to load the model onto

# 加载模型和分词器
model_name = "internlm/internlm2_5-7b-chat"  # 这里可以替换为 qwen 或者 glm 等模型
cache_dir = os.path.join(TIANJI_PATH, "temp", "local_llm")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
    load_in_4bit=True,
    cache_dir=cache_dir,
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(
    model_name, cache_dir=cache_dir, trust_remote_code=True
)

# 准备输入
prompt = "你好，请介绍下你自己"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt},
]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

# 生成响应
generated_ids = model.generate(
    model_inputs.input_ids, max_new_tokens=50, max_length=8096
)
generated_ids = [
    output_ids[len(input_ids) :]
    for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)
