from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
import pandas as pd

# 读取csv数据
df = pd.read_csv("data/campus_data.csv")
texts = []
for _, row in df.iterrows():
    content = f"校园问答：{row['question']} {row['answer']}"
    texts.append(content)

# 文本分割
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = splitter.create_documents(texts)

# 加载向量模型
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 构建本地向量库
db = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="vector_db"
)
db.persist()
print("向量库构建完成，保存在vector_db文件夹")