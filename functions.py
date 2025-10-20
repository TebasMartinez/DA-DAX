from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import torch
import torch.nn as nn

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
def company_kpi_dashboard(df_daily, company):
    """Display KPI dashboard for a specific company"""
    st.subheader("📊 Company Performance Dashboard")
    
    # Filter data for the company
    company_data = df_daily[df_daily['company'] == company].copy()
    company_data['date'] = pd.to_datetime(company_data['date'])
    company_data = company_data.sort_values('date')
    
    # Calculate KPIs
    current_price = company_data['close'].iloc[-1]
    price_30d_ago = company_data['close'].iloc[-30] if len(company_data) >= 30 else company_data['close'].iloc[0]
    
    avg_price = company_data['close'].mean()
    max_price = company_data['close'].max()
    min_price = company_data['close'].min()
    
    avg_daily_return = company_data['return'].mean()
    positive_days = len(company_data[company_data['return'] > 0])
    negative_days = len(company_data[company_data['return'] < 0])
    win_rate = (positive_days / len(company_data)) * 100
    
    avg_volume = company_data['volume'].mean()
    
    # Create KPI columns
    col1, col2, col3, col4 = st.columns(4)
        
    with col1:
        st.metric(
            "Average Price",
            f"€{avg_price:.2f}"
        )
    
    with col2:
        st.metric(
            "Win Rate",
            f"{win_rate:.1f}%"
        )
    
    with col3:
        st.metric(
            "Avg Daily Return",
            f"{avg_daily_return:.2f}%",
            delta_color="inverse" if avg_daily_return < 0 else "normal"
        )

    with col4:
        st.metric(
            "Avg Volume",
            f"{avg_volume:,.0f}",
            help="Average daily trading volume"
        )
    
    # Additional insights
    with st.expander("📈 Detailed Insights"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Price Performance**")
            st.write(f"• 52-week high: €{max_price:.2f}")
            st.write(f"• 52-week low: €{min_price:.2f}")
            st.write(f"• Current vs average: {((current_price/avg_price)-1)*100:.1f}%")
            
            # Calculate different period returns
            if len(company_data) >= 60:
                price_60d_ago = company_data['close'].iloc[-60]
                change_60d = ((current_price - price_60d_ago) / price_60d_ago) * 100
                st.write(f"• 60-day return: {change_60d:.1f}%")
        
        with col2:
            st.write("**Trading Activity**")
            st.write(f"• Total trading days: {len(company_data)}")
            st.write(f"• Positive days: {positive_days} ({win_rate:.1f}%)")
            st.write(f"• Negative days: {negative_days} ({(negative_days/len(company_data))*100:.1f}%)")
            st.write(f"• Neutral days: {len(company_data) - positive_days - negative_days}")

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
def industry_kpi_dashboard(df_daily, industry, companies):
    """Display KPI dashboard for a specific industry"""
    st.subheader("🏭 Industry Performance Dashboard")
    
    # Filter data for the industry
    industry_data = df_daily[df_daily['industry'] == industry].copy()
    industry_data['date'] = pd.to_datetime(industry_data['date'])
    industry_data = industry_data.sort_values('date')
    
    # Calculate industry aggregates
    industry_daily = (
        industry_data.groupby('date', as_index=False)
        .agg({
            'close': 'mean',
            'return': 'mean',
            'volume': 'sum',
            '1eur_usd': 'mean',
            '1eur_gbp': 'mean'
        })
        .rename(columns={
            'close': 'avg_close',
            'return': 'avg_return',
            'volume': 'total_volume'
        })
    )
    
    # Industry KPIs
    current_avg_price = industry_daily['avg_close'].iloc[-1]
    avg_price_30d_ago = industry_daily['avg_close'].iloc[-30] if len(industry_daily) >= 30 else industry_daily['avg_close'].iloc[0]
    industry_change_30d = ((current_avg_price - avg_price_30d_ago) / avg_price_30d_ago) * 100
    
    industry_avg_price = industry_daily['avg_close'].mean()
    industry_max_price = industry_daily['avg_close'].max()
    industry_min_price = industry_daily['avg_close'].min()
    industry_volatility = industry_daily['avg_close'].std()
    
    industry_avg_return = industry_daily['avg_return'].mean()
    positive_industry_days = len(industry_daily[industry_daily['avg_return'] > 0])
    industry_win_rate = (positive_industry_days / len(industry_daily)) * 100
    
    avg_daily_volume = industry_daily['total_volume'].mean()
    max_daily_volume = industry_daily['total_volume'].max()
    
    # Company-specific KPIs within industry
    best_performer = industry_data.groupby('company')['close'].last().idxmax()
    worst_performer = industry_data.groupby('company')['close'].last().idxmin()
    
    # Create KPI columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Industry Avg Price",
            f"€{current_avg_price:.2f}"
        )
    
    with col2:
        st.metric(
            "Industry Win Rate",
            f"{industry_win_rate:.1f}%"
        )
        
    
    with col3:
        st.metric(
            "Avg Daily Return",
            f"{industry_avg_return:.2f}%",
            delta_color="inverse" if industry_avg_return < 0 else "normal"
        )
    
    with col4:
        st.metric(
            "Avg Daily Volume",
            f"{avg_daily_volume:,.0f}",
            help="Total industry trading volume"
        )

