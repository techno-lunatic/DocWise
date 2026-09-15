# DocWise

DocWise is a conversational document analysis assistant built using Retrieval-Augmented Generation (RAG). It allows users to upload company FAQs, policies, and internal documents, then ask questions and receive answers grounded in the uploaded documents.

## Features

- PDF upload and indexing
- Text extraction and chunking
- Semantic embeddings using Sentence Transformers
- Vector storage and similarity search with ChromaDB
- Conversational query rewriting
- Local LLM answer generation using Ollama
- Streaming responses
- Source document and page attribution
- Duplicate filename detection with overwrite support
- Multi-document retrieval

## Architecture

```text
PDF Documents
     ↓
PDF Loader
     ↓
Text Chunking
     ↓
Sentence Transformer Embeddings
     ↓
ChromaDB
     ↓
User Question
     ↓
Query Rewriting
     ↓
Query Embedding
     ↓
Top-K Retrieval
     ↓
Prompt + Retrieved Context
     ↓
Local Ollama LLM
     ↓
Streaming Answer + Sources
```

Detailed diagrams are available in `docs/`.

## Tech Stack

- Python
- Streamlit
- LangChain Community
- PyPDF
- Recursive Character Text Splitter
- Sentence Transformers
- ChromaDB
- Ollama
- Local open-source LLM

## Project Structure

```text
DocWise/
├── app/
│   ├── config.py
│   └── rag/
│       ├── loader.py
│       ├── chunker.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── query_rewriter.py
│       ├── prompt.py
│       ├── generator.py
│       └── document.py
├── data/
│   ├── uploads/
│   └── chroma_db/
├── demo/
│   ├── files/
│   ├── images/
│   └── video/
├── docs/
│   ├── process_flow.png
│   ├── architecture.png
│   └── rag_pipeline.png
├── frontend/
│   └── st_app.py
├── tests/
├── test_rag.py
├── requirements.txt
└── README.md
```

## How It Works

### Document Indexing

1. PDF is uploaded and saved locally.
2. Text is extracted using `PyPDFLoader`.
3. Text is split into smaller chunks.
4. Each chunk is converted into an embedding.
5. Chunks, embeddings, and metadata are stored in ChromaDB.

### Question Answering

1. The latest question is rewritten using conversation history when required.
2. The query is converted into an embedding.
3. ChromaDB retrieves the most relevant chunks.
4. Retrieved chunks are added to the prompt.
5. The local Ollama LLM generates the answer.
6. The answer is streamed to the interface.
7. Sources and page numbers are displayed.

## Demo Documents

Sample company-policy-style PDFs are available in:

```text
demo/files/
```

They can be uploaded directly for demonstrating indexing, multi-document retrieval, conversational questions, and source attribution.

## Limitations

DocWise V1 is optimized for text-dominant, digitally generated PDFs.

It does not currently focus on:

- Scanned or image-only PDFs
- Handwritten documents
- Advanced image understanding
- Complex visual layouts
- Advanced interpretation of diagrams or mathematical notation

## Future Improvements

- Hybrid semantic + keyword retrieval
- Better handling of exact policy/FAQ questions
- Query routing for non-document questions
- Conversation summarization for very long chats
- Advanced document versioning

## Author

Aaditya Gangurde
