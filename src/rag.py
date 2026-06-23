import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_templates import RAG_PROMPT, RAG_WITH_HISTORY_PROMPT
from build_vector_db import vector_db

load_dotenv()
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

def rag_answer(question, history=None):
    """
    RAG问答，支持历史记忆
    history: 对话历史列表 [{"role": "user", "content": "..."}, ...]
    """
    # 1. 向量库检索
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 2. 根据是否有历史选择不同提示词
    if history:
        # 格式化历史对话（最近5轮）
        history_text = ""
        for msg in history[-10:]:  # 最近10条消息
            role = "用户" if msg["role"] == "user" else "助手"
            history_text += f"{role}: {msg['content']}\n"
        
        prompt = RAG_WITH_HISTORY_PROMPT.format(
            history=history_text,
            context=context,
            question=question
        )
    else:
        prompt = RAG_PROMPT.format(context=context, question=question)
    
    # 3. 调用大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content