import hashlib
from datetime import datetime
from langchain_chroma import Chroma
import config_content as config
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def check_md5(md5_hex):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w',encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding="utf-8"):
            line = line.strip()
            if line == md5_hex:
                return True
        return False


def save_md5(md5_hex):
    with open(config.md5_path,'a',encoding="utf-8") as f:
        f.write(md5_hex + '\n')

def get_str_md5(data):
    str_md5 = data.encode('utf-8')
    md5_obj = hashlib.md5()
    md5_obj.update(str_md5)
    md5_hex = md5_obj.hexdigest()
    return md5_hex

class knowloadbaseservice():
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name= config.collection_name,
            embedding_function= DashScopeEmbeddings(model = config.embedding_model, dashscope_api_key = config.api_key),
            persist_directory=config.persist_directory,
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size= config.chunk_size,
            chunk_overlap= config.chunk_overlap,
            separators= config.separators,
            length_function= len
        )

    def upload_by_str(self,data,filename):
        md5_hex = get_str_md5(data)
        if check_md5(md5_hex):
            return "该文件已在数据库中"
        if len(data) > config.max_number:
            know_chunk = self.spliter.split_text(data)
        else:
            know_chunk = [data]

        metadata = {
            "source" : filename,
            "create_time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "operator":"leaf"
        }

        self.chroma.add_texts(
            know_chunk,
            metadatas = [metadata for _ in know_chunk],
        )

        save_md5(md5_hex)
        return "文件已成功加入数据库中"


