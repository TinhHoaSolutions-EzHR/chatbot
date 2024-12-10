# from llama_index.core.llms import ChatMessage, ChatResponse
# from llama_index.core.agent import ReActAgent
# from llama_index.core.tools.function_tool import FunctionTool
# from llama_index.core.tools.types import BaseTool
# from llama_index.core.prompts.base import ChatPromptTemplate
# from llama_index.core.types import MessageRole
# from llama_index.llms.openai import OpenAI
# from typing import List, Any
# from app.models.tool import Tool
# class LLMTool:
#     @staticmethod
#     def summarize():
#         pass
# class RetrievalAgent:
#     def __init__(self, tools: List[Tool], chat_history: List[ChatMessage] = None, model: Any = None):
#         func_tools = []
#         for tool in tools:
#             fn = getattr(LLMTool, tool.name)
#             func_tools.append(FunctionTool.from_defaults(fn=fn))
#         self._chat_history = chat_history
#         if not chat_history:
#             messages: List[ChatMessage] = [
#                 ChatMessage(
#                     role=MessageRole.SYSTEM,
#                     content=("You are an assisant to perform the user input."),
#                 ),
#                 ChatMessage(
#                     role=MessageRole.USER,
#                     content=("{input}"),
#                 ),
#             ]
#             self._chat_prompt_template = ChatPromptTemplate(messages)
#         else:
#             self._chat_prompt_template = ChatPromptTemplate(chat_history)
#     def __call__(self, input: str):
#         messages = self._chat_prompt_template.format_messages(input=input)
#         chat_response = OpenAI().chat()
