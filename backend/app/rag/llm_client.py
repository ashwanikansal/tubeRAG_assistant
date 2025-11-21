from functools import lru_cache
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def get_llm() -> ChatHuggingFace:
    """
    Returns a singleton chat model configured with your HF endpoint.
    HF_API_TOKEN should be in env for auth.
    """
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2,
        do_sample=False,
        repetition_penalty=1.03,
    )

    return ChatHuggingFace(llm=llm)
