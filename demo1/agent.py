"""智能体运行循环：询问模型、解析 Action、调用工具、记录 Observation。"""

import ast
import re
from typing import Any

from llm_client import OpenAICompatibleClient
from tools import AVAILABLE_TOOLS


def parse_action(text: str) -> str | None:
    """从模型输出中取出 Action 字段。"""
    match = re.search(r"^\s*Action\s*:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _run_tool_action(action: str) -> str:
    """解析并运行注册过的工具调用，不执行任意 Python 代码。"""
    call_match = re.fullmatch(r"(\w+)\((.*)\)", action)
    if not call_match:
        return "Action 格式无效，请使用工具调用或 Finish[最终答案]。"

    tool_name, args_source = call_match.groups()
    tool = AVAILABLE_TOOLS.get(tool_name)
    if tool is None:
        return f"未定义的工具：{tool_name}"

    try:
        parsed = ast.parse(f"f({args_source})", mode="eval").body
        kwargs: dict[str, Any] = {}
        for keyword in parsed.keywords:
            if (
                keyword.arg is None
                or not isinstance(keyword.value, ast.Constant)
                or not isinstance(keyword.value.value, str)
            ):
                raise ValueError("工具参数必须是普通字符串")
            kwargs[keyword.arg] = keyword.value.value
        return tool(**kwargs)
    except (SyntaxError, TypeError, ValueError) as exc:
        return f"工具调用参数无效：{exc}"


def run_agent(user_prompt: str, max_steps: int = 6) -> None:
    """执行 ReAct 循环，直到模型返回 Finish 或达到步数上限。"""
    try:
        llm = OpenAICompatibleClient()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    history = [{"role": "user", "content": user_prompt}]
    print(f"用户：{user_prompt}\n{'=' * 48}")

    for step in range(1, max_steps + 1):
        print(f"\n--- 第 {step} 步 ---")
        try:
            output = llm.generate(history)
        except Exception as exc:
            raise SystemExit(f"调用模型失败：{exc}") from exc

        print(f"模型：\n{output}")
        history.append({"role": "assistant", "content": output})
        action = parse_action(output)
        if action is None:
            observation = "未找到 Action 字段，请按要求重新输出一组 Thought 和 Action。"
        elif action.startswith("Finish[") and action.endswith("]"):
            print(f"\n任务完成：{action[len('Finish['):-1]}")
            return
        else:
            observation = _run_tool_action(action)

        print(f"Observation：{observation}")
        history.append({"role": "user", "content": f"Observation: {observation}"})

    print(f"\n已达到最大步数（{max_steps}），请缩短问题或稍后重试。")
