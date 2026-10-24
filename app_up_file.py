import streamlit as st
from knowledge_base import knowloadbaseservice

st.title("文件上传")

upload_file = st.file_uploader(
    "请上传文件",
    type = ["txt","pdf"],
    accept_multiple_files = False
)

if "service" not in st.session_state:
    st.session_state["service"] = knowloadbaseservice()

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024

    st.subheader(f"文件名:{file_name}")
    st.write(f"文件格式:{file_type} | 文件大小:{file_size:.2f} KB")
    text = upload_file.getvalue().decode("utf-8")
    with st.spinner("思考中..."):
        res = st.session_state["service"].upload_by_str(text,file_name)
        st.write(res)
