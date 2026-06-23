import chromadb
from chromadb.utils import embedding_functions
import numpy as np

class ChromaDBDemo:
    """ChromaDB完整示例"""
    def __init__(self):
        # 创建持久化客户端
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # 使用默认的embedding函数
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # 创建或获取collection
        self.collection = self.client.get_or_create_collection(
            name="my_documents",
            embedding_function=self.embedding_fn,
            metadata={"description": "测试文档集合"}
        )

    def add_documents(self):
        """添加文档到数据库"""
        documents = [
            "RAG技术结合了检索和生成两种方法",
            "向量数据库用于存储和检索嵌入向量",
            "余弦相似度是衡量向量相似性的常用方法",
            "文本切片是RAG系统中的重要预处理步骤",
            "大语言模型可以生成连贯的文本回答"
        ]
        
        ids = [f"doc_{i}" for i in range(len(documents))]
        metadatas = [
            {"source": "tutorial", "topic": "RAG"},
            {"source": "tutorial", "topic": "database"},
            {"source": "tutorial", "topic": "similarity"},
            {"source": "tutorial", "topic": "preprocessing"},
            {"source": "tutorial", "topic": "LLM"}
        ]
        
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"已添加 {len(documents)} 个文档")

    def search(self, query: str, n_results: int = 3):
        """搜索相似文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        print(f"\n查询: '{query}'")
        print("-" * 50)
        for i, (doc, dist, meta) in enumerate(zip(
            results['documents'][0],
            results['distances'][0],
            results['metadatas'][0]
        )):
            print(f"结果 {i+1}:")
            print(f"  文档: {doc}")
            print(f"  距离: {dist:.4f}")
            print(f"  元数据: {meta}")
            print()
        
        return results

    def delete_collection(self):
        """删除集合"""
        self.client.delete_collection("my_documents")
        print("已删除集合")

    def get_collection_info(self):
        """获取集合信息"""
        count = self.collection.count()
        print(f"集合信息:")
        print(f"  名称: {self.collection.name}")
        print(f"  文档数量: {count}")
        print(f"  元数据: {self.collection.metadata}")

# 运行示例
def chromadb_demo():
    demo = ChromaDBDemo()
    demo.add_documents()
    demo.get_collection_info()
    
    # 测试搜索
    demo.search("什么是RAG？")
    demo.search("如何计算相似度？")
    
    return demo

if __name__ == "__main__":
    chromadb_demo()