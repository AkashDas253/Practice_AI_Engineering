AI Engineering

AI Engineering is the practice of building software applications around AI models.

Common Components

An AI application may contain:

A language model

Application logic

Data sources

Retrieval systems

Tools

Validation

Monitoring

Retrieval

Retrieval systems allow an application to find relevant information from a collection of documents.

Instead of sending every document to a language model, the application can retrieve the most relevant information and provide it as context.

RAG

Retrieval-Augmented Generation combines retrieval with language generation.

A simple RAG workflow is:

Load documents.

Split documents into chunks.

Create embeddings.

Retrieve relevant chunks.

Provide the chunks to the language model.

Generate an answer.

Important Principle

A language model is only one part of an AI application. The surrounding software system is responsible for managing data, retrieval, validation, errors, and application behavior.