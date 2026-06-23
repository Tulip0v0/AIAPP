import os
import sys
import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ========== 1. 检测是否在云端 ==========
if os.environ.get("STREAMLIT_CLOUD"):
    print("☁️  检测到 Streamlit Cloud 环境，加载已有向量库...")
    
    # 加载嵌入模型（不设置镜像）
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh",
        cache_folder="./model_cache"
    )
    
    # 加载已有向量库
    vector_db = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings
    )
    
    print("✅ 向量库加载完成")
    
else:
    # ========== 本地构建向量库 ==========
    print("🖥️  本地环境，开始构建向量库...")

    # 本地使用镜像加速
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    print("🖥️  本地环境，使用镜像加速")

    print("正在查找数据文件...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"脚本目录：{script_dir}")

    possible_paths = [
        os.path.join(script_dir, "../data/campus_data.csv"),
        os.path.join(script_dir, "data/campus_data.csv"),
        os.path.join(os.getcwd(), "data/campus_data.csv"),
        os.path.join(os.getcwd(), "../data/campus_data.csv"),
        "./data/campus_data.csv",
        "../data/campus_data.csv",
    ]

    csv_path = None
    for path in possible_paths:
        normalized = os.path.normpath(path)
        if os.path.exists(normalized):
            csv_path = normalized
            print(f"✅ 找到数据文件：{csv_path}")
            break

    if csv_path is None:
        print("❌ 找不到数据文件，创建示例数据...")
        data_dir = os.path.join(script_dir, "../data")
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, "campus_data.csv")
        
        sample_data = {
            'id': [1, 2, 3, 4, 5],
            'category': ['请假规则', '奖学金', '宿舍报修', '校园卡', '选课规则'],
            'question': [
                '如何请病假？', 
                '一等奖学金要求？',
                '怎么报修宿舍？',
                '校园卡丢了怎么办？',
                '如何办理退课？'
            ],
            'answer': [
                '学生请病假需填写请假审批单，附带校医院或二甲以上医院诊断证明；1天内班主任审批，3天内辅导员审批，3-7天系部主任审批，7天以上提交学生处审批。',
                '一等奖学年平均绩点≥3.5，二等奖≥3.0；全年无挂科、无违纪处分，体测成绩合格。',
                '两种渠道报修宿舍故障：1.校园后勤小程序线上提交报修；2.前往宿舍一楼宿管站登记报修。',
                '校园卡丢失第一时间登录校园智慧门户APP线上挂失冻结资金；补办地点为新桥校区食堂一楼卡务中心。',
                '在规定选课窗口期内登录教务系统提交退课申请，课程开课满2周后不再受理退课申请。'
            ]
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ 已创建示例数据：{csv_path}")

    print(f"\n正在加载数据...")
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_path, encoding='gbk')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='utf-8')

    print(f"✅ 加载了 {len(df)} 条记录")
    print(f"列名：{df.columns.tolist()}")

    print("\n正在加载嵌入模型（首次运行会下载模型，请稍候）...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh",
        cache_folder="./model_cache"
    )
    print("✅ 模型加载完成")

    print("\n正在构建向量库...")
    texts = df['answer'].tolist()

    metadatas = []
    for idx, row in df.iterrows():
        meta = {
            'id': str(row.get('id', idx + 1)),
            'category': str(row.get('category', '')),
            'question': str(row.get('question', ''))
        }
        metadatas.append(meta)

    vector_db_path = os.path.join(script_dir, "../vector_db")
    os.makedirs(vector_db_path, exist_ok=True)
    print(f"向量库保存路径：{vector_db_path}")

    vector_db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=vector_db_path
    )
    vector_db.persist()

    print(f"\n✅ 已存入 {len(texts)} 条记录到向量库")
    print(f"✅ 向量库保存在：{os.path.abspath(vector_db_path)}")