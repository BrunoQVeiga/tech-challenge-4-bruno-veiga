import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Introdução",
        page_icon="🛢️",  # Emoji de barril de petróleo como ícone da página
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Adicionar um header colorido
    st.markdown(
        """
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            color: #FF6347;  # Cor tomate
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<p class="big-font">Análise Dinâmica do Preço do Petróleo Brent 🌍⛽</p>', unsafe_allow_html=True)

    # Adicionar um texto mais atraente e informativo
    st.markdown(
        """
        📈 **Explore o volátil mundo dos preços do petróleo Brent!** Desde fatores geopolíticos até mudanças econômicas,
        o preço do barril é um verdadeiro termômetro global. Durante essa análse, você não apenas visualizará 
        o histórico de preços do petróleo, mas também terá a oportunidade de realizar previsões futuras com o auxílio de
        **Inteligência Artificial**!
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run()
