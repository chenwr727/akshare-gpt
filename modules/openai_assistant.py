import json
from typing import List

from openai import OpenAI

from utils.log import logger

from .tools import dispatch_tool, get_tools


class OpenAIAssistant:
    def __init__(self, api_key: str, base_url: str, model: str):
        """
        Initialize the OpenAI Assistant with an API key and base URL.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def run_conversation(self, messages: List[dict]):
        """
        Run a conversation using the OpenAI API, supporting tool calls.

        :param messages: List of message dictionaries as per OpenAI API spec.
        :param model: Optional model name to override the default.
        :return: Content of the final response message.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=get_tools(),
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.extend([response_message])
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                logger.info(
                    f"function_name: {function_name}, function_args: {function_args}"
                )
                function_response = dispatch_tool(function_name, function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            logger.debug(f"messages: {messages}")
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return second_response.choices[0].message.content
        else:
            return response_message.content
