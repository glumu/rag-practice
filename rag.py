# -*- coding: utf-8 -*-
import os
import warnings
# 解决OpenMP库冲突问题
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# 抑制警告信息，让输出更清晰
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from typing import Any
import uuid
from operator import itemgetter
from langchain_community.embeddings import ModelScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# Azure OpenAI 配置
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "https://your-resource.cognitiveservices.azure.com")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

# 使用ModelScopeEmbeddings将query进行向量化
embeddings = ModelScopeEmbeddings(model_id="iic/nlp_corom_sentence-embedding_chinese-base")

# 从本地向量库中加载
vector_db = FAISS.load_local("tianchuang_faiss_db", embeddings, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 5}) # 返回Top5个相似的Chunk

chat = AzureChatOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    temperature=0.7,
    streaming=True
)

# Prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "你是一个专业的知识库助手。"
)
user_prompt = HumanMessagePromptTemplate.from_template('''
请根据以下内容回答问题：{context}

问题：{query}
''')

full_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    MessagesPlaceholder(variable_name="chat_history"),
    user_prompt
])

# 存储会话历史的全局字典
session_histories = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    
    history = session_histories[session_id]
    
    # 如果消息数量超过20条，只保留最后20条
    if len(history.messages) > 20:
        recent_messages = history.messages[-20:]
        history.clear()
        for message in recent_messages:
            history.add_message(message)
    
    return history

if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    print(f"会话ID: {session_id}")
    
    # 构建RAG链
    rag_chain = (
        {
            "context": itemgetter("query") | retriever,
            "query": itemgetter("query"),
            "chat_history": itemgetter("chat_history")
        }
        | full_prompt 
        | chat 
        | StrOutputParser()
    )
    
    # 添加消息历史功能
    chain_with_history = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="chat_history"
    )

    while True:
        query = input('请输入问题：')
        if query.lower() in ['exit', 'quit', '退出']:
            break
            
        try:
            response = chain_with_history.invoke(
                {"query": query},
                config={"configurable": {"session_id": session_id}}
            )
            print(f"回答: {response}")
            
            # 显示当前历史记录数量（用于调试）
            current_history = get_session_history(session_id)
            print(f"当前历史记录数量: {len(current_history.messages)}")
            
        except Exception as e:
            print(f"错误: {e}")
