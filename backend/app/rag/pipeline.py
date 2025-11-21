from typing import List
from langchain_core.messages import BaseMessage

from app.rag.youtube_client import extract_video_id, fetch_transcript_text
from app.rag.text_splitting import split_text_to_documents
from app.rag.vector_store import get_or_create_vector_store, get_retriever, get_vector_store
from app.rag.prompting import get_default_prompt
from app.rag.llm_client import get_llm


class TranscriptNotFoundError(Exception):
    ...


async def build_index_for_video(video_id_or_url: str) -> str:
    """
    Ensures that a vector store exists for the given video.
    Returns the normalized video_id.
    """
    video_id = extract_video_id(video_id_or_url)

    # if we already have a vector store, don't rebuild anything
    try:
        get_vector_store(video_id)
        return video_id
    except KeyError:
        pass
    
    # else build everything
    # 1. Fetch transcript
    transcript = fetch_transcript_text(video_id)
    if not transcript:
        raise TranscriptNotFoundError(
            f"No transcript available for video {video_id}"
        )

    # 2. Split into Documents
    docs = split_text_to_documents(transcript)

    # 3. Build or reuse vector store
    get_or_create_vector_store(video_id, docs)

    return video_id


async def answer_question_for_video(
    video_id_or_url: str,
    question: str,
    k: int = 5,
) -> List[str]:
    """
    High-level RAG call for FastAPI route:
    - ensures index exists
    - retrieves top-k chunks
    - calls LLM with context+question
    """
    video_id = await build_index_for_video(video_id_or_url)

    # 1. Get retriever for this video's vector store

    vector_store = get_vector_store(video_id)
    retriever = get_retriever(vector_store, k=k)

    # 2. Retrieve relevant documents
    docs = retriever.invoke(question)

    if not docs:
        # no relevant docs -> let LLM say it doesn't know
        context_text = ""
    else:
        context_text = "\n\n".join(doc.page_content for doc in docs)

    # 3. Build final prompt
    prompt = get_default_prompt()
    final_prompt = prompt.invoke({"context": context_text, "question": question})

    # 4. Call LLM
    llm = get_llm()
    print("Generating final response...")
    result: BaseMessage = llm.invoke(final_prompt)

    # `result` is a ChatMessage; .content has the text
    return [result.content, video_id]


# testing
# import asyncio

# async def main():
#     answer = await answer_question_for_video(
#         "https://www.youtube.com/watch?v=DNBaUCCST3I",
#         "Difference between agentic ai and gen ai?"
#     )
#     print(answer)

# asyncio.run(main())

