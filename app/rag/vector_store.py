import chromadb

from app.config import CHROMA_DIR


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(chunks, embeddings, document_id, filename):

    # Remove older chunks belonging to this document.
    collection.delete(
        where={
            "document_id": document_id
        }
    )

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        chunk_id = f"{document_id}_chunk_{i}"

        metadata = chunk.metadata.copy()

        metadata["document_id"] = document_id
        metadata["filename"] = filename

        ids.append(chunk_id)
        documents.append(chunk.page_content)
        metadatas.append(metadata)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def get_collection():
    return collection