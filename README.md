# FastAPI Chat Service with MongoDB

This project is a FastAPI-based chat service that stores messages in MongoDB and provides features such as message retrieval, deletion, and summarization using Hugging Face's API.

## Setup

### 1. Setting up the Database

First, ensure you have MongoDB installed and running. You can start a local instance using:

```sh
mongod --dbpath /path/to/db
```

Next, open a `mongosh` shell and create the database and collections:

```
use chatdb

// Create 'messages' collection with schema validation
db.createCollection("messages", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["conversation_id", "user_id", "content", "timestamp"],
      properties: {
        conversation_id: { bsonType: "string", description: "must be a string and is required" },
        user_id: { bsonType: "string", description: "must be a string and is required" },
        content: { bsonType: "string", description: "must be a string and is required" },
        timestamp: { bsonType: "date", description: "must be a date and is required" }
      }
    }
  }
})

// Create indexes for faster queries
db.messages.createIndex({ conversation_id: 1 })  
db.messages.createIndex({ user_id: 1 })         
db.messages.createIndex({ timestamp: -1 })      
db.messages.createIndex({ content: "text" })    

// Create 'summaries' collection with schema validation
db.createCollection("summaries", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["conversation_id", "summary_text"],
      properties: {
        conversation_id: { bsonType: "string", description: "must be a string and is required" },
        summary_text: { bsonType: "string", description: "must be a string and is required" }
      }
    }
  }
})

// Create an index on 'conversation_id' for faster retrieval of summaries
db.summaries.createIndex({ conversation_id: 1 }, { unique: true })  
```

### 2. Setting Up the `.env` File

Create a `.env` file in the root directory with the following contents:

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=chatdb
HF_API_KEY=your_hugging_face_api_key
```

Replace `your_hugging_face_api_key` with your actual Hugging Face API key.
Replace MONGO_URI with your MongoDB connection string.

### 3. Installing Dependencies

Create a virtual environment and install dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Running the Application

Start the FastAPI server:

```sh
uvicorn app:app --reload
```

The API documentation will be available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

- **POST /chats** - Store a chat message
- **GET /chats/{conversation_id}** - Retrieve messages for a conversation
- **GET /users/{user_id}/chats** - Retrieve a user's chat history
- **DELETE /chats/{conversation_id}** - Delete a conversation
- **POST /chats/summarize** - Summarize a conversation using Hugging Face API
- **GET /summaries/{conversation_id}** - Get a stored summary