def industry_daily_data(df_daily, industry):
      df_daily = df_daily[df_daily['industry']==industry]

      industry_daily = (
            df_daily.groupby('date', as_index=False)
            .agg({
            'close': 'mean',
            'return': 'mean',
            'volume': 'sum',
            '1eur_usd': 'mean',
            '1eur_gbp': 'mean'
            })
            .rename(columns={
            'close': 'avg_close',
            'return': 'avg_return',
            'volume': 'total_volume'
            }))
      
      close_fig = px.line(industry_daily, x='date', y='avg_close', title='Avg. Industry Close Price')
      returns_fig = px.line(industry_daily, x='date', y='avg_return', title='Avg. Industry Returns')
      volumes_fig = px.line(industry_daily, x='date', y='total_volume', title='Total Industry Volumes')
      st.plotly_chart(close_fig, use_container_width=True)
      st.plotly_chart(returns_fig, use_container_width=True)
      st.plotly_chart(volumes_fig, use_container_width=True)

      left, right = st.columns(2)
      left.scatter_chart(industry_daily, x='avg_close', y='1eur_usd')
      right.scatter_chart(industry_daily, x='avg_close', y='1eur_gbp')

      left, right = st.columns(2)
      left.scatter_chart(industry_daily, x='avg_return', y='1eur_usd')
      right.scatter_chart(industry_daily, x='avg_return', y='1eur_gbp')

      left, right = st.columns(2)
      left.scatter_chart(industry_daily, x='total_volume', y='1eur_usd')
      right.scatter_chart(industry_daily, x='total_volume', y='1eur_gbp')



def industry_monthly_data(df_monthly, industry):
      df_monthly = df_monthly[df_monthly['industry']==industry]

      industry_monthly = (
            df_monthly.groupby('month', as_index=False)
            .agg({
            'close': 'mean',
            'return': 'mean',
            'unemployment_rate': 'mean',
            'interest_rate': 'mean'
            })
            .rename(columns={
            'close': 'avg_close',
            'return': 'avg_return'
            }))

      close_fig_month = px.line(industry_monthly, x='month', y='avg_close', title='Close Price at end of month')
      return_fig_moth = px.line(industry_monthly, x='month', y='avg_return', title='Returns (%) at end of month')
      st.plotly_chart(close_fig_month, use_container_width=True)
      st.plotly_chart(return_fig_moth, use_container_width=True)

      left, right = st.columns(2)
      left.scatter_chart(industry_monthly, x='avg_close', y='unemployment_rate')
      right.scatter_chart(industry_monthly, x='avg_close', y='interest_rate')

      left, right = st.columns(2)
      left.scatter_chart(industry_monthly, x='avg_return', y='unemployment_rate')
      right.scatter_chart(industry_monthly, x='avg_return', y='interest_rate')

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

# PREDICTIVE MODEL

# LSTM Model Class (must match training)
class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim=50, num_layers=2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# Helper functions for predictions
def inverse_transform_predictions(scaled_preds, scaler, feature_index=0):
    """Inverse transform predictions"""
    dummy = np.zeros((len(scaled_preds), scaler.n_features_in_))
    dummy[:, feature_index] = scaled_preds
    inverted = scaler.inverse_transform(dummy)
    return inverted[:, feature_index]

def load_model(ticker):
    """Load the saved model for a specific ticker"""
    try:
        # Replace dots with underscores in filename
        ticker_clean = ticker.replace(".", "_")
        model_path = f"models/lstm_model_{ticker_clean}_complete.pth"
        model_assets = torch.load(model_path, map_location=torch.device('cpu'))
        return model_assets
    except FileNotFoundError:
        st.error(f"❌ Prediction model for {ticker} not found!")
        st.info("Please make sure the model was trained and saved correctly.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model for {ticker}: {str(e)}")
        return None

