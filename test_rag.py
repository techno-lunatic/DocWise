from pathlib import Path

from app.rag.loader import load_pdf
from app.rag.chunker import chunk_documents
from app.rag.embeddings import embed_documents
from app.rag.vector_store import add_documents
from app.rag.retriever import retrieve
from app.rag.query_rewriter import rewrite_query
from app.rag.prompt import build_prompt
from app.rag.generator import generate_answer
from app.rag.document import get_document_id

import time

# ==========================================
# FIND ALL PDF FILES
# ==========================================

upload_dir = Path("data/uploads")

pdf_files = list(upload_dir.glob("*.pdf"))

if not pdf_files:

    print("No PDF files found in data/uploads/")
    exit()


# print(f"Found {len(pdf_files)} PDF(s).")


# ==========================================
# INDEX EACH PDF
# ==========================================

for pdf_path in pdf_files:

    # print(f"\nIndexing: {pdf_path.name}")

    # Generate a unique ID for this PDF
    document_id = get_document_id(pdf_path)

    # print(f"Document ID: {document_id}")


    # Load PDF
    documents = load_pdf(str(pdf_path))

    # print("Pages:", len(documents))


    # Split into chunks
    chunks = chunk_documents(documents)

    # print("Chunks:", len(chunks))


    # Extract text
    texts = [
        chunk.page_content
        for chunk in chunks
    ]


    # Generate embeddings
    embeddings = embed_documents(texts)

    # print("Embeddings:", len(embeddings))


    # Store in ChromaDB
    add_documents(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
        filename=pdf_path.name
    )

    # print("Indexing complete!")


# ==========================================
# CONVERSATION
# ==========================================

messages = []


while True:

    curr= time.perf_counter()

    query = input("\nUser: ")


    # --------------------------------------
    # EXIT
    # --------------------------------------

    if query.lower().strip() == "exit":

        print("Goodbye!")
        break


    # --------------------------------------
    # CLEAR CONVERSATION
    # --------------------------------------

    if query.lower().strip() == "clear":

        messages = []

        print("Conversation memory cleared.")

        continue


    # ==========================================
    # QUERY REWRITING
    # ==========================================

    search_query = rewrite_query(
        query,
        messages
    )

    print(f"\nSearch query: {search_query}")


    # ==========================================
    # RETRIEVAL
    # ==========================================

    results = retrieve(search_query)

    retrieved_documents = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]


    # ==========================================
    # BUILD CONTEXT
    # ==========================================

    context_parts = []


    for document, metadata in zip(
        retrieved_documents,
        retrieved_metadatas
    ):

        filename = metadata.get(
            "filename",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )


        # PyPDFLoader uses zero-based page numbers
        if isinstance(page, int):
            page += 1


        context_parts.append(
            f"[Source: {filename} | Page: {page}]\n"
            f"{document}"
        )


    context = "\n\n".join(context_parts)


    # ==========================================
    # GENERATE ANSWER
    # ==========================================

    prompt = build_prompt(
        context,
        query
    )

    answer = generate_answer(prompt)

    print(f"Answered in {time.perf_counter()-curr}s")


    # ==========================================
    # DISPLAY ANSWER
    # ==========================================

    print("\n===== ANSWER =====")
    print(answer, flush=True)


    # ==========================================
    # DISPLAY SOURCES
    # ==========================================

    # print("\n===== SOURCES =====")


    # for i, metadata in enumerate(
    #     retrieved_metadatas
    # ):

    #     filename = metadata.get(
    #         "filename",
    #         "Unknown"
    #     )

    #     page = metadata.get(
    #         "page",
    #         "Unknown"
    #     )


    #     if isinstance(page, int):
    #         page += 1


    #     print(
    #         f"{i + 1}. {filename} - Page {page}"
    #     )


    # ==========================================
    # SAVE CONVERSATION
    # ==========================================

    messages.append(
        {
            "role": "user",
            "content": query
        }
    )


    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )