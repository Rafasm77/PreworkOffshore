import streamlit as st
import feedparser
import time

# Aplicando CSS para reduzir fonte e espaçamento
st.markdown("""
    <style>
        .news-title {
            font-size: 16px !important;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .news-date {
            font-size: 12px;
            color: gray;
            margin-bottom: 5px;
        }
        .news-leiamais {
            font-size: 12px;
            color: gray;
            margin-bottom: 1px;
        }
        .news-container {
            margin-bottom: 1px; 
        }
    </style>
""", unsafe_allow_html=True)

# URL dos feeds RSS
def get_news():
    rss_urls = [
        "https://br.investing.com/rss/news_25.rss",
        "https://br.investing.com/rss/stock_stock_picks.rss",
        "https://br.investing.com/rss/stock_Opinion.rss",
        "https://finance.yahoo.com/rss/",
        "https://www.infomoney.com.br/feed/",
        "https://pox.globo.com/rss/valor"
    ]
    
    all_entries = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        all_entries.extend(feed.entries)
    
    return all_entries

# Obtendo as notícias
news_items = get_news()

st.subheader("📢 Notícias")

# Limitar a exibição a 20 notícias
max_news = 20
news_count = 0

if news_items:
    for news in news_items:
        if news_count < max_news:
            st.markdown(f'<div class="news-container">', unsafe_allow_html=True)

            # Título com fonte menor
            st.markdown(f'<div class="news-title">{news.title}</div>', unsafe_allow_html=True)

            # Data em cinza
            st.markdown(f'<div class="news-date">{news.published}</div>', unsafe_allow_html=True)

            # Link para a notícia
            st.markdown(f'<div class="news-leiamais"><a href="{news.link}" target="_blank">Leia mais</a></div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.divider()  

            news_count += 1
        else:
            break
else:
    st.error("Não foi possível carregar as notícias.")

 # Atualiza a página a cada 30 segundos
    time.sleep(30)
    st.experimental_rerun()