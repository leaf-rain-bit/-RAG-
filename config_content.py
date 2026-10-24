
collection_name = "rag"
persist_directory = "./chroma_db"
md5_path = "./md5.txt"

chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n","\n",".",",","，","。","?","？","!","！"," ","\r\n",""]

max_number = 1000            # 阈值

similar_num = 1

embedding_model = "text-embedding-v4"
api_key = "你的api_key"
chat_model = "qwen-max"

session_config = {
    "configurable":{
        "session_id":"user_001"
    }
}

