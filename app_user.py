import streamlit as st
from rag import Ragservice
import config_content as config

st.title("智能问答")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = Ragservice()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_list = []
    with st.spinner("思考中..."):
        # 正常输出
        # AImessage = st.session_state["rag"].chain.invoke({"input":prompt},config.session_config)
        # st.chat_message("assistant").write(AImessage)
        # st.session_state["message"].append({"role": "assistant", "content": AImessage})
        # 流式输出
        AImessage = st.session_state["rag"].chain.stream({"input":prompt},config.session_config)
        def stream_output(message,a_list):
            for chunk in message:
                a_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(stream_output(AImessage,ai_list))
        st.session_state["message"].append({"role":"assistant","content":"".join(ai_list)})

