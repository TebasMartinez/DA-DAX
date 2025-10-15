import functions as f
import pandas as pd
import streamlit as st

def main():
    # Session set up
    if "home_page" not in st.session_state:
        # Page structure
        st.session_state.home_page = True
        st.session_state.companies = False
        st.session_state.industries = False

    # HEADER
    left, center, right = st.columns([3,5,3])
    with center:
        st.title("DAX Dashboard")
    
    # HOME PAGE
    if st.session_state.home_page:
        st.write("""
        Welcome! In this app you'll be able to explore data from the DAX from 01/10/2023 to 30/09/2025
        including close prices, returns and volume, and compare it with macroeconomical and 
        social indicators such as exchange rates (EUR to USD and EUR to GBP), ECB's interest rates,
        and Germany's unemployment rate.
        """)
        left, certerleft, center, centerright, right = st.columns([1,4,4,4,1])
        f.companies_button(certerleft)
        f.industries_button(centerright)

    # COMPANIES DATA
    if st.session_state.companies == True:
        left, center, right = st.columns(3)
        f.home_button(center)
        st.write("exploring companies")

    # INDUSTRIES DATA
    if st.session_state.industries == True:
        left, center, right = st.columns(3)
        f.home_button(center)
        st.write("exploring industries")

    # FOOTER
    f.footer()

if __name__ == '__main__':
    main()