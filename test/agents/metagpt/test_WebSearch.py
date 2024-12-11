"""
Tavily AI is the leading search engine optimized for LLMs 
https://app.tavily.com/  
"""
import os
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

response = tavily_client.search("What is the weather in Shanghai?",max_results=10)

for url in response['results']:
    print(url['url'])
