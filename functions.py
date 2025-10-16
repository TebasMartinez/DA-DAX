import plotly.express as px
import streamlit as st

# NAVIGATION
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

def home_button():
      if st.button("Back to home page"):
            st.session_state.home_page = True
            st.session_state.companies = False
            st.session_state.industries = False
            st.session_state.company = ""
            st.session_state.industry = ""
            st.session_state.chosen_company = False
            st.session_state.chosen_industry = False
            st.rerun()

# COMPANIES PAGE 
def company_daily_data(df_daily, company):
      df_daily = df_daily[df_daily['company']==company]

      close_fig = px.line(df_daily, x='date', y='close', title='Close Price')
      volume_fig = px.line(df_daily, x='date', y='volume', title='Volume')
      return_fig = px.line(df_daily, x='date', y='return', title='Returns (%)')
      st.plotly_chart(close_fig, use_container_width=True)
      st.plotly_chart(volume_fig, use_container_width=True)
      st.plotly_chart(return_fig, use_container_width=True)

      left, right = st.columns(2)
      left.scatter_chart(df_daily, x='close', y='1eur_usd')
      right.scatter_chart(df_daily, x='close', y='1eur_gbp')

      left, right = st.columns(2)
      left.scatter_chart(df_daily, x='return', y='1eur_usd')
      right.scatter_chart(df_daily, x='return', y='1eur_gbp')

      left, right = st.columns(2)
      left.scatter_chart(df_daily, x='volume', y='1eur_usd')
      right.scatter_chart(df_daily, x='volume', y='1eur_gbp')

def company_monthly_data(df_monthly, company):
      df_monthly = df_monthly[df_monthly['company']==company]

      close_fig_month = px.line(df_monthly, x='month', y='close', title='Close Price at end of month')
      return_fig_moth = px.line(df_monthly, x='month', y='return', title='Returns (%) at end of month')
      st.plotly_chart(close_fig_month, use_container_width=True)
      st.plotly_chart(return_fig_moth, use_container_width=True)

      left, right = st.columns(2)
      left.scatter_chart(df_monthly, x='close', y='unemployment_rate')
      right.scatter_chart(df_monthly, x='close', y='interest_rate')

      left, right = st.columns(2)
      left.scatter_chart(df_monthly, x='return', y='unemployment_rate')
      right.scatter_chart(df_monthly, x='return', y='interest_rate')

# INDUSTRIES PAGE
def industry_daily_data(df_daily, industry):
      pass

def industry_monthly_data(df_monthly, industry):
      pass

# FOOTER
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
    Created by <a href="https://www.tebasmartinez.com/" target="_blank">Tebas Martínez</a><br>
    See this project's repo on <a href="https://github.com/TebasMartinez/DA-DAX" target="_blank">GitHub</a>
    </div>
    """
    st.components.v1.html(footer)