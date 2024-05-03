SYSTEM = '你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福'
accumulative_counts = 16
alpaca_en = dict(
    dataset=dict(
        data_files=dict(train='./tianji/tianji-wishes-chinese-v0.1.json'),
        path='json',
        type='datasets.load_dataset'),
    dataset_map_fn=None,
    max_length=2048,
    pack_to_max_length=True,
    remove_unused_columns=True,
    shuffle_before_pack=True,
    template_map_fn=dict(
        template='xtuner.utils.PROMPT_TEMPLATE.qwen_chat',
        type='xtuner.dataset.map_fns.template_map_fn_factory'),
    tokenizer=dict(
        padding_side='right',
        pretrained_model_name_or_path='./qwen/Qwen1___5-7B-Chat',
        trust_remote_code=True,
        type='transformers.AutoTokenizer.from_pretrained'),
    type='xtuner.dataset.process_hf_dataset',
    use_varlen_attn=False)
alpaca_en_path = './tianji/tianji-wishes-chinese-v0.1.json'
batch_size = 1
betas = (
    0.9,
    0.999,
)
custom_hooks = [
    dict(
        tokenizer=dict(
            padding_side='right',
            pretrained_model_name_or_path='./qwen/Qwen1___5-7B-Chat',
            trust_remote_code=True,
            type='transformers.AutoTokenizer.from_pretrained'),
        type='xtuner.engine.hooks.DatasetInfoHook'),
    dict(
        evaluation_inputs=[
            '祝姐姐生日快乐',
            '祝姐姐生日快乐，严肃风格',
            '祝姐姐生日快乐,小红书风格',
            '祝妹妹谈判顺利，小红书风格',
            '祝大家元宵节快乐',
            '祝领导春节快乐，严肃风格',
        ],
        every_n_iters=50,
        prompt_template='xtuner.utils.PROMPT_TEMPLATE.qwen_chat',
        system='你现在是一个送祝福大师，帮我针对不同人和事情、节日送对应的祝福',
        tokenizer=dict(
            padding_side='right',
            pretrained_model_name_or_path='./qwen/Qwen1___5-7B-Chat',
            trust_remote_code=True,
            type='transformers.AutoTokenizer.from_pretrained'),
        type='xtuner.engine.hooks.EvaluateChatHook'),
]
dataloader_num_workers = 0
default_hooks = dict(
    checkpoint=dict(
        by_epoch=False,
        interval=500,
        max_keep_ckpts=2,
        type='mmengine.hooks.CheckpointHook'),
    logger=dict(
        interval=10,
        log_metric_by_epoch=False,
        type='mmengine.hooks.LoggerHook'),
    param_scheduler=dict(type='mmengine.hooks.ParamSchedulerHook'),
    sampler_seed=dict(type='mmengine.hooks.DistSamplerSeedHook'),
    timer=dict(type='mmengine.hooks.IterTimerHook'))
env_cfg = dict(
    cudnn_benchmark=False,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
evaluation_freq = 50
evaluation_inputs = [
    '祝姐姐生日快乐',
    '祝姐姐生日快乐，严肃风格',
    '祝姐姐生日快乐,小红书风格',
    '祝妹妹谈判顺利，小红书风格',
    '祝大家元宵节快乐',
    '祝领导春节快乐，严肃风格',
]
launcher = 'none'
load_from = None
log_level = 'INFO'
log_processor = dict(by_epoch=False)
lr = 0.0002
max_epochs = 3
max_length = 2048
max_norm = 1
model = dict(
    llm=dict(
        pretrained_model_name_or_path='./qwen/Qwen1___5-7B-Chat',
        quantization_config=dict(
            bnb_4bit_compute_dtype='torch.float16',
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            llm_int8_has_fp16_weight=False,
            llm_int8_threshold=6.0,
            load_in_4bit=True,
            load_in_8bit=False,
            type='transformers.BitsAndBytesConfig'),
        torch_dtype='torch.float16',
        trust_remote_code=True,
        type='transformers.AutoModelForCausalLM.from_pretrained'),
    lora=dict(
        bias='none',
        lora_alpha=16,
        lora_dropout=0.1,
        r=64,
        task_type='CAUSAL_LM',
        type='peft.LoraConfig'),
    type='xtuner.model.SupervisedFinetune',
    use_varlen_attn=False)
optim_type = 'torch.optim.AdamW'
optim_wrapper = dict(
    accumulative_counts=16,
    clip_grad=dict(error_if_nonfinite=False, max_norm=1),
    dtype='float16',
    loss_scale='dynamic',
    optimizer=dict(
        betas=(
            0.9,
            0.999,
        ),
        lr=0.0002,
        type='torch.optim.AdamW',
        weight_decay=0),
    type='mmengine.optim.AmpOptimWrapper')
pack_to_max_length = True
param_scheduler = [
    dict(
        begin=0,
        by_epoch=True,
        convert_to_iter_based=True,
        end=0.09,
        start_factor=1e-05,
        type='mmengine.optim.LinearLR'),
    dict(
        begin=0.09,
        by_epoch=True,
        convert_to_iter_based=True,
        end=3,
        eta_min=0.0,
        type='mmengine.optim.CosineAnnealingLR'),
]
pretrained_model_name_or_path = './qwen/Qwen1___5-7B-Chat'
prompt_template = 'xtuner.utils.PROMPT_TEMPLATE.qwen_chat'
randomness = dict(deterministic=False, seed=None)
resume = False
save_steps = 500
save_total_limit = 2
tokenizer = dict(
    padding_side='right',
    pretrained_model_name_or_path='./qwen/Qwen1___5-7B-Chat',
    trust_remote_code=True,
    type='transformers.AutoTokenizer.from_pretrained')
train_cfg = dict(max_epochs=3, type='xtuner.engine.runner.TrainLoop')
train_dataloader = dict(
    batch_size=1,
    collate_fn=dict(
        type='xtuner.dataset.collate_fns.default_collate_fn',
        use_varlen_attn=False),
    dataset=dict(
        dataset=dict(
            data_files=dict(train='./tianji/tianji-wishes-chinese-v0.1.json'),
            path='json',
            type='datasets.load_dataset'),
        dataset_map_fn=None,
        max_length=2048,
        pack_to_max_length=True,
        remove_unused_columns=True,
        shuffle_before_pack=True,
        template_map_fn=dict(
            template='xtuner.utils.PROMPT_TEMPLATE.qwen_chat',
            type='xtuner.dataset.map_fns.template_map_fn_factory'),
        tokenizer=dict(
            padding_side='right',
            pretrained_model_name_or_path='./qwen/Qwen1___5-7B-Chat',
            trust_remote_code=True,
            type='transformers.AutoTokenizer.from_pretrained'),
        type='xtuner.dataset.process_hf_dataset',
        use_varlen_attn=False),
    num_workers=0,
    sampler=dict(shuffle=True, type='mmengine.dataset.DefaultSampler'))
use_varlen_attn = False
visualizer = None
warmup_ratio = 0.03
weight_decay = 0
work_dir = './work_dirs/qwen1_5_7b_chat_qlora_alpaca_e3'
