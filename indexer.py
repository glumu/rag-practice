# -*- coding: utf-8 -*-

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import ModelScopeEmbeddings
from langchain_community.vectorstores import FAISS

if __name__ == "__main__":

    # 解析PDF，切成Chunk片段
    pdf_loader = PyPDFLoader("福建天创公司介绍.pdf", extract_images=True) # 使用OCR解析PDF中图片里的文字
    docs = pdf_loader.load()
    print(docs)

    # 使用RecursiveCharacterTextSplitter切分
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    chunks = text_splitter.split_documents(docs)
    # print(chunks)

    # 使用ModelScopeEmbeddings进行向量化
    embeddings = ModelScopeEmbeddings(model_id="iic/nlp_corom_sentence-embedding_chinese-base")

    # 将chunk插入到faiss本地向量库
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("tianchuang_faiss_db")