def predict_future(model_assets, future_days=30):
    """Generate future predictions using loaded model"""
    try:
        model = LSTMModel(**model_assets['model_config'])
        model.load_state_dict(model_assets['model_state_dict'])
        model.eval()
        
        scaler = model_assets['scaler']
        last_sequence = model_assets['last_sequence']
        
        future_predictions = []
        current_seq = torch.tensor(last_sequence[np.newaxis, :, :], dtype=torch.float32)
        
        for _ in range(future_days):
            with torch.no_grad():
                next_pred_scaled = model(current_seq).item()
            future_predictions.append(next_pred_scaled)
            
            # Update sequence
            last_row = current_seq[0, -1, :].numpy().copy()
            new_row = last_row.copy()
            new_row[0] = next_pred_scaled  # update close price
            
            new_sequence = np.vstack([current_seq[0, 1:, :].numpy(), new_row])
            current_seq = torch.tensor(new_sequence[np.newaxis, :, :], dtype=torch.float32)
        
        # Inverse transform
        future_prices = inverse_transform_predictions(np.array(future_predictions), scaler, 0)
        return future_prices
    
    except Exception as e:
        st.error(f"❌ Error generating predictions: {str(e)}")
        return None
    
def company_predictions(df_daily, company):
    # Get ticker for this company
    ticker = df_daily[df_daily['company'] == company]['ticker'].iloc[0]
    
    st.write(f"Using LSTM neural network to predict future prices for {company} ({ticker})")
    
    # Load model
    with st.spinner("Loading prediction model..."):
        model_assets = load_model(ticker)
    
    if model_assets is None:
        return
    
    # Prediction controls
    left, right = st.columns(2)
    with left:
        future_days = st.slider("Days to predict", min_value=5, max_value=90, value=30, 
                               help="Number of trading days to forecast")
    with right:
        show_uncertainty = st.checkbox("Show uncertainty band", value=True)
    
    # Generate predictions
    if st.button("Generate Forecast", type="primary"):
        with st.spinner("Generating AI predictions..."):
            future_prices = predict_future(model_assets, future_days)
        
        if future_prices is not None:
            # Create the prediction plot
            plot_predictions(df_daily, company, ticker, future_prices, future_days, 
                           model_assets, show_uncertainty)
            
            # Show prediction statistics
            show_prediction_stats(future_prices, df_daily, company)

def plot_predictions(df_daily, company, ticker, future_prices, future_days, model_assets, show_uncertainty):
    """Create interactive prediction plot"""
    
    # Filter company data
    company_data = df_daily[df_daily['company'] == company].copy()
    company_data['date'] = pd.to_datetime(company_data['date'])
    company_data = company_data.sort_values('date')
    
    # Create future dates
    last_date = company_data['date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, future_days + 1)]
    
    # Create plot
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    # Historical data (last 60 days for context)
    historical_days = min(60, len(company_data))
    historical_data = company_data.tail(historical_days)
    
    fig.add_trace(
        go.Scatter(
            x=historical_data['date'],
            y=historical_data['close'],
            mode='lines',
            name='Historical Prices',
            line=dict(color='#1f77b4', width=3)
        )
    )
    
    # Future predictions
    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=future_prices,
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=6)
        )
    )
    
    # Uncertainty band
    if show_uncertainty:
        recent_volatility = company_data['close'].tail(20).std()
        upper_bound = future_prices + recent_volatility
        lower_bound = future_prices - recent_volatility
        
        fig.add_trace(
            go.Scatter(
                x=future_dates + future_dates[::-1],
                y=np.concatenate([upper_bound, lower_bound[::-1]]),
                fill='toself',
                fillcolor='rgba(255, 165, 0, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Uncertainty Band',
                showlegend=True
            )
        )
    
    # Vertical line separating history from forecast
    fig.add_vline(
        x=last_date.timestamp() * 1000,  # Convert to milliseconds for Plotly
        line_dash="dash", 
        line_color="gray",
        annotation_text="Forecast Start"
    )
    
    fig.update_layout(
        title=f"{company} ({ticker}) - {future_days}-Day Price Forecast",
        xaxis_title="Date",
        yaxis_title="Price (EUR)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_prediction_stats(future_prices, df_daily, company):
    """Display prediction statistics"""
    st.subheader("📊 Forecast Summary")
    
    # Get current price
    company_data = df_daily[df_daily['company'] == company].copy()
    company_data['date'] = pd.to_datetime(company_data['date'])
    current_price = company_data['close'].iloc[-1]
    forecast_final = future_prices[-1]
    
    # Calculate changes
    price_change = forecast_final - current_price
    pct_change = (price_change / current_price) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price", 
            f"€{current_price:.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            f"Forecast ({len(future_prices)} days)", 
            f"€{forecast_final:.2f}"
        )
    
    with col3:
        st.metric(
            "Expected Change", 
            f"{pct_change:.1f}%",
            delta_color="inverse" if pct_change < 0 else "normal"
        )
    
    with col4:
        avg_forecast = np.mean(future_prices)
        st.metric(
            "Average Forecast", 
            f"€{avg_forecast:.2f}"
        )
    
    # Additional insights
    st.info(f"""
    **Insights:**
    - The AI model predicts the price will range from **€{min(future_prices):.2f}** to **€{max(future_prices):.2f}**
    - Forecast trend: {'📈 Bullish' if pct_change > 0 else '📉 Bearish' if pct_change < 0 else '➡️ Neutral'}
    - *Note: AI predictions are based on historical patterns and should not be used as financial advice*
    """)

