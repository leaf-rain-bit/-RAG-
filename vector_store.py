from langchain_chroma import Chroma
import config_content as config
from langchain_community.embeddings import DashScopeEmbeddings

class vectorsroremodel(object):
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name= config.collection_name,
            embedding_function= self.embedding,
            persist_directory= config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs = {"k":config.similar_num})



