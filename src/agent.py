from tools import get_current_week, calculate_gpa
from rag import rag_answer

# ============================================
# 对话记忆管理
# ============================================

conversation_history = []

def add_to_history(role, content):
    """添加对话到历史"""
    conversation_history.append({"role": role, "content": content})
    # 保留最近20条
    if len(conversation_history) > 20:
        conversation_history.pop(0)

def get_history():
    """获取历史记录"""
    return conversation_history

# ============================================
# 智能体核心函数
# ============================================

def agent_chat(user_input):
    """智能问答入口"""
    # 1. 意图识别 - 查询周数
    if "周" in user_input and ("几" in user_input or "校历" in user_input):
        return get_current_week()

    # 2. 意图识别 - 计算绩点
    if "绩点" in user_input or "GPA" in user_input:
        import re
        scores = re.findall(r'\d+', user_input)
        if scores:
            return calculate_gpa(', '.join(scores))
        else:
            return "请告诉我您的各科分数，例如：85,90,78"

    # 3. 默认走RAG问答（传入历史）
    return rag_answer(user_input, history=get_history())


def chat_with_memory(user_input):
    """带记忆的多轮对话"""
    # 记录用户输入
    add_to_history("user", user_input)
    
    # 获取回答
    response = agent_chat(user_input)
    
    # 记录助手回答
    add_to_history("assistant", response)
    
    return response


# ============================================
# 交互式对话
# ============================================

def run_chat():
    print("=" * 50)
    print("  校园智能助手 (带记忆功能)")
    print("=" * 50)
    print("输入 'exit' 退出")
    print("输入 'clear' 清空记忆")
    print("-" * 50)
    
    while True:
        user_input = input("\n你: ").strip()
        
        if user_input.lower() == 'exit':
            print("再见！")
            break
        elif user_input.lower() == 'clear':
            conversation_history.clear()
            print("✅ 记忆已清空")
            continue
        
        response = chat_with_memory(user_input)
        print(f"助手: {response}")


if __name__ == "__main__":
    run_chat()