from sentence_transformers import SentenceTransformer

import chromadb

# 加载相同 embedding 模型

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("my_knowledge")

# 向量化 query

query_embedding = embed_model.encode(query).tolist()

# 检索

results = collection.query(

    query_embeddings=[query_embedding],

    n_results=3,

    include=["documents", "metadatas"]

)

for doc, dist in zip(results['documents'][0], results['distances'][0]):

    print(f"Distance: {dist} (越小越相似)")

    print(doc[:200])