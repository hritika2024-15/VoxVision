import streamlit as st

def style_background_home():

    st.markdown("""

    <style>
        .stApp {
        background: #f56uh0 !important;}
    </style>


                """,
                unsafe_allow_html=True)


def style_background_dashboard():

 st.markdown("""

    <style>
        .stApp {
        background: #e03e3f !important;}
    </style>


                """,
                unsafe_allow_html=True)


def style_base_layout():

 st.markdown("""

    <style>

    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Playwrite+BE+WAL+Guides&family=Playwrite+GB+S+Guides:ital@0;1&display=swap');
        /*Hide Top Bar of streamlit */

        #MainMenu, footer, header{
        visibility: hidden;}

        .block-container {
        padding-top: 1.5rem !important;
        margin: 0 auto !important;
        }

        .block-container h1,
        .block-container h2,
        .block-container h3,
        .block-container h4,
        .block-container p {
        text-align: center !important;
        }

        [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        }

        h1{
        font-family: 'Outfit', sans-serif !important;
         font-size: 3rem !important;
         line-height: 1.2 !important;
         margin-bottom: 0rem !important;}

        h2{
                 font-family: 'Outfit', sans-serif !important;
                  font-size: 3rem !important;
                  line-height: 1.2 !important;
                  margin-bottom: 0rem !important;}

        h3, h4, p {
                font-family: "Playwrite GB S Guides", cursive !important;
                 font-weight: 400 !important;
  font-style: italic !important;
            }

        button,
        button[kind="secondary"],
        button[data-testid="stBaseButton-secondary"]{
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"],
            button[data-testid="stBaseButton-tertiary"]{
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover,
            button[kind="secondary"]:hover,
            button[kind="tertiary"]:hover,
            button[data-testid^="stBaseButton-"]:hover{
                transform: scale(1.05) !important;
                cursor: pointer !important;
            }
                          
    </style>


                """,
                unsafe_allow_html=True)