# 📊 Smart Contract Analyst

Financial report analysis application based on RAG (Retrieval Augmented Generation) using LangChain, ChromaDB, and OpenAI.

## ✨ Features

- **PDF Document Upload**: Import your financial reports (URD)
- **Vector Indexing**: Documents are chunked and stored in ChromaDB
- **Intelligent Q&A**: Ask questions about your documents and get contextualized answers
- **Intuitive User Interface**: Simple and efficient Streamlit interface
- **REST API**: FastAPI backend for decoupled architecture

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Streamlit UI  │─────▶│   FastAPI API   │─────▶│    ChromaDB     │
│   (Port 8501)   │      │   (Port 8000)   │      │  Vector Store   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   OpenAI API    │
                         │  (GPT-4 + Ada)  │
                         └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Docker and Docker Compose (optional)
- OpenAI API Key

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/Jovillios/smart-contract-analyst.git
cd smart-contract-analyst
```

2. **Configure OpenAI API Key**

```bash
export OPENAI_API_KEY="your-api-key"
```

### Option 1: With Docker (recommended)

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:8501
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Local Installation

```bash
# Install uv if needed
pip install uv

# Install dependencies
uv sync

# Start the API
uv run uvicorn src.api.main:app --reload --port 8000

# In another terminal, start the frontend
uv run streamlit run src/ui/app.py --server.port 8501
```

## 📖 Usage

1. **Upload a PDF document**
   - Access the interface at http://localhost:8501
   - Use the upload widget to drop your financial report
   - Wait for indexing confirmation

2. **Ask questions**
   - Use the chat to ask questions about the document
   - The assistant will respond based solely on the document content
   - Sources used can be displayed in a dropdown menu

## 🔌 API Endpoints

### `POST /ingest`
Ingests a PDF document into the vector database

**Parameters:**
- `file`: PDF file (form-data)

**Response:**
```json
{
  "filename": "report.pdf",
  "total_pages": 42,
  "status": "Ingestion successful"
}
```

### `POST /query`
Ask a question about indexed documents

**Body:**
```json
{
  "question": "What was last year's revenue?"
}
```

**Response:**
```json
{
  "answer": "The revenue was...",
  "sources": [
    {
      "source": "report.pdf",
      "page": 5
    }
  ]
}
```

### `DELETE /reset`
Clears the vector database (useful for development)

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4
- **Embeddings**: OpenAI text-embedding-3-large
- **Vector Store**: ChromaDB
- **PDF Processing**: PyMuPDF
- **Orchestration**: LangChain

## 📁 Project Structure

```
smart-contract-analyst/
├── src/
│   ├── api/          # FastAPI backend
│   │   ├── main.py   # API endpoints
│   │   └── utils.py  # Utility functions
│   └── ui/           # Streamlit frontend
│       └── app.py    # User interface
├── data/
│   ├── pdf/          # Original PDFs
│   └── uploaded/     # Uploaded PDFs
├── chroma/           # ChromaDB vector database
├── notebooks/        # Exploration notebooks
├── tests/            # Unit tests
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 🧪 Tests

```bash
uv run pytest
```

## 🔧 Development

### Linting and Formatting

```bash
uv run ruff check .
uv run ruff format .
```

### Exploration Notebooks

The `notebooks/` folder contains Jupyter notebooks to explore:
- `00_discovery.ipynb`: Data exploration
- `01_ingestion.ipynb`: Ingestion pipeline testing
- `02_vector_store.ipynb`: ChromaDB manipulation

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or pull request.
