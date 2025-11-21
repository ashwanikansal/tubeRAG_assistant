from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.rag.schemas import ChatRequest, ChatResponse
from app.rag.pipeline import answer_question_for_video

app = FastAPI(title="YouTube RAG Backend")

# CORS – allow extension & localhost for dev
origins = [
    "http://localhost",
    "http://localhost:8000",
    "chrome-extension://*",  # during dev refine this to actual ID
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer_id = await answer_question_for_video(
            video_id_or_url=request.video_id_or_url,
            question=request.question,
        )
        return ChatResponse(
            answer=answer_id[0],
            video_id=answer_id[1],
        )
    except Exception as e:
        # log exception in real app
        raise HTTPException(status_code=500, detail=str(e))
