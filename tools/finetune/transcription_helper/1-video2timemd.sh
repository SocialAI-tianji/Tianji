#!/bin/bash

# 需要提前安装好 autocut https://github.com/mli/autocut
# 将所有视频转为的mp3文件进行转录（直接对mp4等视频文件操作也可）
for file in ./audio/*.mp3; do
    if [ -f "$file" ]; then
        # 调用 autocut 命令处理每个文件
        autocut --lang zh --whisper-model large-v2 -t "$file"
    fi
done

