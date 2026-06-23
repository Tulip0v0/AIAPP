import gradio as gr
from src.rag import search_knowledge

def chat_reply(user_input):
    context = search_knowledge(user_input)
    reply = f"根据校园知识库查询到：\n{context}"
    return reply

demo = gr.Interface(
    fn=chat_reply,
    inputs=gr.Textbox(label="你的校园问题", placeholder="例如：图书馆几点关门"),
    outputs=gr.Textbox(label="问答回复"),
    title="校园百事通助手",
    description="基于本地知识库的校园问答小程序"
)

if __name__ == "__main__":
    demo.launch()