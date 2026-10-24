from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
import config_content as config
from vector_store import vectorsroremodel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from file_history_store import get_history
from langchain_core.runnables import RunnablePassthrough,RunnableLambda


class Ragservice:
    def __init__(self):
        self.embedding_model = vectorsroremodel(
            embedding= DashScopeEmbeddings(
                model=config.embedding_model,
                dashscope_api_key=config.api_key
            )
        )

        self.chat_model = ChatTongyi(
            model = config.chat_model,
            api_key= config.api_key,
            streaming= True
        )

        self.prompt_template = ChatPromptTemplate(
            [
                ("system","你是一个根据参考文献简洁的回答问题的助手，参考文献：{context}"),
                ("system","并且如下是提供的聊天纪录："),
                MessagesPlaceholder("history"),
                ("user","用户提问：{input}")
            ]
        )

        self.chain = self.get_chain()

    def get_chain(self):
        retriever = self.embedding_model.get_retriever()

        def check_document(docs):
            if not docs:
                return "无相关参考资料"
            document_str = ""
            for doc in docs:
                document_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}"
            return document_str

        def temp1(value):
            return value["input"]

        def temp2(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value

        chain = (
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(temp1) | retriever | check_document
            } | RunnableLambda(temp2) | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key= "input",
            history_messages_key= "history",
        )

        return conversation_chain


