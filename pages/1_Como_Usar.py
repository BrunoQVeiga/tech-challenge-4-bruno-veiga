from typing import Any
import numpy as np
import streamlit as st

# Configurando a página do Streamlit
def como_usar():
    st.set_page_config(
        page_title="Como Usar",
        page_icon="📘",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title('🛢️ Preço Diário do Barril de Petróleo Brent')

    # Adicionar um header colorido e informativo
    st.markdown(
        """
        <style>
        .info-font {
            font-size:20px;
            color: #2E8B57;  # Cor verde mar
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<p class="info-font">🚀 Modelo de Predição Diária - Preço do Petróleo (IPEA)</p>', unsafe_allow_html=True)

    st.markdown("""
    A aplicação segue um fluxo interativo para estimar o preço diário do barril de petróleo Brent. 
    Vamos guiá-lo através de cada etapa necessária para obter e visualizar as previsões!
    """, unsafe_allow_html=True)

    # Link com estilo
    st.markdown("""
    Os dados são carregados automaticamente da página do IPEA:
                
    -> [Acesse os dados aqui](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)
    
    Utilizamos técnicas avançadas de Machine Learning para prever os valores diários do preço do barril de petróleo Brent.
    """, unsafe_allow_html=True)

    st.subheader('🔍 Como funciona?')

    st.markdown("""
    1. **Navegue até a página de execução do modelo.**
    2. **Clique no botão para iniciar a busca dos dados via web scraping.**
    3. **Selecione o intervalo de tempo para a previsão.**
    4. **Execute o modelo.**
    5. **Visualize os resultados através de dataframes ou gráficos.**
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; color: blue;'>
        <strong>Todos os dados estão disponíveis para download, para que você possa analisá-los como preferir!</strong>
    </div>
    """, unsafe_allow_html=True)

# Executando a aplicação
if __name__ == "__main__":
    como_usar()

