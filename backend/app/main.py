from fastapi import FastAPI
from app.api.routes_chatbot import router as chatbot_router

app = FastAPI(
    title="E-Commerce Chatbot",
    description="A FastAPI chatbot for product queries using DummyJSON and Groq LLM.",
    version="1.0.0"
)

app.include_router(chatbot_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)