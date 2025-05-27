from fastapi import FastAPI, Query
from typing import List, Optional
from datetime import datetime

from .config import settings
from .client import messages_collection, summaries_collection
from .models.chat import ChatMessage, MessageResponse
from .models.summary import SummarizationRequest, SummaryResponse
from .service.chat_service import store_message, get_messages, delete_messages, get_user_messages
from .service.summary_service import summarize_conversation, get_summary

app = FastAPI(title="Chat Summarization Service")

@app.post("/chats", response_model=MessageResponse)
async def create_chat(chat: ChatMessage):
    """Store a chat message in the database."""
    return await store_message(chat)

@app.get("/chats/{conversation_id}", response_model=List[MessageResponse])
async def read_chats(
    conversation_id: str,
    keyword: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 50
):
    """ Retrieve messages from a specific conversation, with optional keyword and date filters. """
    return await get_messages(conversation_id, keyword, start_date, end_date, limit)

@app.get("/users/{user_id}/chats", response_model=List[MessageResponse])
async def get_user_chat_history(
    user_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Messages per page")
):
    """ Retrieve a paginated list of chat messages for a given user."""
    return await get_user_messages(user_id, page, limit)
    

@app.delete("/chats/{conversation_id}")
async def delete_chat(conversation_id: str):
    """ Delete an entire conversation and all its messages. """
    return await delete_messages(conversation_id)

@app.post("/summaries", response_model=SummaryResponse)
async def create_summary(req: SummarizationRequest):
    """
    Summarizes a conversation by its ID using the Hugging Face API.
    It fetches all messages in the conversation (sorted by timestamp),
    then constructs a string with user IDs, messages, and timestamps,
    and finally sends it to the Hugging Face summarization API.
    """
    return await summarize_conversation(req.conversation_id)

@app.get("/summaries/{conversation_id}", response_model=SummaryResponse)
async def read_summary(conversation_id: str):
    """ Get's the conversation summary if it exits. """
    return await get_summary(conversation_id)