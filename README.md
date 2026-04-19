# Multimodal RAG E-commerce Platform

This project is a complete, end-to-end AI-powered product catalog system. It features **semantic search**, **visual search** (via image URLs), and a **RAG-based AI Shopping Assistant**.

## 🚀 Features
- **Multimodal Search**: Search by text and/or image URLs.
- **AI Shopping Assistant**: RAG-powered answers based strictly on your product catalog.
- **Admin Dashboard**: Full CRUD management with automatic vector store synchronization.
- **Data Explorer**: Monitor system health, DB records, and vector counts.
- **Evaluation Suite**: Measure Precision@5 and MRR for search efficacy.

## 🛠 Tech Stack
- **Backend**: FastAPI, SQLAlchemy (PostgreSQL), Pinecone (Vector Store)
- **AI**: Google Gemini 1.5 Flash (Multimodal context) & text-embedding-004.
- **Frontend**: React (Vite), Tailwind CSS, Framer Motion.

## 📦 Project Structure
- `/backend`: FastAPI application and AI logic.
- `/frontend`: React application and styling.
- `/evals`: Search relevance evaluation scripts.
- `products.json`: Initial dataset for seeding.

## ⚙️ Prerequisites
1. **Python 3.10+**
2. **PostgreSQL** or any SQLAlchemy-supported DB.
3. **Pinecone Account** with an index named `ecommerce-catalog` (768 dimensions).
4. **Google Gemini API Key**.

---

## 🏃 How to Run

### 1. Set Environment Variables
Create a `.env` file in the root (or set in terminal):
```bash
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Seed the Data
In a separate terminal (from project root):
```bash
set PYTHONPATH=%PYTHONPATH%;.
python backend/load_data.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Run Evaluations
```bash
python evals/evals.py
```

---

## 🔍 Example Queries
- "I need some stylish wireless headphones for my daily commute."
- "Show me high-performance mechanical keyboards with RGB."
- "What are the best stability running shoes for overpronators?"
- **Multimodal**: Paste a URL of a shoe image + "Find similar items to this."

---

Created by **Antigravity AI**.
