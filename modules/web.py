import streamlit as st

from modules.openai_assistant import OpenAIAssistant
from modules.tools import _TOOL_DESCRIPTIONS
from utils.common import get_today


def get_response(assistant: OpenAIAssistant, prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = assistant.run_conversation(st.session_state.messages[-20:])
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    return msg


def chat_session(system_prompt: str):
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "# Tools\n"
        + "\n".join(
            [f"- {tool['function']['description']}" for tool in _TOOL_DESCRIPTIONS]
        )
    )
    st.sidebar.markdown("---")
    st.title("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": system_prompt.format(get_today()),
            },
        ]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])
        else:
            # st.sidebar.markdown(msg["content"])
            pass

    return st.chat_input()
