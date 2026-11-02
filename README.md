# DocWise — Local RAG Application

DocWise is a locally running Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents through a conversational interface. It uses semantic search to retrieve relevant document sections and a locally hosted LLM to generate responses.

## Features

- PDF upload and text extraction using PyPDFLoader.
- Recursive text chunking with configurable overlap.
- Semantic embeddings using Sentence Transformers.
- Vector storage and retrieval using ChromaDB.
- Top-5 relevant chunk retrieval.
- Conversational query rewriting using chat history.
- Local response generation using Ollama.
- Streaming responses through Streamlit.
- Source filename and page metadata display.
- Duplicate filename detection and document replacement.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| PDF Processing | PyPDFLoader |
| Text Chunking | RecursiveCharacterTextSplitter |
| Embeddings | Qwen3-Embedding-0.6B |
| Vector Database | ChromaDB |
| LLM Runtime | Ollama |
| Language Model | Llama 3.2 3B |
| Framework Components | LangChain |

## RAG Pipeline

**Document Ingestion**

1. Upload PDF through Streamlit.
2. Extract text and page metadata using PyPDFLoader.
3. Split text into chunks using RecursiveCharacterTextSplitter.
4. Generate embeddings using Sentence Transformers.
5. Store embeddings and metadata in ChromaDB.

**Question Answering**

1. Accept a user query.
2. Rewrite follow-up questions using conversation history.
3. Generate query embeddings.
4. Retrieve the five most relevant chunks from ChromaDB.
5. Pass retrieved context to the local LLM through Ollama.
6. Stream the generated response with source and page information.

## Configuration

| Parameter | Value |
|---|---|
| Chunk Size | 800 |
| Chunk Overlap | 120 |
| Retrieval Top-K | 5 |
| Embedding Model | Qwen/Qwen3-Embedding-0.6B |
| Embedding Normalization | Enabled |
| LLM | llama3.2:3b |
| Generation | Streaming |

## Project Structure

```text
DocWise/
│
├── app/
│   ├── config.py
│   └── rag/
│       ├── loader.py
│       ├── chunker.py
│       ├── embeddings.py
│       ├── retriever.py
│       ├── query_rewriter.py
│       ├── prompt.py
│       ├── generator.py
│       ├── vector_store.py
│       └── document.py
│
├── frontend/
│   └── st_app.py
│
├── demo/
│   ├── files/
│   ├── Images/
│   └── Video/
│
├── requirements.txt
├── README.md
└── MANUAL.md
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/techno-lunatic/DocWise.git
cd DocWise
```

**2. Create and activate a virtual environment**

```bash
python -m venv docwise_venv

# Git Bash (Windows)
source docwise_venv/Scripts/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Install Ollama and download the language model**

Download Ollama from https://ollama.com/

```bash
ollama pull llama3.2:3b
```

**5. Run the application**

```bash
streamlit run frontend/st_app.py
```

Open the local URL displayed in the terminal.

The embedding model `Qwen/Qwen3-Embedding-0.6B` is loaded through Sentence Transformers and may be downloaded during its first initialization.

## Usage

1. Upload a PDF document.
2. Wait for document processing and indexing.
3. Enter a question related to the uploaded document.
4. View the generated response and its source information.
5. Ask follow-up questions using the conversation interface.

If a document with the same filename already exists, the application provides an overwrite option to replace its previously indexed chunks.

## References

- [Ollama](https://ollama.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB](https://docs.trychroma.com/)
- [Streamlit](https://docs.streamlit.io/)
- [LangChain](https://python.langchain.com/)
