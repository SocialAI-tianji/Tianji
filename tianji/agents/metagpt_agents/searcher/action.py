from dotenv import load_dotenv

load_dotenv()


import json
import asyncio
from metagpt.actions import Action
from metagpt.logs import logger
from tianji.agents.metagpt_agents.utils.json_from import SharedDataSingleton
from tianji.agents.metagpt_agents.utils.agent_llm import ZhipuApi as LLMApi
from tianji.agents.metagpt_agents.utils.helper_func import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from duckduckgo_search import DDGS
import ast
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import re

"""
网络搜索助手 agent 所对应的 action。
"""


class QueryExpansion(Action):
    PROMPT_TEMPLATE: str = """
    #Role:
    - 查询扩展小助手

    ## Background:
    - 作为一个专业的查询扩展小助手。接下来，我将向你展示一段用户与大模型的历史对话记录，user 表示用户，assistant 表示大模型，你需要从中分析并生成合适的额外查询。

    ## Goals:
    - 你的任务是对历史对话记录中的内容进行分析，并且生成合适数量的额外查询，以供搜索引擎查询。

    ## Attention:
    - 我将提供给你用户目前所面对的场景，你可以自行参考，并且在此基础生成额外查询。

    ## Constraints:
    - 直接返回单个列表（例如：["额外查询一","额外查询二","额外查询三"]），不需要回复其他任何内容！

    ## Input:
    - 历史对话记录：```{instruction}```
    - 用户目前所面对的场景: ```{scene}``

    ## Workflow:
    ### Step 1: 思考生成的额外查询否需要包含场景要素（例如对象，场景，语气等细节）。
    ### Step 2: 生成查询列表并返回 "["额外查询一","额外查询二","额外查询三"]"
    """

    name: str = "queryExpansion"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()
        scene_label = sharedData.scene_label
        json_data = load_json("scene_attribute.json")
        scene, _, _ = extract_single_type_attributes_and_examples(
            json_data, scene_label
        )

        prompt = self.PROMPT_TEMPLATE.format(
            instruction=instruction,
            scene=scene,
        )

        max_retry = 5
        for attempt in range(max_retry):
            try:
                rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
                logger.info("机器人分析需求：\n" + rsp)
                rsp = (
                    rsp.replace("```list", "")
                    .replace("```", "")
                    .replace("“", '"')
                    .replace("”", '"')
                    .replace("，", ",")
                )
                sharedData.extra_query = ast.literal_eval(rsp)
                return rsp
            except:
                pass
        raise Exception("Searcher agent failed to response")


class WebSearch(Action):
    name: str = "WebSearch"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()
        queries = sharedData.extra_query
        search_results = {}

        def search(query):
            max_retry = 5
            for attempt in range(max_retry):
                try:
                    response = _call_ddgs(query)
                    return _parse_response(response)
                except Exception as e:
                    time.sleep(random.randint(2, 5))
            raise Exception(
                "Failed to get search results from DuckDuckGo after retries."
            )

        def _call_ddgs(query: str, **kwargs) -> dict:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(_async_call_ddgs(query, **kwargs))
                return response
            finally:
                loop.close()

        async def _async_call_ddgs(query: str, **kwargs) -> dict:
            ddgs = DDGS(**kwargs)
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        ddgs.text, query.strip("'"), max_results=100, safesearch="off"
                    ),  # 先返回多个网页片段，避免遇到防爬虫的网站，导致可抽取的知识过少。
                    timeout=20,
                )
                return response
            except asyncio.TimeoutError:
                raise

        def _parse_response(response: dict) -> dict:
            raw_results = []
            filtered_results = {}
            count = 0
            for item in response:
                raw_results.append(
                    (
                        item["href"],
                        item["description"] if "description" in item else item["body"],
                        item["title"],
                    )
                )
            for url, snippet, title in raw_results:
                if all(
                    domain not in url
                    for domain in ["zhihu.com", "baidu.com", "sohu.com"]  # 屏蔽掉一些防爬虫的网站。
                ) and not url.endswith(".pdf"):
                    filtered_results[count] = {
                        "url": url,
                        "summ": json.dumps(snippet, ensure_ascii=False)[1:-1],
                        "title": title,
                    }
                    count += 1
                    if (
                        count >= 7
                    ):  # 确保最多每个扩展查询返回最多20个网页的内容，可自行根据大模型的 context length 更换合适的参数。
                        break
            return filtered_results

        with ThreadPoolExecutor() as executor:
            future_to_query = {executor.submit(search, q): q for q in queries}

            for future in as_completed(future_to_query):
                try:
                    results = future.result()
                except Exception:
                    pass
                else:
                    for result in results.values():
                        if result["url"] not in search_results:
                            search_results[result["url"]] = result
                        else:
                            search_results[result["url"]][
                                "summ"
                            ] += f"\n{result['summ']}"

        search_results = {
            idx: result for idx, result in enumerate(search_results.values())
        }

        sharedData.search_results = search_results
        return ""


