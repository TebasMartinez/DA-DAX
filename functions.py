import streamlit as st

def companies_button(position):
    if position.button("Explore companies"):
            st.session_state.home_page = False
            st.session_state.companies = True
            st.session_state.industries = False
            st.rerun()

def industries_button(position):
      if position.button("Explore industries"):
            st.session_state.home_page = False
            st.session_state.companies = False
            st.session_state.industries = True
            st.rerun()

def home_button(position):
      if position.button("Back to home page"):
            st.session_state.home_page = True
            st.session_state.companies = False
            st.session_state.industries = False
            st.rerun()

def footer():
    footer = """<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: pink;
    color: black;
    text-align: center;
    }
    </style>
    <div class="footer">
    <p>Created by <a href="https://www.tebasmartinez.com/" target="_blank">Tebas Martínez</a></p>
    </div>
    """
    st.components.v1.html(footer)