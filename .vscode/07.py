# 第一步：导入库
import gradio as gr

# 第二步：定义处理函数
def greet(name):
    return f"你好，{name}！欢迎学习AI应用开发！"

# 第三步：创建界面
demo = gr.Interface(
    fn=greet,           # 处理函数
    inputs="text",      # 输入类型
    outputs="text",     # 输出类型
    title="AI应用开发演示",  # 标题
    description="请输入你的名字，我会和你打招呼"  # 描述
)

# 第四步：启动应用
demo.launch()