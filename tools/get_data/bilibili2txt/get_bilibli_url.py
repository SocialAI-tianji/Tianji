"""
使用说明:
    该脚本用于爬取Bilibili网站上指定关键字和页码范围内的视频信息，并将其保存为CSV文件。

    使用方法:
    python get_bilibli_url.py -k <搜索关键字> -s <起始页码> -e <结束页码> -o <输出CSV文件名>

    参数:
    -k --keyword: 搜索关键字
    -s --start_page: 起始页码
    -e --end_page: 结束页码
    -o --output: 输出CSV文件名
"""

import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Dict, Optional
import argparse


class BilibiliScraper:
    def __init__(self):
        """
        初始化BilibiliScraper类，设置基本URL和请求头。
        """
        self.base_url = "https://search.bilibili.com/all"
        self.headers = {
            "authority": "search.bilibili.com",
            "method": "GET",
            "Referer": "https://www.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

    def _get_search_results(self, keyword: str, page: int = 1) -> str:
        """
        获取指定关键字和页码的搜索结果页面的HTML内容。

        :param keyword: 搜索关键字
        :param page: 页码
        :return: 搜索结果页面的HTML内容
        """
        params = {
            "keyword": keyword,
            "from_source": "webtop_search",
            "search_source": "5",
            "page": page,
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def _parse_video_cards(self, html_content: str) -> List[BeautifulSoup]:
        """
        解析搜索结果页面的HTML内容，提取视频卡片信息。

        :param html_content: 搜索结果页面的HTML内容
        :return: 包含视频卡片的列表
        """
        soup = BeautifulSoup(html_content, "html.parser")
        video_cards = soup.find_all("div", class_="bili-video-card")
        return video_cards

    def _get_video_details(self, url: str) -> Optional[str]:
        """
        获取指定URL的视频详情页面的点击量信息。

        :param url: 视频详情页面的URL
        :return: 点击量信息（如果存在）
        """
        headers = {
            "authority": "www.bilibili.com",
            "method": "GET",
            "Referer": "https://www.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            view_count_tag = soup.find("div", class_="view-text")
            if view_count_tag:
                view_count = view_count_tag.text.strip()
                return view_count
        else:
            print("error: \n")
            print(response.text)
        return None

    def scrape_videos(
        self, keyword: str, start_page: int = 1, end_page: int = 1
    ) -> List[Dict[str, str]]:
        """
        爬取指定关键字和页码范围内的视频信息。

        :param keyword: 搜索关键字
        :param start_page: 起始页码
        :param end_page: 结束页码
        :return: 包含视频信息的列表
        """
        all_videos = []
        for page in range(start_page, end_page + 1):
            html_content = self._get_search_results(keyword, page)
            video_cards = self._parse_video_cards(html_content)

            for card in video_cards:
                link_tag = card.find("a", href=True)
                title_tag = card.find("h3", class_="bili-video-card__info--tit")
                if link_tag and title_tag:
                    sub_url = "http:" + link_tag["href"]
                    title = title_tag["title"]
                    try:
                        view_count = self._get_video_details(sub_url)
                    except:
                        print(f"now url:{sub_url} {title} error!")
                        continue
                    sub_video_info = {
                        "URL": sub_url,
                        "Title": title,
                        "View Count": view_count,
                    }
                    print(sub_video_info)
                    all_videos.append(sub_video_info)
        return all_videos

    def save_to_csv(self, videos: List[Dict[str, str]], filename: str) -> None:
        """
        将视频信息保存为CSV文件。

        :param videos: 包含视频信息的列表
        :param filename: 保存的CSV文件名
        """
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["URL", "Title", "View Count"])
            writer.writeheader()
            for video in videos:
                writer.writerow(video)


# 使用示例
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="爬取Bilibili网站上指定关键字和页码范围内的视频信息")
    parser.add_argument("-k", "--keyword", type=str, required=True, help="搜索关键字")
    parser.add_argument("-s", "--start_page", type=int, default=1, help="起始页码")
    parser.add_argument("-e", "--end_page", type=int, default=1, help="结束页码")
    parser.add_argument(
        "-o", "--output", type=str, default="./bilibili_videos.csv", help="输出CSV文件名"
    )
    args = parser.parse_args()

    scraper = BilibiliScraper()
    videos = scraper.scrape_videos(args.keyword, args.start_page, args.end_page)
    scraper.save_to_csv(videos, args.output)
    print(f"Saved {len(videos)} videos to '{args.output}'")
