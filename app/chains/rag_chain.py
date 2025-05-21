
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from app.tools.vectorstore_loader import load_or_create_vectorstore

# 加载导航向量库
navigation_vectorstore = load_or_create_vectorstore(
    "../../data/hospital_navigation_corpus.txt",
    "../../vectorstore/faiss_index/navigation_faiss"
)
navigation_chain = RetrievalQA.from_chain_type(
    # llm=ChatOpenAI(),
llm = ChatOllama(
    model="qwen2:7b",
    temperature=0.3,
),
    retriever=navigation_vectorstore.as_retriever()
)

def get_navigation_answer(query: str) -> str:
    return navigation_chain.run(query)

# 加载医疗问答向量库
qa_vectorstore = load_or_create_vectorstore(
    "../../data/medical_qa_corpus.txt",
    "../../vectorstore/faiss_index/qa_faiss"
)
qa_chain = RetrievalQA.from_chain_type(
    # llm=ChatOpenAI(),
llm = ChatOllama(
    model="qwen2:7b",
    temperature=0.3,
),
    retriever=qa_vectorstore.as_retriever()
)

def get_medical_qa_answer(query: str) -> str:
    return qa_chain.run(query)
