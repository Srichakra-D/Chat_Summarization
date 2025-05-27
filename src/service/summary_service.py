import requests
import unicodedata
from fastapi import HTTPException

from ..client import messages_collection, summaries_collection
from ..models.summary import SummaryResponse
from ..config import settings

async def summarize_conversation(conversation_id: str) -> SummaryResponse:
    cursor = messages_collection.find({"conversation_id": conversation_id}).sort("timestamp", 1)
    formatted = []
    async for m in cursor:
        formatted.append(f"{m['user_id']}: {m['content']}")
    if not formatted:
        raise HTTPException(404, "No messages found")
    clean = [unicodedata.normalize("NFKC", line.strip()) for line in formatted]
    conversation_text = "\n".join(clean)
    summary_text = generate_summary(conversation_text)

    await summaries_collection.update_one(
        {"conversation_id": conversation_id},
        {"$set": {"summary_text": summary_text}},
        upsert=True
    )
    return SummaryResponse(conversation_id=conversation_id, summary_text=summary_text)

async def get_summary(conversation_id: str) -> SummaryResponse:
    doc = await summaries_collection.find_one({"conversation_id": conversation_id})
    if not doc:
        raise HTTPException(404, "Summary not found")
    return SummaryResponse(conversation_id=doc["conversation_id"], summary_text=doc["summary_text"])


def generate_summary(conversation_text: str) -> str:
    if not settings.HF_API_KEY:
        raise HTTPException(500, "Hugging Face API key is missing")
    headers = {"Authorization": f"Bearer {settings.HF_API_KEY}"}
    payload = {"inputs": conversation_text, "parameters": {"max_length": 500, "min_length": 30, "do_sample": False}}
    resp = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers=headers,
        json=payload
    )
    if resp.status_code != 200:
        raise HTTPException(500, "Error from Hugging Face API")
    try:
        return resp.json()[0]["summary_text"]
    except (KeyError, IndexError):
        raise HTTPException(500, "Unexpected response format")