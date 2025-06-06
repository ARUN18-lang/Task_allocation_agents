from langchain_nvidia_ai_endpoints import ChatNVIDIA
from Agents.utils import get_nvidia_api_key

def get_model():
    llm = ChatNVIDIA(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        api_key=get_nvidia_api_key(),
        base_url="https://integrate.api.nvidia.com/v1",
        max_tokens=10000
    )
    return llm
