import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_templates import RAG_PROMPT

load_dotenv()
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

# ========== 延迟加载向量库 ==========
_vector_db = None

def get_vector_db():
    global _vector_db
    if _vector_db is not None:
        return _vector_db
    
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh",
        cache_folder="./model_cache"
    )
    _vector_db = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings
    )
    return _vector_db

def rag_answer(question):
    # 1. 获取向量库
    try:
        vector_db = get_vector_db()
    except Exception as e:
        return f"向量库加载失败：{str(e)}"
    
    # 2. 检索
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 3. 生成回答
    prompt = RAG_PROMPT.format(context=context, question=question)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content