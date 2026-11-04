"""程序入口：加载环境配置并启动旅行助手。"""

from dotenv import load_dotenv

from agent import run_agent


def main() -> None:
    load_dotenv()
    prompt = input("请输入旅行问题（直接回车使用默认问题）：\n> ").strip()
    if not prompt:
        prompt = "你好，请查询一下今天北京的天气，并根据天气推荐一个合适的旅游景点。"
    run_agent(prompt)

if __name__ == "__main__":
    main()
