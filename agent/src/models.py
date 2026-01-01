from langchain_groq.chat_models import ChatGroq

GROQ_MODEL = ChatGroq(
    model="qwen/qwen3-32b",
    reasoning_effort=None,
    max_tokens=200,
)