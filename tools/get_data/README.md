# 简介

这里包含了各种方便使用获取数据、清理语料的工具

## Bilibili视频获取

这里介绍如何从b站单独下载和批量下载视频。

我们可以通过以下等工具：

http://zhouql.vip/bilibili

https://github.com/nICEnnnnnnnLee/BilibiliDown

https://github.com/iawia002/lux

### 使用王子周棋洛的bilidown（推荐）

直接下载 https://zhouql.vip/bilibili/pc/  即可，如果想要不安装还可以直接选择单文件下载，下载后直接按照ui可以很方便使用。

非常优美的工具，up主的对应b站：

https://space.bilibili.com/1608325226

开源仓库：

https://gitee.com/zhou-qiluo/bilibili-down

### 使用 BilibiliDown

直接下载 https://github.com/nICEnnnnnnnLee/BilibiliDown/releases/download/V6.29/BilibiliDown.v6.29.win_x64_jre11.release.zip

解压后运行 `Double-Click-to-Run-for-Win.bat`

然后输入网址批量下载即可。下载结束后直接打开文件夹可查看到已下载文件。

## 视频音频转文字

使用通义听悟

### 上传资料

访问 https://tingwu.aliyun.com/home

选择 上传音视频。这里建议你在左侧新建一个文件夹方便管理。

可以批量拖进去上传，或者关联阿里云盘。

### 管理与下载

在我的记录里，左侧你可以新建文件夹来存放不同的转录（或者开启）；

右上角找到批量，点击全选，导出即可。可以选择doc，不需要时间戳和发言人（看需求如果需要发言人可以加上）

一次导出最多12篇

## everything2txt

支持 '.pdf', '.docx', '.epub', '.md', '.rtf','.fb2' 6种文件转换到txt

使用说明详见内部 READM.md

## 批量处理jpg图片进行文字OCR后转txt

使用 batch_ocr.py ，安装 paddle-ocr后支持批量处理jpg图片进行文字OCR后转txt
