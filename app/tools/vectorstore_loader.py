# app/tools/vectorstore_loader.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader


def load_or_create_vectorstore(file_path: str, store_path: str):
    # 如果向量库目录不存在，则构建
    if not os.path.exists(store_path):
        print(f"未检测到向量库，开始构建：{store_path}")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"找不到语料文件：{file_path}")

        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=500, chunk_overlap=0
        )
        docs = text_splitter.split_documents(documents)

        vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings(),)
        vectorstore.save_local(store_path)
        print(f"向量库已构建并保存：{store_path}")

    # 无论是否新建，最后统一加载
    print(f"加载向量库：{store_path}")
    return FAISS.load_local(store_path, OpenAIEmbeddings(),allow_dangerous_deserialization=True
)
