# 该脚本用于将指定文件夹中的所有 mp3 文件进行转录，使用 autocut 工具处理音频文件。
# 使用方法:
# bash 1-video2timemd.sh
# 注意事项:
# - 需要提前安装好 autocut，安装链接：https://github.com/mli/autocut
# - 本脚本会处理 ./audio/ 文件夹中的所有 mp3 文件，也可以直接对 mp4 等视频文件进行操作。

for file in ./audio/*.mp3; do
    if [ -f "$file" ]; then
        # 调用 autocut 命令处理每个文件
        autocut --lang zh --whisper-model large-v2 -t "$file"
    fi
done