def industry_predictions(df_daily, industry, companies):
    st.subheader("🏭 Industry-wide AI Predictions")
    
    st.write(f"Showing AI predictions for all companies in the {industry} industry")
    
    # Load models for all companies in this industry
    models_loaded = []
    for company in companies:
        ticker = df_daily[df_daily['company'] == company]['ticker'].iloc[0]
        model_assets = load_model(ticker)
        if model_assets is not None:
            models_loaded.append({
                'company': company,
                'ticker': ticker,
                'model_assets': model_assets
            })
    
    if not models_loaded:
        st.error("No prediction models available for companies in this industry.")
        return
    
    st.success(f"✅ Loaded {len(models_loaded)} prediction models")
    
    # Prediction controls
    future_days = st.slider("Days to predict", min_value=5, max_value=60, value=30, 
                           key="industry_days")
    
    if st.button("Generate Industry Forecast", type="primary"):
        with st.spinner("Generating industry-wide predictions..."):
            # Generate predictions for all companies
            predictions = []
            for model_info in models_loaded:
                future_prices = predict_future(model_info['model_assets'], future_days)
                if future_prices is not None:
                    predictions.append({
                        'company': model_info['company'],
                        'ticker': model_info['ticker'],
                        'current_price': df_daily[df_daily['company'] == model_info['company']]['close'].iloc[-1],
                        'future_prices': future_prices,
                        'final_forecast': future_prices[-1],
                        'pct_change': (future_prices[-1] - df_daily[df_daily['company'] == model_info['company']]['close'].iloc[-1]) / df_daily[df_daily['company'] == model_info['company']]['close'].iloc[-1] * 100
                    })
        
        if predictions:
            # Create industry summary
            plot_industry_summary(predictions, future_days)
            
            # Show individual company predictions in a table (no nested expanders)
            st.subheader("Company Forecasts Summary")
            
            # Create a styled dataframe
            summary_data = []
            for pred in predictions:
                summary_data.append({
                    'Company': pred['company'],
                    'Ticker': pred['ticker'],
                    'Current Price (€)': pred['current_price'],
                    f'{future_days}-Day Forecast (€)': pred['final_forecast'],
                    'Change (%)': pred['pct_change'],
                    'Trend': 'Bullish 📈' if pred['pct_change'] > 1 else 'Bearish 📉' if pred['pct_change'] < -1 else 'Neutral ➡️'
                })
            
            summary_df = pd.DataFrame(summary_data)
            
            # Display with some styling
            st.dataframe(
                summary_df.style.format({
                    'Current Price (€)': '{:.2f}',
                    f'{future_days}-Day Forecast (€)': '{:.2f}',
                    'Change (%)': '{:.1f}%'
                }).background_gradient(
                    subset=['Change (%)'], 
                    cmap='RdYlGn',  # Red-Yellow-Green
                    vmin=-10, 
                    vmax=10
                ),
                use_container_width=True,
                height=400
            )
      
            st.info(f"""
            - *Note: AI predictions are based on historical patterns and should not be used as financial advice*
            """)

def plot_industry_summary(predictions, future_days):
    """Create industry summary plot"""
    
    # Prepare data for plotting
    companies = [p['company'] for p in predictions]
    current_prices = [p['current_price'] for p in predictions]
    forecast_prices = [p['final_forecast'] for p in predictions]
    pct_changes = [p['pct_change'] for p in predictions]
    
    # Create summary dataframe
    summary_df = pd.DataFrame({
        'Company': companies,
        'Current Price': current_prices,
        f'{future_days}-Day Forecast': forecast_prices,
        'Percentage Change': pct_changes
    })
    
    # Sort by percentage change
    summary_df = summary_df.sort_values('Percentage Change', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        summary_df, 
        x='Company', 
        y='Percentage Change',
        color='Percentage Change',
        color_continuous_scale=['red', 'lightgray', 'green'],
        title=f'Industry Outlook: Expected {future_days}-Day Price Changes'
    )
    
    fig.update_layout(
        xaxis_title="Company",
        yaxis_title="Expected Change (%)",
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    avg_change = np.mean(pct_changes)
    bullish_companies = len([p for p in pct_changes if p > 0])
    bearish_companies = len([p for p in pct_changes if p < 0])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Expected Change", f"{avg_change:.1f}%")
    with col2:
        st.metric("Bullish Companies", bullish_companies)
    with col3:
        st.metric("Bearish Companies", bearish_companies)