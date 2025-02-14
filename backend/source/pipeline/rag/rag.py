import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from enum import Enum
from typing import List, Optional, Dict, Any

class RAG:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', index_path: str = 'code_index.faiss'):
        self.model: SentenceTransformer = SentenceTransformer(model_name)
        self.index_path: str = index_path
        self.index: Optional[faiss.Index] = None
        self.code_chunks: List[str] = []
        self.metadata: List[Dict[str, Any]] = []

        # initializes faiss index if not found then must be first run
        if not self.index_path or not os.path.exists(self.index_path):
            self.index = None
        else:
            try:
                self.index = faiss.read_index(self.index_path)
            except Exception as e:
                print(f"Warning: Could not load index from {self.index_path}. Creating new index.")
                self.index = None

    def extract_content(self, file_path: str) -> Dict[str, str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                filename = os.path.basename(file_path)
                content = f.read()
            return {
                "filename": filename,
                "content": content
            }
        except Exception as e:
            print(f"Warning: Could not process file {file_path}: {str(e)}")
            return {"filename": "", "content": ""}

    def embed_code(self, code_files: List[Dict[str, str]]) -> None:  # Added -> None
        code_chunks = []
        metadata = []

        # Process each dictionary of code content
        for file_dict in code_files:
            try:
                content = file_dict['content']
                filename = file_dict['filename']

                # get the language of the file
                language = os.path.splitext(filename)[1][1:].upper() if os.path.splitext(filename)[1] else "TXT"
                
                # split into meaningful chunks
                chunks = self._split_into_chunks(content, language)
                code_chunks.extend(chunks)
                
                # store metadata for each chunk
                for i, chunk in enumerate(chunks):
                    metadata.append({
                        'file_name': filename,
                        'chunk_number': i,
                        'start_line': i * 10,
                    })
            except Exception as e:
                print(f"Warning: Could not process file {filename}: {str(e)}")
                continue

        if not code_chunks:
            raise ValueError("No valid code chunks were extracted from the files.")

        self.code_chunks = code_chunks
        self.metadata = metadata
        
        # create embeddings for each chunk
        embeddings = self.model.encode(code_chunks, show_progress_bar=True)

        # initialize or update faiss index
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))
        
        # save index
        faiss.write_index(self.index, self.index_path)

    def _split_into_chunks(self, content: str, lang: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        # error catching
        if not content:
            raise ValueError("Content cannot be empty")
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")
        if not isinstance(overlap, int) or overlap < 0:
            raise ValueError("overlap must be a non-negative integer")
        if overlap >= chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        
        chunks = []
        
        try:
            # validate if language is supported
            try:
                language_enum = Language[lang]
            except KeyError:
                # fallback to generic text splitting if language not supported
                print(f"Warning: Language '{lang}' not supported. Falling back to generic text splitting.")
                language_enum = None

            # create the splitter with language-specific settings
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=language_enum,
                chunk_size=chunk_size,
                chunk_overlap=overlap
            ) if language_enum else RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
                length_function=len,
                is_separator_regex=False
            )
            
            # split the content into chunks
            code_docs = splitter.create_documents([content])
            chunks = [doc.page_content for doc in code_docs]
            if not chunks:
                raise ValueError("Failed to generate chunks from the content")
            return chunks

        except Exception as e:
            raise RuntimeError(f"Error splitting content into chunks: {str(e)}")


    def retrieve_context(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if self.index is None or self.index.ntotal == 0:
            raise ValueError("The Faiss index is empty. Please embed code before querying.")

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k)

        results = []
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.code_chunks):
                results.append({
                    'code': self.code_chunks[idx],
                    'metadata': self.metadata[idx],
                    'similarity_score': float(1 / (1 + distances[0][i]))
                })
            else:
                print(f"Warning: Skipping invalid index {idx}.")

        if not results:
            raise ValueError("No relevant context found. The index may not be populated correctly.")

        return results

    def clear_index(self) -> None:  # Added -> None
        self.index = faiss.IndexFlatL2(384)
        self.code_chunks = []
        self.metadata = []
        faiss.write_index(self.index, self.index_path)

    def format_prompt(self, query: str, context: List[Dict[str, Any]]) -> str:
        # Include only the top 3 most relevant context sections based on similarity score
        sorted_context = sorted(context, key=lambda x: x['similarity_score'], reverse=True)[:3]
        
        # Build the context string with only essential details
        context_str = ""
        for i, result in enumerate(sorted_context, 1):
            context_str += f"\nSection {i}:\n"
            context_str += f"Code:\n{result['code']}\n"  # Exclude metadata and similarity score
            context_str += "-" * 40 + "\n"

        # Concise prompt with minimal instructions
        prompt = f"""Provide only the shortest and most direct answer to the question. Do not elaborate or provide additional information.
        
        Context:{context_str}

        Question: {query}

        Answer:"""

        return prompt
