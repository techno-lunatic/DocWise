from sentence_transformers import SentenceTransformer
# ST is a library that converts a text based sentence into embeddings

from app.config import EMBEDDING_MODEL


model = SentenceTransformer(EMBEDDING_MODEL)

# Embeds the entire documents provided into embeddings
def embed_documents(texts):

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()


# Converts user query into embeddings
def embed_query(query):

    embedding = model.encode(
        query,
        prompt_name="query",
        normalize_embeddings=True
    )

    return embedding.tolist()