from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List

from ..models.chat import ChatMessage, MessageResponse
from ..client import messages_collection

async def store_message(chat: ChatMessage) -> MessageResponse:
    message_doc = chat.dict()
    result = await messages_collection.insert_one(message_doc)
    message_doc["message_id"] = str(result.inserted_id)
    return MessageResponse(**message_doc)

async def get_messages(
    conversation_id: str,
    keyword: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    limit: int
) -> List[MessageResponse]:
    
    query = {"conversation_id" : conversation_id}
    if keyword:
        query["$text"] = {"$search" : keyword}
    
    if end_date or start_date:
        dr = {}
        if start_date: dr["$gte"] = start_date
        if end_date: dr["$lte"] = end_date
        query["timestamp"] = dr
    
    cursor = messages_collection.find(query).sort("timestamp", -1).limit(limit)
    msgs = []
    async for m in cursor:
        msgs.append(MessageResponse(**{**m, "message_id": str(m["_id"]) }))
    
    if not msgs:
        raise HTTPException(404, "No messages found")
    
    return msgs

async def get_user_messages(user_id: str,
    page: int,
    limit: int):
    
    skip = (page - 1) * limit
    query = {"user_id": user_id}

    messages = []
    async for message in messages_collection.find(query).sort("timestamp", -1).skip(skip).limit(limit):
        message["message_id"] = str(message["_id"])
        messages.append(message)

    if not messages:
        raise HTTPException(status_code=404, detail="No chat history found for this user")

    return messages
    

async def delete_messages(conversation_id: str) -> dict:
    res = await messages_collection.delete_many({"conversation_id": conversation_id})
    if res.deleted_count == 0:
        raise HTTPException(404, "Conversation not found")
    return {"deleted": res.deleted_count}