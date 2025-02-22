import streamlit as st
import feedparser
from datetime import datetime
import time

# CSS
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

# Função para exibir notícias
def display_news():

    update_placeholder = st.empty()
    
    while True:
        with update_placeholder.container():
            
            last_updated = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            print(f"Página atualizada às {last_updated}")

            news_items = get_news()

            st.subheader("📢 Notícias")

            # Limitar a exibição a 20 notícias
            max_news = 20
            news_count = 0

            if news_items:
                for news in news_items[:max_news]:
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
                st.error("Não foi possível carregar as notícias.")
        
        # Espera 30 segundos e atualiza a página automaticamente
        time.sleep(30)
        

# Exibir as notícias e a mensagem de atualização
display_news()
