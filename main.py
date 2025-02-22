import streamlit as st

dash = st.Page("dash.py", title="Dash - Análise de ativos")
news = st.Page("news2.py", title="Notícias")
heatmap = st.Page("heatmap.py", title="HeatMap IBOV")

pg = st.navigation([dash, news, heatmap])
pg.run()