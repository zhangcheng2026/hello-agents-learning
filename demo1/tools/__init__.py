"""注册智能体可以调用的工具。"""

from tools.attraction_tool import get_attraction
from tools.weather_tool import get_weather

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}
