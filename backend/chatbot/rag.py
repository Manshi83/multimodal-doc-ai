import faiss
import numpy as np
import requests

documents = []
index = None

def build_index(chunks, embeddings):
    global documents, index

    documents = chunks

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))


def query_rag(query, model):
    global documents, index

    if index is None:
        raise Exception("Upload PDF first")

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=5)

    contexts = [documents[i] for i in I[0]]
    context = " ".join(contexts)

    prompt = f"""
    You are a helpful assistant.

    Use ONLY the given context to answer.
    If not found, say "Not found in document".

    Context:
    {context}

    Question: {query}

    Answer clearly:
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception("Model failed")

    return response.json()["response"]