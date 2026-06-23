# src/split_data.py
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 读取校园csv问答数据集
df = pd.read_csv("./data2/campus_data.csv")
# 拼接单条问答为完整文本
all_text = ""
for idx, row in df.iterrows():
    single_text = f"分类：{row['category']} 问题：{row['question']} 回答：{row['answer']} 来源：{row['source']}\n"
    all_text += single_text

# 2. 初始化文本切分器（实训给定参数）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,      # 每段200字
    chunk_overlap=20     # 分段重叠20字
)

# 3. 执行文本切分
chunks = text_splitter.split_text(all_text)

# 4. 打印切分结果，用于实训验证
print(f"文本切分完成，共生成 {len(chunks)} 个文本块")
for i, chunk in enumerate(chunks):
    print(f"===== 文本块{i+1} =====")
    print(chunk)