import pandas as pd
import os

# 数据文件在 AIAPP/data/campus_data.csv
data_path = "data/campus_data.csv"

# 检查文件是否存在
if not os.path.exists(data_path):
    print(f"找不到文件：{data_path}")
    print("请确认文件在 data 文件夹中")
    exit()

print("正在读取数据...")
df = pd.read_csv(data_path)

def split_text(text, chunk_size=200, chunk_overlap=20):
    """按字符数切分文本，支持重叠"""
    chunks = []
    start = 0
    text_length = len(text)
    
    # 如果文本为空，返回空列表
    if text_length == 0:
        return chunks
    
    # 如果文本长度小于等于 chunk_size，直接返回
    if text_length <= chunk_size:
        return [text]
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        
        # 计算下一个起始位置
        start = end - chunk_overlap
        
        # 防止死循环：如果 start 没有前进，强制前进
        if start <= 0:
            start = chunk_size
    
    return chunks

print("正在处理数据...")
text_list = []
for idx, row in df.iterrows():
    text = f"问题：{row['question']}\n回答：{row['answer']}"
    text_list.append(text)

print(f"共 {len(text_list)} 条数据")

# 切分文本
all_chunks = []
for i, text in enumerate(text_list):
    chunks = split_text(text, chunk_size=200, chunk_overlap=20)
    all_chunks.extend(chunks)
    
    # 每处理10条显示进度
    if (i + 1) % 10 == 0:
        print(f"已处理 {i+1}/{len(text_list)} 条")

print(f"切分完成，共 {len(all_chunks)} 段")

# 输出切分结果
output_path = "split_temp.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(all_chunks):
        f.write(f"第 {i+1} 段:\n")
        f.write(chunk + "\n=====\n")

print(f"结果已保存到：{output_path}")