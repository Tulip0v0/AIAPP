from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
# 1. 加载文档（支持 pdf/txt/md 等）

documents = SimpleDirectoryReader("./my_docs").load_data()

# 2. 默认分块（可自定义 chunk_size）

# 底层会自动分块、生成节点（nodes）

# 3. 持久化 Chroma 客户端

db = chromadb.PersistentClient(path="./chroma_db")

chroma_collection = db.get_or_create_collection("my_knowledge")



# 4. 设置向量存储

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 5. 构建索引（自动 embedding + 存储）

index = VectorStoreIndex.from_documents(

    documents,

    storage_context=storage_context,

    # 可以指定 embed_model，默认用 OpenAI，也可以换本地模型

)

print("索引构建完成，已持久化到 ./chroma_db")