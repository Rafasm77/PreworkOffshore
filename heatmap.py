import streamlit as st

st.set_page_config(page_title="Mapa de Calor IBOV", layout="wide")

st.title("📈 Mapa de calor de ações IBOV")

# HTML do widget de mapa de calor do TradingView
heatmap_widget = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
    </a>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
  {
    "exchanges": [],
    "dataSource": "IBOV",
    "grouping": "sector",
    "blockSize": "market_cap_basic",
    "blockColor": "change",
    "locale": "en",
    "symbolUrl": "",
    "colorTheme": "light",
    "hasTopBar": false,
    "isDataSetEnabled": false,
    "isZoomEnabled": true,
    "hasSymbolTooltip": true,
    "isMonoSize": false,
    "width": "100%",
    "height": "500"
  }
  </script>
</div>
"""

# Exibir o widget dentro da página
st.components.v1.html(heatmap_widget, height=600)
