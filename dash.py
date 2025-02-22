import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import ta
import re
import numpy as np
import json
import runpy

# Configurar a página
st.set_page_config(page_title="Análise de Ações B3", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .main {background-color: #F5F5F5;}
    .stSelectbox label {font-size: 18px;}
    .metric {padding: 15px; background-color: white; border-radius: 10px; margin: 5px;}
</style>
""", unsafe_allow_html=True)

# Carregar os tickers do arquivo JSON
with open('tickers_ibov.json', 'r') as file:
    TICKERS = json.load(file)

# Acessar o ticker padrão
default_ticker = 'BBAS3.SA'
print(f'Ticker padrão: {default_ticker}, Nome: {TICKERS[default_ticker]}')


def get_stock_data(ticker, start_date, end_date):
    """Obtém dados de ações do Yahoo Finance dentro de um intervalo de datas"""
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

def format_currency(value):
    """Formata o valor como moeda"""
    return f'R$ {value:,.2f}' if value else 'NA'

# Barra lateral
st.sidebar.header("Seleção de ativo")
selected_ticker = st.sidebar.selectbox(
    "Selecione um ativo:",
    options=list(TICKERS.keys()),
    format_func=lambda x: f"{TICKERS[x]} ({x})"
)

# Seleção de data para dados históricos
st.sidebar.subheader("Selecione o intervalo de datas")
start_date = st.sidebar.date_input("Data de Início", pd.to_datetime('2024-01-01'))
end_date = st.sidebar.date_input("Data de Fim", pd.to_datetime('today'))

def calcular_indicadores(df):
    """Calcula indicadores técnicos e retorna o DataFrame atualizado"""
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)  # Índice de Força Relativa (RSI)

    df['Volume_Media_20'] = df['Volume'].rolling(20).mean()  # Média móvel do volume nos últimos 20 dias
    df['Volume_Anormal'] = df['Volume'] > (df['Volume_Media_20'] * 2)  # Volume considerado anormal

    df['Volatilidade_20'] = df['Close'].pct_change().rolling(20).std() * np.sqrt(252)  # Volatilidade anualizada com base em 20 dias

    return df

# Texto que contém o nome e o ticker
header_text = f"Análise do ativo: {TICKERS[selected_ticker]} ({selected_ticker})"

# Conteúdo principal
st.header(header_text)

# Expressão regular para capturar o conteúdo dentro dos parênteses
match = re.search(r"\((.*?)\)", header_text)

if match:
    ticker_full = match.group(1)  # Captura "PETR4.SA"
    ticker_code = ticker_full.split('.')[0]  # Remove ".SA"
else:
    ticker_code = None  # Caso não encontre o formato esperado

# Obter dados da ação com o intervalo de datas selecionado
hist = get_stock_data(selected_ticker, start_date, end_date)
hist = calcular_indicadores(hist)

# Exibir informações básicas sobre a ação
stock = yf.Ticker(selected_ticker)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Preço Atual", format_currency(stock.info.get('regularMarketPrice', 'N/A')))  # Preço de mercado atual
with col2:
    st.metric("P/L", f"{stock.info.get('trailingPE', 'N/A')}")  # Índice Preço/Lucro (P/L)

# Verificando se o DataFrame 'hist' contém dados suficientes
if len(hist) > 0:
    # Verificando se há dados suficientes para acessar a última linha
    if len(hist['Volatilidade_20']) > 0:
        with col3:
            st.metric("Volatilidade (20d)", f"{hist['Volatilidade_20'].iloc[-1]:.2%}")  # Volatilidade baseada nos últimos 20 dias
    else:
        with col3:
            st.metric("Volatilidade (20d)", "N/A")  # Se não houver dados, exibe N/A

    if len(hist['RSI']) > 0:
        with col4:
            st.metric("RSI (14)", f"{hist['RSI'].iloc[-1]:.2f}")  # Índice de Força Relativa (RSI) de 14 períodos
    else:
        with col4:
            st.metric("RSI (14)", "N/A")  # Se não houver dados, exibe N/A

    with col5:
        st.metric("52 Semanas Alta", format_currency(stock.info.get('fiftyTwoWeekHigh', 'N/A')))  # Máxima de 52 semanas
else:
    st.warning("Nenhum dado histórico disponível para o ativo selecionado. Verifique gráfico Trading View abaixo.")

# HTML do widget de gráfico do TradingView
tradingview_widget = f"""
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_c3f01&symbol={ticker_code}&interval=D&theme=dark"
    width="100%" height="500" frameborder="0" allowtransparency="true"></iframe>
"""

st.components.v1.html(tradingview_widget, height=500)

# Layout Informações Fundamentais + Volume Anormal
col1, col2 = st.columns([1, 1.1])

# 📊 Coluna 1 - Informações Fundamentais
with col1:
    st.subheader("Informações Fundamentais")
    fundamentals = {
        'Empresa': stock.info.get('longName'),
        'Setor': stock.info.get('sector'),
        'EBITDA': format_currency(stock.info.get('ebitda')),
        'LPA': format_currency(stock.info.get('trailingEps')),
        'Valor de Mercado': format_currency(stock.info.get('marketCap'))
    }
    st.json(fundamentals)

# 📈 Coluna 2 - Volume Anormal
with col2:
    st.subheader("📊 Volume Anormal")
    fig_volume = go.Figure()

    # Gráfico de volume diário
    fig_volume.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name="Volume", marker=dict(color='blue')))

    # Destacar dias com volume anormal
    volume_anormal = hist[hist['Volume_Anormal']]
    fig_volume.add_trace(go.Bar(x=volume_anormal.index, y=volume_anormal['Volume'], name="Volume Anormal", marker=dict(color='red')))

    # Ajuste do tamanho do gráfico
    fig_volume.update_layout(
        height=300,
        width=600,
        showlegend=True
    )
    st.plotly_chart(fig_volume, use_container_width=False)

# Calcular EV/EBITDA
def calculate_ev_ebitda(ticker):
    stock = yf.Ticker(ticker)
    market_cap = stock.info.get('marketCap', 0)
    total_debt = stock.info.get('totalDebt', 0)
    cash = stock.info.get('cash', 0)
    ev = market_cap + total_debt - cash

    # Obter o EBITDA
    ebitda = stock.info.get('ebitda', 0)

    # Calcular EV/EBITDA
    if ebitda != 0:  # Evitar divisão por zero
        ev_ebitda = ev / ebitda
    else:
        ev_ebitda = None

    return ev_ebitda

ev_ebitda = calculate_ev_ebitda(selected_ticker)
if ev_ebitda is not None:
    st.success(f"O EV/EBITDA da empresa {selected_ticker} é: {ev_ebitda:.2f}")
else:
    st.write(f" ")


# Gráfico de preços históricos
st.subheader("Histórico de Preços")
fig = go.Figure()
fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Preço Fechamento'))  # Preço de fechamento da ação
fig.update_layout(height=400, showlegend=True)
st.plotly_chart(fig, use_container_width=True)


