import requests

def summarize(text):
    prompt = f"""
    Summarize the following document in 5 bullet points:

    {text}
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