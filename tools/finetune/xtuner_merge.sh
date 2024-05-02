HF_OUTPUT_DIR="./hf"
MERGE_OUTPUT_DIR="./merge"
SCRIPT_PATH="./internlm2_chat_7b_qlora_oasst1_e3_copy.py" 
SRC_MODEL_PATH="/home/model_temp/Shanghai_AI_Laboratory/internlm2-chat-7b"
WEIGHTS_PATH="/home/finetune/work_dirs/internlm2_chat_7b_qlora_oasst1_e3_copy/iter_291.pth"

rm -rf $HF_OUTPUT_DIR
rm -rf $MERGE_OUTPUT_DIR
mkdir -p $HF_OUTPUT_DIR
mkdir -p $MERGE_OUTPUT_DIR

xtuner convert pth_to_hf "${SCRIPT_PATH}" "${WEIGHTS_PATH}" "${HF_OUTPUT_DIR}"
xtuner convert merge \
    "${SRC_MODEL_PATH}" \
    "${HF_OUTPUT_DIR}" \
    "${MERGE_OUTPUT_DIR}" \
    --max-shard-size "2GB"