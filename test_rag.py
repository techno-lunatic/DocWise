from app.rag.loader import load_pdf
from app.rag.chunker import chunk_documents
from app.rag.embeddings import embed_documents
from app.rag.vector_store import add_documents
from app.rag.retriever import retrieve


pdf_path = "data/uploads/english.pdf"


# 1. Load PDF
documents = load_pdf(pdf_path)

print("Pages:", len(documents))


# 2. Split into chunks
chunks = chunk_documents(documents)

print("Chunks:", len(chunks))


# 3. Extract text
texts = [
    chunk.page_content
    for chunk in chunks
]


# 4. Create embeddings
embeddings = embed_documents(texts)

print("Embeddings:", len(embeddings))


# 5. Store in ChromaDB
add_documents(chunks, embeddings)

print("Indexing complete!")


# 6. Test retrieval
query = input("\nAsk a question: ")

results = retrieve(query)


# 7. Display retrieved chunks
retrieved_documents = results["documents"][0]

for i, document in enumerate(retrieved_documents):

    print(f"\n--- Result {i + 1} ---")
    print(document)