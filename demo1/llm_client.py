"""OpenAI 兼容模型客户端。"""

import os

from openai import OpenAI

from prompt_template import AGENT_SYSTEM_PROMPT


class OpenAICompatibleClient:
    """调用 OpenAI 或其他兼容 Chat Completions API 的模型服务。"""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL")
        if not api_key:
            raise ValueError("缺少 OPENAI_API_KEY。请复制 .env.example 为 .env 并填写模型服务密钥。")
        if not self.model:
            raise ValueError("缺少 OPENAI_MODEL。请在 .env 文件中填写模型名称。")
        self.client = OpenAI(api_key=api_key, base_url=self.base_url)

    def generate(self, history: list[dict[str, str]]) -> str:
        """根据对话历史生成下一步 Thought/Action。"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": AGENT_SYSTEM_PROMPT}, *history],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""


def translate_to_chinese(text: str) -> str:
    """使用已配置的模型把文本翻译为简体中文。"""
    llm = OpenAICompatibleClient()
    response = llm.client.chat.completions.create(
        model=llm.model,
        messages=[
            {"role": "system", "content": "请将用户提供的内容准确翻译成简体中文，只输出译文。"},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or text
