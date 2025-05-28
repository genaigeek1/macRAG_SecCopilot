
from src.retriever import VectorRetriever
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

class SecurityRAGPipeline:
    def __init__(self, documents: list):
        self.retriever = VectorRetriever()
        self.retriever.build_index(documents)
        self.llm = Ollama(model='mistral')
        self.qa = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.retriever)

    def answer(self, question: str):
        return self.qa.run(question)
