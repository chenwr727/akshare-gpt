import streamlit as st

from modules.config import load_config
from modules.openai_assistant import OpenAIAssistant
from modules.web import chat_session, get_response
from utils.log import logger

st.set_page_config(
    page_title="ChatGPT Assistant",
    page_icon="🤖",
    # layout="wide",
    initial_sidebar_state="expanded",
)

openai_config = load_config()["openai"]
assistant = OpenAIAssistant(
    openai_config["api_key"], openai_config["base_url"], openai_config["model"]
)

prompt = chat_session(openai_config["system_prompt"])
if prompt:
    logger.info(f"prompt: {prompt}")
    msg = get_response(assistant, prompt)
    logger.info(f"response: {msg}")