class SelectResult(Action):
    PROMPT_TEMPLATE: str = """
    #Role:
    - 选取网页内容小助手

    ## Background:
    - 接下来，我将向你展示一段从搜索引擎返回的内容（字典列表形式），"url"字段表示网址，"summ"表示网页的部分片段，"title"表示网页的标题。你需要分析哪一些网站可能需要进一步查询。

    ## Goals:
    - 你的任务是基于我所提供的查询列表，从中识别并筛选出哪一些网页的内容可能符合查询列表里的查询。

    ## Constraints:
    - 最多返回20个需要进一步查询的网页。
    - 你只需要返回单个列表，用索引值代表需要进一步查询的网页（例如：["0","4","6"]），不需要回复其他任何内容！。

    ## Input:
    - 搜索引擎返回的内容：```{search_results}```
    - 查询列表: ```{extra_query}``
    """

    name: str = "selectResult"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()

        prompt = self.PROMPT_TEMPLATE.format(
            search_results=sharedData.search_results,
            extra_query=sharedData.extra_query,
        )

        max_retry = 5
        for attempt in range(max_retry):
            try:
                rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
                logger.info("机器人分析需求：\n" + rsp)
                rsp = (
                    rsp.replace("```list", "")
                    .replace("```", "")
                    .replace("“", '"')
                    .replace("”", '"')
                    .replace("，", ",")
                )
                rsp = ast.literal_eval(rsp)
                sharedData.filter_weblist = [int(item) for item in rsp]
                return str(rsp)
            except:
                pass
        raise Exception("Searcher agent failed to response")


class SelectFetcher(Action):
    name: str = "selectFetcher"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()

        def fetch(url: str) -> Tuple[bool, str]:
            try:
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                html = response.content
            except requests.RequestException as e:
                return False, str(e)

            text = BeautifulSoup(html, "html.parser").get_text()
            cleaned_text = re.sub(r"\n+", "\n", text)
            if len(cleaned_text) <= 50:  # 如果网页内容少于50个字体，着判定为没有价值的，并且不加入到结果中。
                return False, "no valuable content"
            return True, cleaned_text

        with ThreadPoolExecutor() as executor:
            future_to_id = {
                executor.submit(
                    fetch, sharedData.search_results[select_id]["url"]
                ): select_id
                for select_id in sharedData.filter_weblist
                if select_id in sharedData.search_results
            }

            for future in as_completed(future_to_id):
                select_id = future_to_id[future]
                try:
                    web_success, web_content = future.result()
                except Exception:
                    pass
                else:
                    if web_success:
                        sharedData.search_results[select_id]["content"] = web_content[
                            :4096
                        ]
        return ""


class FilterSelectedResult(Action):
    PROMPT_TEMPLATE: str = """
    #Role:
    - 数据抽取小助手。

    ## Background:
    - 接下来，我将呈现一段从搜索引擎返回的内容。您的任务是尽可能提取出有潜力或有可能与查询列表里的主题直接相关或间接相关的信息,同时过滤掉所有不相关或冗余的部分。

    ## Goals:
    - 你的任务是基于我所提供的查询列表，把重要的内容提取出来。

    ## Constraints:
    - 直接返回提取后的结果，不需要回复其他任何内容！。
    - 提取的信息不可以过于概括，反之需要包含所有相关的细节。

    ## Input:
    - 搜索引擎返回的内容：```{search_results}```
    - 查询列表: ```{extra_query}``
    """

    name: str = "selectResult"

    async def run(self, instruction: str):
        sharedData = SharedDataSingleton.get_instance()

        async def ask(result, extra_query):
            prompt = self.PROMPT_TEMPLATE.format(
                search_results=result, extra_query=extra_query
            )
            rsp = await LLMApi()._aask(prompt=prompt, temperature=1.00)
            logger.info("机器人分析需求：\n" + rsp)
            return rsp

        def run_ask(result, extra_query):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(ask(result, extra_query))
                return response
            finally:
                loop.close()

        with ThreadPoolExecutor() as executor:
            future_to_id = {
                executor.submit(
                    run_ask, result["content"], sharedData.extra_query
                ): select_id
                for select_id, result in sharedData.search_results.items()
                if "content" in result
            }

            for future in as_completed(future_to_id):
                select_id = future_to_id[future]
                try:
                    result = future.result()
                except Exception as exc:
                    pass
                else:
                    sharedData.search_results[select_id]["filtered_content"] = result
        return ""
