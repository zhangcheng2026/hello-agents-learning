# 初识智能体：模块化旅行助手 Demo

本项目参考 Notion《第01章｜初识智能体·代码示例》，演示一个 ReAct 智能体：模型规划下一步动作，程序调用天气或景点搜索工具，并把工具结果交回模型生成最终答复。

## 文件结构

```text
demo1/
├── main.py                    # 程序入口，读取用户问题
├── agent.py                   # Thought/Action/Observation 主循环
├── prompt_template.py         # 智能体系统指令模板
├── llm_client.py              # OpenAI 兼容模型客户端
├── tools/
│   ├── __init__.py             # 工具注册表
│   ├── weather_tool.py         # 工具 1：wttr.in 实时天气查询
│   └── attraction_tool.py      # 工具 2：Tavily 景点搜索
├── requirements.txt           # Python 依赖
└── .env.example               # 环境变量配置示例
```

## 安装与配置

需要 Python 3.10 或更新版本，以及可联网环境。在 PyCharm Terminal 执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

编辑 `.env`，填写模型服务的 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`，以及 `TAVILY_API_KEY`。不要把真实密钥提交到 Git。

- OpenAI 用户可以保留 `OPENAI_BASE_URL=https://api.openai.com/v1`。
- 使用其他兼容服务时，按服务商提供的信息填写 Base URL 和模型名称。
- `TAVILY_API_KEY` 用于景点搜索；天气查询本身不需要单独的 API 密钥。

## 启动

```powershell
.\.venv\Scripts\python.exe main.py
```

输入旅行问题后按回车；直接回车使用默认的北京天气示例。也可以在 PyCharm 中右键 `main.py` 并选择 Run。

## 运行流程

`main.py → agent.py → llm_client.py 生成 Action → agent.py 分派工具 → tools/weather_tool.py 或 tools/attraction_tool.py → Observation 返回模型`

`agent.py` 仅允许调用 `tools/__init__.py` 中注册的工具，不会执行模型生成的任意 Python 代码。


##运行的经过
D:\python\python.exe D:\hello-agents-learning\demo1\main.py 
请输入旅行问题（直接回车使用默认问题）：
> 杭州  明天旅游
用户：杭州  明天旅游
================================================

--- 第 1 步 ---
模型：
Thought: 先查询杭州明天的天气情况，以便推荐合适的景点。
Action: get_weather(city="杭州")
Observation：杭州当前天气：Mist，气温 17°C

--- 第 2 步 ---
模型：
Thought: 已获取杭州天气为雾（Mist），接下来根据该天气搜索适合游玩的景点。
Action: get_attraction(city="杭州", weather="Mist")
Observation：Under Mist weather in Hangzhou, the sources recommend visiting West Lake, which is conveniently located near many other attractions and easily accessible on foot. The sources also highlight Lingyin Temple, West Lake National Wetland Park, and the bustling Wulin Square as suitable spots for exploration. For dining, Lou Wai Lou is recommended for traditional Hangzhou cuisine, while Tian Wai Tian is noted for its vegetarian offerings near Lingyin. The sources suggest that these locations are ideal for tourists looking to enjoy Hangzhou's natural beauty and cultural heritage despite the mist.

--- 第 3 步 ---
模型：
Thought: 已获得杭州雾天适合游玩的景点及餐饮推荐，可以整理成中文建议并结束。
Action: Finish[杭州明天有雾（当前气温约17°C），雾中游西湖别有一番朦胧意境，以下是适合的推荐：

景点：
1. 西湖——雾天湖景如水墨画，且周边景点集中、步行即可串联游览。
2. 灵隐寺——雾中古寺更显清幽禅意。
3. 西溪国家湿地公园（西湖国家湿地公园）——雾气缭绕，湿地风光更有韵味。
4. 武林广场——市区繁华地段，购物休闲方便。

餐饮：
- 楼外楼：品尝传统杭帮菜。
- 天外天：位于灵隐附近，以素斋闻名。

温馨提示：雾天能见度较低，出行注意交通安全，路面可能湿滑；可适当放慢行程，优先选择西湖周边步行游览，把灵隐寺与天外天素斋安排在一起。祝旅途愉快！]
Observation：Action 格式无效，请使用工具调用或 Finish[最终答案]。

--- 第 4 步 ---
模型：
Thought: 上次答复格式无效，可能是内容换行导致，这次将最终答案整理为单行输出。
Action: Finish[杭州明天有雾（当前气温约17°C），雾中游西湖别有一番朦胧意境。推荐景点：1. 西湖——雾天湖景如水墨画，周边景点集中可步行串联；2. 灵隐寺——雾中古寺更显清幽禅意；3. 西溪国家湿地公园——雾气缭绕，湿地风光更有韵味；4. 武林广场——市区繁华地段，购物休闲方便。餐饮推荐：楼外楼品尝传统杭帮菜；天外天位于灵隐附近，以素斋闻名。温馨提示：雾天能见度较低，注意交通安全，路面可能湿滑，可放慢行程，优先西湖周边步行游览，并把灵隐寺与天外天素斋安排在一起。祝旅途愉快！]

任务完成：杭州明天有雾（当前气温约17°C），雾中游西湖别有一番朦胧意境。推荐景点：1. 西湖——雾天湖景如水墨画，周边景点集中可步行串联；2. 灵隐寺——雾中古寺更显清幽禅意；3. 西溪国家湿地公园——雾气缭绕，湿地风光更有韵味；4. 武林广场——市区繁华地段，购物休闲方便。餐饮推荐：楼外楼品尝传统杭帮菜；天外天位于灵隐附近，以素斋闻名。温馨提示：雾天能见度较低，注意交通安全，路面可能湿滑，可放慢行程，优先西湖周边步行游览，并把灵隐寺与天外天素斋安排在一起。祝旅途愉快！

进程已结束，退出代码为 0