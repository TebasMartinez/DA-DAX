import functions as f
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

def main():
    # Session set up
    if "home_page" not in st.session_state:
        # Page structure
        st.session_state.home_page = True
        st.session_state.companies = False
        st.session_state.chosen_company = False
        st.session_state.industries = False
        st.session_state.chosen_industry = False
        # Dataframes
        dfs = ['DAX', 'close_prices', 'volumes', 'returns', 
               'EURtoUSD', 'EURtoGBP', 'interest_rates', 'unemployment', 
               'monthly_close_prices', 'monthly_returns', 'monthly_volumes', 
               'merged_daily_market', 'merged_monthly_market']
        for df in dfs:
            st.session_state[df] = pd.read_csv(f"data/{df}.csv")
        # Variables
        st.session_state.company = ""
        st.session_state.industry = ""

    # HEADER
    left, center, right = st.columns([3,5,3])
    with center:
        st.title("DAX Dashboard")
    
    # HOME PAGE
    if st.session_state.home_page:
        st.write("""
        Welcome! In this app you'll be able to explore data from the DAX from 01/10/2023 to 30/09/2025
        including close prices, returns and volume, and compare it with macroeconomic and 
        social indicators such as exchange rates (EUR to USD and EUR to GBP), ECB's interest rates,
        and Germany's unemployment rate.
        """)
        left, certerleft, center, centerright, right = st.columns([1,4,4,4,1])
        f.companies_button(certerleft)
        f.industries_button(centerright)

    # COMPANIES DATA
    if st.session_state.companies == True:

        # Prompt user to choose a company
        if st.session_state.chosen_company == False:
            with st.sidebar:
                f.home_button()
            st.header("Company selection:")

            companies = sorted(set(st.session_state.merged_daily_market['company']))
            st.session_state.company = st.selectbox("Choose a company to explore:", companies)

            if st.button("Show data"):
                st.session_state.chosen_company = True
                st.rerun()

        # Company chosen
        else:
            with st.sidebar:
                f.home_button()
                if st.button("Change company"):
                    st.session_state.chosen_company = False
                    st.rerun()

            company = st.session_state.company
            industry = st.session_state.DAX[st.session_state.DAX['company']==company]['industry_en'].iloc[0]
            st.header(company)
            st.write(f"Industry: {industry}")

            with st.expander("Daily data"):
                f.company_daily_data(st.session_state.merged_daily_market, company)
            
            with st.expander("Monthly data"):
                f.company_monthly_data(st.session_state.merged_monthly_market, company)

    # INDUSTRIES DATA
    if st.session_state.industries == True:

        # Prompt user to choose an industry
        if st.session_state.chosen_industry == False: 
            with st.sidebar:
                f.home_button()

            st.header("Industry selection:")

            industries = sorted(set(st.session_state.merged_daily_market['industry']))
            st.session_state.industry = st.selectbox("Choose an industry to explore:", industries)

            if st.button("Show data"):
                st.session_state.chosen_industry = True
                st.rerun()

        # Industry chosen
        else:
            with st.sidebar:
                f.home_button()
                if st.button("Change industry"):
                    st.session_state.chosen_industry = False
                    st.rerun()

            industry = st.session_state.industry
            companies = list(st.session_state.DAX[st.session_state.DAX['industry_en']==industry]['company'].unique())
            n_companies = len(companies)
            st.header(industry)
            if n_companies == 1:
                st.markdown(f"Your selected industry, _{industry}_, is represented in the DAX with {n_companies} company:")
            else:
                st.markdown(f"Your selected industry, _{industry}_, is represented in the DAX with {n_companies} companies:")
            for company in companies:
                st.write(company)

            with st.expander("Daily data"):
                f.industry_daily_data(st.session_state.merged_daily_market, industry)
            
            with st.expander("Monthly data"):
                f.industry_monthly_data(st.session_state.merged_monthly_market, industry)

    # FOOTER
    f.footer()

if __name__ == '__main__':
    main()