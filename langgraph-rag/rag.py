import streamlit as st
from webui import rag_chat_page, knowledge_base_page
from utils import get_img_base64

#检查当前模块是否是主程序入口
if __name__ == '__main__':
    with st.sidebar:
        st.logo(
            get_img_base64('chatchat_lite_logo.png'),
            size="large",
            icon_image=get_img_base64('chatchat_lite_small_logo.png')
        )

    pg = st.navigation({
        "对话":[
            st.Page(rag_chat_page,title="智能客服",icon=":material/chat:"),
        ],
        "设置":[
            st.Page(knowledge_base_page,title="行业知识库",icon=":material/library_books:"),
        ]

    })

    pg.run()