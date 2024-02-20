import os
import logging

import docx
import argparse


def argsParser():
    parser = argparse.ArgumentParser(
        description="该脚本能够将原始 .txt/.docx 转化为 .txt数据"
        "例如 `path`=liyi/ "
        "|-- liyi"
        "   |-- jingjiu"
        "       |-- *.txt"
        "       |-- ....."
        "   |-- songli"
        "       |-- *.docx"
        "       |-- ....."
        "将在 liyi/datasets 下生成处理后的 .txt 文件"
        "例如：python process_data.py \ "
        "--path liyi/"
    )
    parser.add_argument("--path", type=str, help="原始数据集目录")
    args = parser.parse_args()
    return args


log = logging.getLogger("myLogger")
log.setLevel(logging.DEBUG)

BASIC_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
formatter = logging.Formatter(BASIC_FORMAT)

chlr = logging.StreamHandler()  # console
chlr.setLevel(logging.DEBUG)
chlr.setFormatter(formatter)


log.addHandler(chlr)


def parser_docx(path):
    file = docx.Document(path)
    out = ""
    for para in file.paragraphs:
        text = para.text
        if text != "":
            out = out + text + "\n"
    return out


def parser_txt(path):
    out = ""
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                out = out + line + "\n"
    return out


if __name__ == "__main__":
    ARGS = argsParser()
    ori_data_path = ARGS.path

    data_dict = {}
    for sub_dir_name in os.listdir(ori_data_path):
        sub_dir_path = os.path.join(ori_data_path, sub_dir_name)
        data_dict.setdefault(sub_dir_path, {})
        samples = {}

        for sub_file_name in os.listdir(sub_dir_path):
            file_path = os.path.join(sub_dir_path, sub_file_name)

            sorted(file_path, reverse=True)
            if file_path.endswith(".docx"):
                samples.setdefault("docx", [])
                samples["docx"].append(sub_file_name)
            elif file_path.endswith(".txt"):
                samples.setdefault("txt", [])
                samples["txt"].append(sub_file_name)

        data_dict[sub_dir_path].setdefault("samples", samples)

    for datax, obj in data_dict.items():
        if "samples" in obj.keys():
            samples = obj["samples"]
            if "docx" in samples.keys():
                file_list = samples["docx"]
                file_list = sorted(
                    file_list, key=lambda file_path: int(file_path.split("-")[1][1:])
                )
                obj["samples"]["docx"] = file_list
            data_dict[datax] = obj

    docx_list = []
    txt_list = []
    for datax, obj in data_dict.items():
        if "samples" in obj.keys():
            samples = obj["samples"]
            if "docx" in samples.keys():
                docx_list.extend(os.path.join(datax, x) for x in samples["docx"])

            if "txt" in samples.keys():
                txt_list.extend(os.path.join(datax, x) for x in samples["txt"])

    data_dir = os.path.join(ori_data_path, "datasets")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for ind, file in enumerate(docx_list):
        out_text = parser_docx(file)
        with open(os.path.join(data_dir, f"docx_{ind}.txt"), "w") as f:
            f.write(out_text)

    for ind, file in enumerate(txt_list):
        out_text = parser_txt(file)
        with open(os.path.join(data_dir, f"txt_{ind}.txt"), "w") as f:
            f.write(out_text)
