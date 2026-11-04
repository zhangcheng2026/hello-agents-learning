"""工具 2：通过 Tavily 搜索适合当前天气的旅游景点。"""

import os

from tavily import TavilyClient


def get_attraction(city: str, weather: str) -> str:
    """搜索景点建议；密钥从 TAVILY_API_KEY 环境变量读取。"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "未配置 TAVILY_API_KEY。请在 .env 文件中填写 Tavily API 密钥。"

    try:
        client = TavilyClient(api_key=api_key)
        result = client.search(
            query=f"{city} 在{weather}天气下适合游览的旅游景点及推荐理由",
            search_depth="basic",
            include_answer=True,
        )
        if result.get("answer"):
            return result["answer"]
        snippets = [
            f"- {item.get('title', '搜索结果')}: {item.get('content', '')}"
            for item in result.get("results", [])
        ]
        return "根据搜索结果：\n" + "\n".join(snippets) if snippets else "没有找到相关景点信息。"
    except Exception as exc:
        return f"景点搜索失败：{exc}"
