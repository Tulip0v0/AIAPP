import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_templates import RAG_PROMPT

load_dotenv()

# ========== 检查 API Key ==========
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("❌ 未找到 DEEPSEEK_API_KEY，请在环境变量或 Streamlit Secrets 中配置")

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=api_key
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


def rag_answer(question, history=None):
    """
    RAG问答，支持历史记忆
    
    参数：
        question: 用户问题
        history: 对话历史列表 [{"role": "user", "content": "..."}, ...]
    
    返回：
        大模型生成的回答
    """
    try:
        vector_db = get_vector_db()
    except Exception as e:
        return f"向量库加载失败：{str(e)}"
    
    # 1. 检索相关文档
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 2. 如果有历史，加入提示词
    if history:
        history_text = ""
        for msg in history[-10:]:
            role = "用户" if msg["role"] == "user" else "助手"
            history_text += f"{role}: {msg['content']}\n"
        context = f"对话历史：\n{history_text}\n\n参考资料：\n{context}"
    
    # 3. 拼接提示词
    prompt = RAG_PROMPT.format(context=context, question=question)
    
    # 4. 调用大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


# ========== 测试 ==========
if __name__ == "__main__":
    # 测试1：基础问答
    print("测试1：", rag_answer("宿舍断电时间是几点？"))
    
    # 测试2：带历史问答
    history = [
        {"role": "user", "content": "我叫小明"},
        {"role": "assistant", "content": "你好小明！有什么可以帮你的吗？"}
    ]
    print("测试2：", rag_answer("我叫什么", history=history))