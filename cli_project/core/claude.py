from typing import Any, cast

from anthropic import Anthropic
from anthropic.types import Message, MessageParam, ToolParam


class Claude:
    def __init__(self, model: str):
        self.client = Anthropic()
        self.model = model

    def add_user_message(self, messages: list[MessageParam], message: Message | str | list[Any]) -> None:
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(cast(MessageParam, user_message))

    def add_assistant_message(self, messages: list[MessageParam], message: Message | str) -> None:
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(cast(MessageParam, assistant_message))

    def text_from_message(self, message: Message) -> str:
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )

    def chat(
        self,
        messages: list[MessageParam],
        system: str | None = None,
        temperature: float = 1.0,
        stop_sequences: list[str] | None = None,
        tools: list[ToolParam] | None = None,
        thinking: bool = False,
        thinking_budget: int = 1024,
    ) -> Message:
        if stop_sequences is None:
            stop_sequences = []

        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message: Message = self.client.messages.create(**params)  # type: ignore[call-overload]
        return message
