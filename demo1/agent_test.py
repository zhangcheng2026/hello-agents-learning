from dotenv import load_dotenv
from tools.weather_tool import get_weather
from tools.attraction_tool import get_attraction
from llm_client import translate_to_chinese

load_dotenv()
city = "北京"
weather = get_weather(city)
print("天气：", weather)
print("景点：", translate_to_chinese(get_attraction(city, weather)))
