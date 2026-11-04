"""工具 1：通过 wttr.in 查询指定城市的实时天气。"""

from urllib.parse import quote
import requests

def get_weather(city: str) -> str:
    """查询天气并返回易读的中文文本。"""
    url = f"https://wttr.in/{quote(city)}?format=j1"
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "demo1-travel-agent/1.0"})
        response.raise_for_status()
        current = response.json()["current_condition"][0]
        description = current["weatherDesc"][0]["value"]
        temperature = current["temp_C"]
        return f"{city}当前天气：{description}，气温 {temperature}°C"
    except requests.RequestException as exc:
        return f"天气查询失败：{exc}"
    except (KeyError, IndexError, ValueError) as exc:
        return f"天气数据解析失败，请检查城市名称：{exc}"


# data = get_weather("吉隆坡")
# print(data)