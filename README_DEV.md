# TubeRAG Assistant – Developer Documentation

TubeRAG Assistant is a Chrome extension paired with a FastAPI backend that enables AI-powered chat about YouTube videos using RAG (Retrieval Augmented Generation).

This README explains project structure, setup steps, development flow, and how everything works internally.

## 🚀 1. Project Overview

This project consists of **two main components**:

**A. Chrome Extension**
* Injects a chat UI on YouTube video pages.
* Extracts current video ID from the URL.
* Sends the video ID + user questions to backend.
* Displays answers using a clean AI chat interface.
* Handles:
    * Local chat history per video
    * SPA URL navigation (YouTube’s dynamic routing)
    * Dynamic panel creation via extension icon click

**B. FastAPI Backend**
* Receives requests from extension.
* Extracts transcript using YouTube API (English only).
* Performs RAG pipeline:
    * Chunk transcript
    * Embed chunks
    * Store embeddings (in-memory vector store)
    * Retrieve relevant chunks
    * Query LLM (HuggingFace API)
* Returns final answer.

## 🔧 2. Backend Setup

**Install dependencies**
```bash
cd backend
pip install -r app/requirements.txt
```
**Set environment variables**
```bash
HF_API_KEY="your_huggingface_api_key"
```
**Run server**
```bash
uvicorn app.main:app --reload --port 8000
```
Backend will now run at:
```
http://localhost:8000
```
**API Endpoint**
|Endpoint |	Method | Description
|---|---|---|
|/api/chat | POST | Main RAG endpoint


## 🧠 3. RAG Pipeline 
**1. Video Identification**
* Extract video ID from URL or raw ID
* Validate video link and normalize input
* Used: **custom ID extractor**

**2. Transcript Retrieval**
* Fetch English transcript from YouTube
* Handle “no subtitles” / disabled cases
* Used: **youtube_transcript_api()**

**3. Chunking**
* Split transcript into overlapping segments
* Preserve context for retrieval
* Used: **LangChain RecursiveCharacterTextSplitter()**

**4. Embeddings**
* Convert chunks into 768-dim vectors
* Represent meaning for semantic search
* Used: **HuggingFace SentenceTransformer**

**5. Vector Indexing**
* Store all embeddings in FAISS
* Build searchable vector database per video
* Used: **LangChain + FAISS**

**6. Retrieval**
* Embed user question
* Find top-k relevant transcript chunks
* Used: **FAISS retriever (k=5)**

**7. Prompt Construction**
* Combine retrieved text + question
* Enforce “answer only from context” rule
* Used: **LangChain PromptTemplate()**

**8. Answer Generation**
* Generate grounded response via LLM
* Deterministic, low-temperature outputs
* Used: **HuggingFace Endpoint (Llama 3.1 8B)**

**9. Response Delivery**
* Send answer back to extension
* Save per-video chat history
* Used: **FastAPI JSON response**

## 🧩 4. Chrome Extension Setup
**Load Unpacked Extension**
1. Open:
*chrome://extensions*
2. Enable Developer Mode
3. Click Load Unpacked
4. Select the extension/ folder.

**Important Files**

*manifest.json*
* Permissions
* Background service worker

*background.js*
* Handles backend communication
* Sends TOGGLE_CHAT_PANEL to content script on icon click

*popup.js*
* Injects chat UI
* Handles:
    * Chat rendering
    * Loader animation
    * History storage
    * URL change detection (SPA)

*popup.css*
* UI styling

## 🔄 5. Full Flow Summary

**YouTube Page → Popup Script → Background → FastAPI → LLM → Back → Panel**
1. User opens YouTube video.
1. User clicks extension icon.
1. Chatwindow will open with historic chats(if available).
1. User enters question.
1. popup.js → background.js (via runtime.sendMessage).
1. background.js → backend (POST /api/chat).
1. Backend runs RAG pipeline.
1. background.js receives response.
1. Popup script displays formatted answer.