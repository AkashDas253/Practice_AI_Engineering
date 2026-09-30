# Retrieval & RAG Practice

Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

**Practice documents included:** `rag.txt`, `ai_engineering.md`, `rag.json`, `rag_notes.csv`, `rag.html`, and `rag_paper.pdf`.

**Output:** Generated artifacts are saved in `output/` and may be reused by later exercises.

## Document Ingestion

| Script Name | Purpose / RAG Concept | Execution Command |
| --- | --- | --- |
| `document_loading.py` | Demonstrates discovering and loading documents from local files without interpreting their format-specific contents. | `python document_loading.py` |
| `document_parsing.py` | Demonstrates extracting and normalizing usable text from different document formats such as TXT, Markdown, JSON, CSV, HTML, and PDF. | `python document_parsing.py` |

## Chunking

| Script Name | Purpose / RAG Concept | Execution Command |
| --- | --- | --- |
| `text_chunking.py` | Demonstrates different chunking strategies, including fixed-size, sentence-based, paragraph-based, recursive, and overlapping chunks. | `python text_chunking.py` |
| `metadata_extraction.py` | Demonstrates extracting and attaching metadata such as source, title, section, document type, and chunk information. | `python metadata_extraction.py` |

## Embeddings

| Script Name | Purpose / RAG Concept | Execution Command |
| --- | --- | --- |
| `embedding_generation.py` | Demonstrates converting normalized document chunks into vector embeddings for semantic retrieval. | `python embedding_generation.py` |
| `embedding_similarity.py` | Demonstrates comparing query and document embeddings to measure semantic similarity. | `python embedding_similarity.py` |

## Vector Storage & Retrieval

| Script Name | Purpose / RAG Concept | Execution Command |
| --- | --- | --- |
| `vector_store.py` | Demonstrates storing prepared document chunks, embeddings, and metadata in a simple vector store. Produces `output/vector_store.json` for reuse by retrieval exercises. | `python vector_store.py` |
| `semantic_search.py` | Demonstrates semantic retrieval using vector similarity, including top-K selection, similarity thresholds, and basic relevance filtering. Reads from `output/vector_store.json`. | `python semantic_search.py` |
| `keyword_search.py` | Demonstrates traditional keyword-based retrieval using lexical matching. Reads from `output/vector_store.json`. | `python keyword_search.py` |
| `hybrid_search.py` | Demonstrates combining keyword and semantic retrieval signals into a hybrid ranking. Reads from `output/vector_store.json`. | `python hybrid_search.py` |
| `metadata_filtering.py` | Demonstrates narrowing retrieval candidates using document and chunk metadata before or during search. Reads from `output/vector_store.json`. | `python metadata_filtering.py` |
| `retrieval_reranking.py` | Demonstrates retrieving an initial candidate set and reranking the candidates using a second relevance signal before selecting the final results. Reads from `output/vector_store.json`. | `python retrieval_reranking.py` |

## RAG Construction

| Script Name | Purpose / RAG Concept | Execution Command |
| --- | --- | --- |
| `context_assembly.py` | Demonstrates selecting, ordering, deduplicating, and combining retrieved chunks into context for the language model. Uses `output/vector_store.json` as its retrieval source. | `python context_assembly.py` |
| `rag_basic.py` | Demonstrates the basic RAG pipeline: retrieve relevant information, assemble context, and generate an answer using the retrieved chunks. Uses `output/vector_store.json`. | `python rag_basic.py` |
| `rag_grounded_generation.py` | Demonstrates generating answers grounded in retrieved context rather than relying only on model knowledge. Uses `output/vector_store.json`. | `python rag_grounded_generation.py` |
| `rag_citations.py` | Demonstrates generating answers with source and chunk citations so supporting retrieved documents can be traced. Uses `output/vector_store.json`. | `python rag_citations.py` |
| `rag_no_answer.py` | Demonstrates checking retrieval relevance and returning no answer when sufficiently relevant information is not found. Uses `output/vector_store.json`. | `python rag_no_answer.py` |

## Advanced RAG

| Script Name | Purpose / RAG Concept | Execution Command |
| --- | --- | --- |
| `rag_query_rewriting.py` | Demonstrates transforming a user's query into a retrieval-friendly query before semantic search. Uses `output/vector_store.json` and produces a rewritten query and retrieved documents in the console. | `python rag_query_rewriting.py` |
| `rag_multi_query.py` | Demonstrates generating multiple search queries and combining their retrieval results to improve retrieval coverage. Uses `output/vector_store.json` and produces generated queries and combined retrieval results in the console. | `python rag_multi_query.py` |
| `rag_conversation_context.py` | Demonstrates using conversation history to resolve follow-up questions before retrieving relevant document chunks. Uses `output/vector_store.json` and produces the retrieval query, retrieved context, and generated answer in the console. | `python rag_conversation_context.py` |
| `rag_evaluation.py` | Demonstrates evaluating retrieval quality and generated answers using retrieval similarity, groundedness, relevance, and completeness measures. Uses `output/vector_store.json` and produces retrieval and answer evaluation metrics in the console. | `python rag_evaluation.py` |
| `rag_pipeline.py` | Demonstrates the complete RAG pipeline from document ingestion, parsing, chunking, metadata, and embeddings through retrieval, context construction, and grounded generation. Uses `documents/rag.txt` and produces `output/rag_pipeline.json` plus the pipeline results in the console. | `python rag_pipeline.py` |