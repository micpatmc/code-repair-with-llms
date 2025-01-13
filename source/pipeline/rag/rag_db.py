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
        self.index_path =  index_path
        self.index = None
        self.code_chunks = []

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

        # read and split the code files into chunks
        for file in code_files:
            with open(file, 'r') as f:
                code_chunks.extend(f.readlines())
        self.code_chunks = code_chunks
        embeddings = self.model.encode(code_chunks)

        # get out index value as our embedding shape
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))
        faiss.write_index(self.index, self.index_path)

    # retrieves our context from the vector db
    def retrieve_context(self, query , k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k)
        return [self.code_chunks[i] for i in indices[0]]
    
    def clear_index(self):
        self.index = None
        self.code_chunks = []
        # write empty index to faiss with 384 dimensions since default model uses 384
        faiss.write_index(faiss.IndexFlatL2(384), self.index_path)

if __name__ == "__main__":
    # Initialize the RAG pipeline
    rag = RAG()

    # Embed code from files
    code_files = ["C:\\Users\\Gavin Cruz\\Documents\\SD1\\finalspace\\code-repair-with-llms\\source\\pipeline\\rag\\example1.py", "C:\\Users\\Gavin Cruz\\Documents\\SD1\\finalspace\\code-repair-with-llms\\source\\pipeline\\rag\\example2.py"]  # Replace with actual file paths
    rag.embed_code(code_files)

    # Clear the vector database
    rag.clear_index()

    # Save the Faiss index for later use
    print("Vector database created and saved to", rag.index_path)