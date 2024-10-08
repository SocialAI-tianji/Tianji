"""
使用说明:
    该脚本用于对输入的 JSON 文件内容 kmeans 进行聚类，并将聚类结果保存到指定目录中。

    使用方法:
    python jsonknowledges_kmeans.py -i <输入JSON文件路径> -o <输出目录路径> [-c]

    参数:
    -i --input: 指定输入的 JSON 文件路径。
    -o --output: 指定保存聚类结果的目录路径。
    -c --contour: 开启轮廓聚类，否则使用原始聚类方法。
"""

import json
import os
import re
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
import argparse
from tianji import TIANJI_PATH
import numpy as np


def find_best_k(embeddings, k_min=2, k_max=10):
    """
    使用轮廓系数选择最佳的聚类数 k
    """
    best_k = k_min
    best_score = -1
    for k in range(k_min, k_max + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        score = silhouette_score(embeddings, labels)
        print(f"k={k}, Silhouette Score={score:.4f}")
        if score > best_score:
            best_score = score
            best_k = k
    print(f"最佳聚类数 k={best_k}，对应的 Silhouette Score={best_score:.4f}")
    return best_k


def main(input_file, output_dir, use_contour):
    # 读取整个文件内容
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 尝试解析整个文件为 JSON 对象
    try:
        json_data = json.loads(content)
        if isinstance(json_data, dict):
            json_data = [json_data]
    except json.JSONDecodeError:
        # 如果解析失败，使用正则表达式来匹配每个 JSON 对象
        json_objects = re.findall(r"\{.*?\}", content, re.DOTALL)
        json_data = []
        for obj in json_objects:
            try:
                json_data.append(json.loads(obj))
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON object: {e}")

    # 提取所有文本内容
    # 保留整个 JSON 对象
    documents = json_data

    # 使用 SentenceTransformer 模型生成句子嵌入
    model = SentenceTransformer(
        "BAAI/bge-large-zh-v1.5",
        cache_folder=os.path.join(TIANJI_PATH, "temp", "embedding_model"),
    )
    # 提取每个 JSON 的第一个 value 用于生成嵌入
    embeddings = model.encode(
        [entry[next(iter(entry))] for entry in documents if entry],
        normalize_embeddings=True,
    )

    if use_contour:
        # 找到最佳的 k 值
        best_k = find_best_k(embeddings, k_min=6, k_max=10)
    else:
        best_k = 12  # 使用固定聚类数，推荐 6 或者 10 ，根据实际情况调整

    # K-Means 聚类
    km = KMeans(n_clusters=best_k, random_state=42)
    km.fit(embeddings)

    # 获取聚类结果
    clusters = km.labels_.tolist()

    # 将结果保存到不同的 JSON 文件中
    for cluster_num in range(best_k):
        cluster_items = [
            documents[i] for i in range(len(documents)) if clusters[i] == cluster_num
        ]

        # 计算相似度并重新排序
        if cluster_items:
            cluster_embeddings = embeddings[np.array(clusters) == cluster_num]
            similarity_matrix = np.dot(cluster_embeddings, cluster_embeddings.T)
            sorted_indices = np.argsort(-similarity_matrix.sum(axis=1))  # 按照相似度降序排序
            cluster_items = [cluster_items[i] for i in sorted_indices]

        # 使用第一个 JSON 对象的标题作为文件名
        if cluster_items:
            title = list(cluster_items[0].keys())[0]  # 获取第一个 JSON 对象的标题
            # 为避免文件名重复或非法，添加聚类编号
            filename = os.path.join(output_dir, f"cluster_{cluster_num+1}_{title}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(cluster_items, f, ensure_ascii=False, indent=4)
            print(f'Cluster "{title}" saved to {filename}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster JSON values")
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the input JSON file"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Directory to save the clustered JSON files",
    )
    parser.add_argument(
        "-c", "--contour", action="store_true", help="Enable contour clustering"
    )
    args = parser.parse_args()

    # 确保输出目录存在
    os.makedirs(args.output, exist_ok=True)

    main(args.input, args.output, args.contour)
