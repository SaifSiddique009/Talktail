# Product Chatbot REST API

## Project Overview
This FastAPI-based backend powers a conversational chatbot for customer queries about products. It integrates:
- **Data Source**: DummyJSON Products API[](https://dummyjson.com/products) for real product details (titles, prices, ratings, categories, reviews, etc.).
- **AI Model**: Groq LLM (`llama-3.3-70b-versatile`) for intent analysis and generating human-like responses.
- **Logic**: RAG-style – Analyzes query intent (e.g., product details, price, reviews, category lists, high-rated products), retrieves relevant data, and crafts natural replies.
- **Endpoints**:
  - `GET /api/products`: Returns all products.
  - `POST /api/chat`: Processes messages like "Tell me about Kiwi" or "Products above 4 stars".
- **Evaluation Focus**: Clean REST design, modular FastAPI structure, seamless AI integration, context-aware chatbot, and full documentation.

Example Response for `{"message": "Tell me more about Kiwi"}`:
```json
{
  "response": "Kiwi is a delicious, nutrient-packed fruit option we carry! Our 4-pack is priced at around $2.50, with a stellar 4.8 rating from happy customers. It ships quickly and comes with our standard freshness guarantee. Want to add some to your cart?"
}


## Local Setup
1. Clone: `git clone https://github.com/yourusername/product-chatbot.git`
2. Backend: `cd backend && pip install -r requirements.txt`
   - Copy .env.example to .env, add GROQ_API_KEY.
   - Run: `uvicorn app.main:app --reload`
3. Frontend: `cd frontend && pip install -r requirements.txt`
   - Run: `streamlit run app.py`
4. Visit http://localhost:8501, optionally enter key (uses .env if present).

## Deployment

