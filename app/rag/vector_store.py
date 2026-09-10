import chromadb

from app.config import CHROMA_DIR


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(chunks, embeddings):

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    documents = [
        chunk.page_content
        for chunk in chunks
    ]

    metadatas = [
        chunk.metadata
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def get_collection():
    return collection