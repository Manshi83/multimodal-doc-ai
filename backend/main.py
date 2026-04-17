from fastapi import FastAPI, File, UploadFile, HTTPException

from backend.ingestion.pdf_loader import extract_text
from backend.chunking.chunker import chunk_text
from backend.embeddings.embedder import get_embeddings, model
from backend.summarizer.summarizer import summarize
from backend.chatbot.rag import build_index, query_rag

app = FastAPI(title="PDF Chatbot API")


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    try:
        file_bytes = await file.read()
        text = extract_text(file_bytes)

        chunks = chunk_text(text)
        embeddings = get_embeddings(chunks)

        build_index(chunks, embeddings)

        summary = summarize(text)

        return {
            "summary": summary,
            "message": "PDF processed and ready for chat"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/")
async def chat(query: str):
    try:
        answer = query_rag(query, model)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    return {"message": "API is running"}