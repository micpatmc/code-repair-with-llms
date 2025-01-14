"""
Here, this class will store the vector db for the model to refer to 
rather than passing the code files to the prompts each time.

This class must be initialized and populated prior to the first stage
in the pipeline
"""
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

class RAG:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='code_index.faiss'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.index = None
        self.code_chunks = []
        self.metadata = []

        # initializes faiss index if not found then must be first run
        if not self.index_path or not os.path.exists(self.index_path):
            self.index = None
        else:
            try:
                self.index = faiss.read_index(self.index_path)
            except Exception as e:
                print(f"Warning: Could not load index from {self.index_path}. Creating new index.")
                self.index = None

    def embed_code(self, code_files):
        code_chunks = []
        metadata = []

        # read and split the code files into chunks
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # split into meaningful chunks
                    chunks = self._split_into_chunks(content)
                    code_chunks.extend(chunks)
                    # store file path and chunk position for each chunk
                    for i, chunk in enumerate(chunks):
                        metadata.append({
                            'file_path': file_path,
                            'chunk_number': i,
                            'start_line': i * 10,
                            'file_name': os.path.basename(file_path)
                        })
            except Exception as e:
                print(f"Warning: Could not process file {file_path}: {str(e)}")
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

    # split code content into meaningful chunks
    def _split_into_chunks(self, content, chunk_size=10):
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            current_chunk.append(line)
            
            # create a new chunk when we hit the chunk size or find a natural break
            if (len(current_chunk) >= chunk_size and 
                (line.strip() == '' or line.strip().startswith('def ') or 
                 line.strip().startswith('class '))):
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
        
        # add any remaining lines as the last chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks

    # retrieves relevant code chunks based on query
    def retrieve_context(self, query, k=5):
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

    def clear_index(self):
        self.index = faiss.IndexFlatL2(384)
        self.code_chunks = []
        self.metadata = []
        faiss.write_index(self.index, self.index_path)