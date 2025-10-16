# ShopTalk: The AI Product Chatbot

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-orange)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-purple)](https://groq.com/)

ShopTalk is an intelligent e-commerce chatbot designed to provide instant, natural-language answers to customer questions about products. It leverages the speed of the Groq LPU™ Inference Engine with the `llama-3.3-70b-versatile` model to understand user intent, retrieves real-time product data from the DummyJSON API, and formulates helpful, human-like responses.

The project consists of a robust **FastAPI backend** for the core logic and a user-friendly **Streamlit frontend** for interaction.

---

## 🚀 Live Demo

You can interact with the deployed application directly in your browser!

*   **Frontend (Chat Interface):** [**https://shoptalk.onrender.com/**](https://shoptalk.onrender.com/)
*   **Backend (API Docs):** [**https://talktail.onrender.com/docs**](https://talktail.onrender.com/docs)

*Note: You will need to provide your own Groq API key to use the live demo.*

## 🎥 Video Walkthrough

For a detailed walkthrough and demonstration of the project, please watch the video linked below:

[Watch the Full Project Demo on Google Drive](https://drive.google.com/file/d/1uDj2n73kclWthww4d2t7aOsLjZvf6nuH/view?usp=sharing)

## ✨ Features

-   **Natural Language Understanding:** Ask questions in plain English, just like talking to a human sales assistant.
-   **Intent-Driven Responses:** The chatbot intelligently identifies user intent to provide precise answers for:
    -   **Product Details:** Get a full summary of a product (price, rating, warranty, etc.).
    -   **Specific Information:** Ask for just the price, reviews, or return policy.
    -   **Filtered Lists:** Find products by category (`"Do you have any electronics?"`) or by rating (`"Show me products with ratings above 4."`).
    -   **Category Discovery:** Ask what product categories are available.
-   **Fuzzy Name Matching:** Finds products even if you don't type the exact name (e.g., "kiwi" matches "Kiwi").
-   **Super-Category Search:** Broader categories like "fashion" or "electronics" will correctly map to their respective sub-categories.
-   **Interactive Frontend:** A simple and intuitive Streamlit interface with pre-written query examples to get you started.
-   **RESTful API:** A well-documented FastAPI backend with Swagger UI for easy testing and integration.

## 🛠️ How It Works

The chatbot uses a two-step LLM-powered process to ensure accurate, data-grounded responses:

1.  **Intent Analysis:** When a user sends a message, the FastAPI backend sends the query to the Groq API. The first prompt asks the LLM to analyze the message and extract key information into a structured JSON object, identifying the `intent`, `product_name`, `category`, and `rating_filter`.

2.  **Data Retrieval & Response Generation:**
    -   Based on the extracted intent, the backend calls the appropriate function in the `product_service` to fetch relevant product data from the DummyJSON API (with in-memory caching for performance).
    -   This retrieved, context-specific data is then passed back to the Groq API with a second, tailored prompt.
    -   This final prompt instructs the LLM to act as a friendly customer service rep and formulate a natural language response **based only on the provided data**, preventing hallucinations and ensuring accuracy.



## 📂 Project Structure

```
product-chatbot/
 ├── backend/
 │    ├── app/
 │    │    ├── api/
 │    │    │    └── routes_chatbot.py     # FastAPI routes
 │    │    ├── core/
 │    │    │    └── config.py             # Pydantic settings
 │    │    ├── services/
 │    │    │    ├── chatbot_service.py    # Core chat logic
 │    │    │    └── product_service.py    # Data fetching/filtering
 │    │    ├── models/
 │    │    │    └── schemas.py            # Pydantic models
 │    │    ├── utils/
 │    │    │    └── groq_client.py        # Groq API wrapper
 │    │    └── main.py                   # FastAPI app entrypoint
 │    ├── requirements.txt              # Backend dependencies
 ├── frontend/
 │    ├── app.py                        # Streamlit UI code
 │    ├── requirements.txt              # Frontend dependencies
 ├── .env                                # Environment variables (you create this)
 └── README.md
```

## ⚙️ Getting Started: Local Setup

Follow these steps to run the entire application on your local machine.

### Prerequisites

-   [Python 3.9+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/)
-   A [Groq API Key](https://console.groq.com/keys)

### 1. Clone the Repository

```bash
git clone https://github.com/SaifSiddique009/Talktail.git
cd Talktail
```

### 2. Set Up Environment Variables

Add your Groq API key to this file:

```env
# .env
GROQ_API_KEY="gsk_YourSecretGroqApiKeyHere"
```

### 3. Install Dependencies

You'll need to install dependencies for both the backend and frontend.

```bash
# Install dependencies
pip install -r requirements.txt
```

### 4. Run the Backend Server

Open a terminal and start the FastAPI server. It will run on `http://localhost:8001`.

```bash
cd backend/
uvicorn app.main:app --reload --port 8001
```

You can now access the API documentation at **[http://localhost:8001/docs](http://localhost:8001/docs)**.

### 5. Run the Frontend Application

Open a **second terminal** and start the Streamlit app.

```bash
cd frontend/
streamlit run app.py
```

Navigate to **[http://localhost:3000](http://localhost:3000)** (or the URL provided in your terminal) to interact with the chatbot.

## 🚀 Usage

### Using the Streamlit Frontend

1.  **API Key**: If you set up the `.env` file, your Groq API key will be pre-filled. If not, you must enter it into the text input field.
2.  **Ask a Question**:
    -   Select a pre-written query from the dropdown menu to see how it works.
    -   Type your own custom question into the text box.
3.  **Send**: Click the "Send" button to get a response from the chatbot.

### Using the API directly

You can also send requests directly to the FastAPI backend using tools like `curl` or the Swagger UI.

#### Get All Products

```bash
curl -X GET "http://localhost:8001/api/products"
```

#### Chat Endpoint

```bash
curl -X POST "http://localhost:8001/api/chat" \
-H "Content-Type: application/json" \
-d '{
      "message": "Tell me the reviews for volleyball.",
      "groq_api_key": "gsk_YourSecretGroqApiKeyHere"
    }'
```

## 🗣️ Example Queries

Here are some examples of questions you can ask the chatbot:

-   `"What’s the price of kiwi?"`
-   `"Do you have any electronics?"`
-   `"Show me products with ratings above 4."`
-   `"Tell me the reviews for volleyball."`
-   `"Do you have volleyball?"`
-   `"Show me products with ratings below 4."`
-   `"Tell me the return policy of Kiwi."`
-   `"What product categories do you have?"`
-   `"What can you tell me about the Essence Mascara?"`

---