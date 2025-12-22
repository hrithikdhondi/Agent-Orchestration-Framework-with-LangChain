from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

class SharedKnowledgeBase:
    def __init__(self, persist_directory: str = "./faiss_index"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Local embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load existing index or create new
        index_path = os.path.join(persist_directory, "index.pkl")
        if os.path.exists(index_path):
            self.vectorstore = FAISS.load_local(persist_directory, self.embeddings,  allow_dangerous_deserialization=True)
        else:
            self.vectorstore = FAISS.from_texts(["Shared knowledge base initialized."], self.embeddings)
            self.save()
    
    def save(self):
        """Persist vectorstore to disk"""
        self.vectorstore.save_local(self.persist_directory)
    
    def save_fact(self, fact: str):
        """Save important fact to shared memory"""
        self.vectorstore.add_texts([fact])
        self.save()
        print(f"💾 Saved to shared memory: {fact[:50]}...")
    
    def search_relevant_facts(self, query: str, k: int = 3) -> list:
        """Find relevant past knowledge for query"""
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def get_context(self, query: str) -> str:
        """Get formatted context from shared memory"""
        docs = self.search_relevant_facts(query)
        if not docs:
            return "No relevant past knowledge found."
        
        context = "Shared Knowledge Base:\n"
        for i, doc in enumerate(docs, 1):
            context += f"{i}. {doc.page_content}\n"
        return context