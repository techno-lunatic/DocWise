# DocWise - User Manual

This manual explains how to install, start, and use DocWise.

## 1. Prerequisites

Install:

- Python
- Ollama
- Git
- VS Code (recommended)

## 2. Activate the Virtual Environment

From the project root, use Git Bash:

```bash
source docwise_venv/Scripts/activate
```

Verify Python:

```bash
python --version
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If Sentence Transformers gives a `torchvision` error, install the CPU versions:

```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 4. Check Ollama

Make sure Ollama is running and check the installed models:

```bash
ollama list
```

The model configured as `LLM_MODEL` in `app/config.py` must be installed.

## 5. Start the Application

From the DocWise root folder:

```bash
python -m streamlit run frontend/st_app.py
```

The application will open in your browser.

## 6. Upload and Index PDFs

1. Open DocWise.
2. Upload one or more PDF files.
3. For the demo, use the sample PDFs in:

```text
demo/files/
```

4. Click **Index Documents**.

DocWise performs:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

Wait for indexing to complete before asking questions.

## 7. Duplicate Documents

If a PDF with the same filename already exists, DocWise asks whether to overwrite it.

**Yes, Overwrite:** removes the old chunks and indexes the new PDF.

**No, Keep Existing:** keeps the existing document and does not index the new copy.

## 8. Ask Questions

After indexing, ask questions in the chat box.

Examples:

```text
What is the company's leave policy?
```

```text
How many vacation days are employees entitled to?
```

```text
What is the work-from-home policy?
```

```text
What are the rules for employee travel expenses?
```

The system retrieves relevant document chunks and provides them to the local LLM as context.

## 9. Conversational Questions

DocWise uses conversation history to resolve references.

Example:

```text
User: What is the company's vacation policy?

User: How many days does it provide?
```

The second question can be rewritten into a standalone search query before retrieval.

## 10. Sources

Each response can show the source document and page information used for the answer.

The system is instructed to answer using the retrieved document context and to say when the requested information is not found rather than inventing facts.

## 11. Recommended Demo

For a short demonstration:

1. Start Ollama.
2. Start Streamlit.
3. Upload the two PDFs from `demo/files/`.
4. Click **Index Documents**.
5. Ask a question answered by one document.
6. Ask a question requiring another document.
7. Ask a follow-up question using words such as "it", "they", or "that".
8. Show the source/page information.
9. Demonstrate the streaming response.

## 12. Troubleshooting

### ModuleNotFoundError

Activate the virtual environment and run:

```bash
pip install -r requirements.txt
```

### Ollama model error

Check:

```bash
ollama list
```

Make sure the installed model matches `LLM_MODEL` in `app/config.py`.

### Old or unexpected results

Re-index the relevant PDF. ChromaDB data is stored in:

```text
data/chroma_db/
```

### Poor PDF retrieval

DocWise V1 works best with digitally generated, text-based PDFs. Scanned/image-only PDFs are outside the current V1 scope.

## 13. Stop the Application

In the terminal running Streamlit, press:

```text
Ctrl + C
```
