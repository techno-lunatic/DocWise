import sys
from pathlib import Path


# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))


import streamlit as st

from app.config import UPLOAD_DIR
from app.rag.loader import load_pdf
from app.rag.chunker import chunk_documents
from app.rag.embeddings import embed_documents
from app.rag.vector_store import add_documents
from app.rag.retriever import retrieve
from app.rag.query_rewriter import rewrite_query
from app.rag.prompt import build_prompt
from app.rag.generator import generate_answer
from app.rag.document import get_document_id


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DocWise",
    page_icon="📚",
    layout="wide"
)


st.title("DocWise")
st.caption("Conversational analysis of text-based documents")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_files" not in st.session_state:
    st.session_state.pending_files = None

if "overwrite_confirmation" not in st.session_state:
    st.session_state.overwrite_confirmation = False


# --------------------------------------------------
# INDEX PDF
# --------------------------------------------------

def index_pdf(file, overwrite=False):

    file_path = UPLOAD_DIR / file.name

    # If file already exists and overwrite
    # permission has not been given, stop here.
    if file_path.exists() and not overwrite:

        return {
            "status": "exists",
            "filename": file.name
        }

    # Save uploaded PDF
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    # Generate document ID
    document_id = get_document_id(file_path)

    # Load PDF
    documents = load_pdf(str(file_path))

    # Split PDF into chunks
    chunks = chunk_documents(documents)

    # Create embeddings
    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = embed_documents(texts)

    # Store chunks and embeddings
    add_documents(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
        filename=file.name
    )

    return {
        "status": "indexed",
        "filename": file.name,
        "pages": len(documents),
        "chunks": len(chunks)
    }


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

def ask_question(query):

    # Rewrite the question using conversation history
    search_query = rewrite_query(
        query,
        st.session_state.messages
    )

    # Retrieve relevant chunks
    results = retrieve(search_query)

    retrieved_documents = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]

    # Build context for LLM
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

    # Build final LLM prompt
    prompt = build_prompt(
        context=context,
        question=query
    )

    # Return streaming generator + metadata
    answer_stream = generate_answer(prompt)

    return answer_stream, retrieved_metadatas


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )


    # --------------------------------------------------
    # INDEX BUTTON
    # --------------------------------------------------

    if st.button("Index Documents"):

        if not uploaded_files:

            st.warning(
                "Upload at least one PDF."
            )

        else:

            duplicate_files = []

            # Check for existing filenames
            for file in uploaded_files:

                file_path = UPLOAD_DIR / file.name

                if file_path.exists():
                    duplicate_files.append(
                        file.name
                    )


            # --------------------------------------------------
            # DUPLICATES FOUND
            # --------------------------------------------------

            if duplicate_files:

                st.warning(
                    "The following PDF(s) already exist:"
                )

                for filename in duplicate_files:

                    st.write(
                        f"📄 {filename}"
                    )

                st.session_state.pending_files = (
                    uploaded_files
                )

                st.session_state.overwrite_confirmation = True

                st.rerun()


            # --------------------------------------------------
            # NO DUPLICATES
            # --------------------------------------------------

            else:

                for file in uploaded_files:

                    with st.spinner(
                        f"Indexing {file.name}..."
                    ):

                        result = index_pdf(file)

                    st.success(
                        f"{result['filename']} indexed "
                        f"({result['pages']} pages, "
                        f"{result['chunks']} chunks)"
                    )


    # --------------------------------------------------
    # OVERWRITE CONFIRMATION
    # --------------------------------------------------

    if st.session_state.overwrite_confirmation:

        st.warning(
            "A PDF with the same filename already exists. "
            "Do you want to overwrite it?"
        )

        col1, col2 = st.columns(2)


        # --------------------------------------------------
        # YES - OVERWRITE
        # --------------------------------------------------

        with col1:

            if st.button("Yes, Overwrite"):

                pending_files = (
                    st.session_state.pending_files
                )

                for file in pending_files:

                    with st.spinner(
                        f"Overwriting {file.name}..."
                    ):

                        result = index_pdf(
                            file,
                            overwrite=True
                        )

                    st.success(
                        f"{result['filename']} "
                        f"overwritten and indexed "
                        f"({result['pages']} pages, "
                        f"{result['chunks']} chunks)"
                    )

                st.session_state.pending_files = None

                st.session_state.overwrite_confirmation = False

                st.rerun()


        # --------------------------------------------------
        # NO - KEEP EXISTING
        # --------------------------------------------------

        with col2:

            if st.button("No, Keep Existing"):

                st.info(
                    "Existing PDF(s) were kept."
                )

                st.session_state.pending_files = None

                st.session_state.overwrite_confirmation = False

                st.rerun()


    # --------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------

    st.divider()

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            with st.expander("Sources"):

                for source in message["sources"]:

                    st.write(
                        f"📄 {source['filename']} "
                        f"— Page {source['page']}"
                    )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

query = st.chat_input(
    "Ask something about your documents..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if query:

    # Display user's question
    with st.chat_message("user"):

        st.markdown(query)


    # Display assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer_stream, metadata = ask_question(
                    query
                )

                # Stream the answer as it is generated
                answer = st.write_stream(
                    answer_stream
                )


                # --------------------------------------------------
                # SOURCE INFORMATION
                # --------------------------------------------------

                sources = []

                for source in metadata:

                    filename = source.get(
                        "filename",
                        "Unknown"
                    )

                    page = source.get(
                        "page",
                        "Unknown"
                    )

                    if isinstance(page, int):
                        page += 1

                    sources.append(
                        {
                            "filename": filename,
                            "page": page
                        }
                    )


                # Display sources
                with st.expander("Sources"):

                    for source in sources:

                        st.write(
                            f"📄 {source['filename']} "
                            f"— Page {source['page']}"
                        )


            except Exception as e:

                answer = (
                    "An error occurred while "
                    "processing your question."
                )

                st.error(str(e))

                sources = []


    # --------------------------------------------------
    # SAVE CHAT HISTORY
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )