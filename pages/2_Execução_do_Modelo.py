import json
import numpy as np
import pandas as pd
import requests
import streamlit as st
from datetime import datetime
import pickle
from prophet import *
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Configuração inicial de estado no Streamlit
def initialize_state():
    if "df_base" not in st.session_state:
        st.session_state.df_base = None

    if 'loaded_model' not in st.session_state:
        with open('models/prophet_model.pkl', 'rb') as file:
            st.session_state.loaded_model = pickle.load(file)

    if 'model_clicked' not in st.session_state:
        st.session_state.model_clicked = False

    if 'processed_df' not in st.session_state:
        st.session_state.processed_df = None

def load_data():
    st.write("Carregando dados do IPEA...")
    url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"
    response = requests.get(url)
    dfs = pd.read_html(response.text, attrs={'id': 'grd_DXMainTable'})
    if len(dfs) > 0:
        df = dfs[0]
        df.columns = ['Data', 'Preco']
        df.to_csv('preco_petroleo_brent_atualizado.csv', index=False, encoding='utf-8')
        df = pd.read_csv('preco_petroleo_brent_atualizado.csv')        
        df = df.drop(0)
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
        df = df.reset_index(drop=True).sort_values(by="Data", ascending=False)
        df['Preco'] = df['Preco'].astype(int) / 100
        df = df.rename(columns={'Data':'ds', 'Preco': 'y'})
        df = df[['ds', 'y']]
        df.set_index('ds', inplace=True)

        df_diario = df.asfreq('D').fillna(method='bfill')
        df_diario = df_diario.reset_index()

        st.success("Dados carregados com sucesso!")
        return df_diario
    else:
        print("Nenhuma tabela encontrada.")
        return None

def execute_model(df, periods):
    future_dates = pd.date_range(start=df['ds'].max(), periods=periods, freq='D')
    future_df = pd.DataFrame(future_dates, columns=['ds'])
    forecast = st.session_state.loaded_model.predict(future_df)
    return forecast[['ds', 'yhat']]

def combine_real_predicted_data(real, predicted):
    combined = pd.merge(real, predicted, on='ds', how='outer', suffixes=('', '_pred'))
    combined['y'] = combined['y'].fillna(combined['yhat'])
    combined['Data Type'] = 'Real'
    combined.loc[combined['yhat'].notna(), 'Data Type'] = 'Predicted'
    return combined[['ds', 'y', 'Data Type']]

def visualize_data(df, data_escolhida):
    # Data específica para mudar a cor
    df = df[df['ds'] >= data_escolhida]
    data_limite = df[df['Data Type'] == 'Real']['ds'].max()

    # Criação do gráfico de linha interativo usando Plotly Express
    fig = px.line(df, x='ds', y='y', color='Data Type',
                  color_discrete_map={
                      'Real': '#3071f2',  # Azul para valores reais
                      'Predicted': '#f2a20c'  # Laranja para valores preditos
                  },
                  labels={
                      'ds': 'Data',
                      'y': 'Valor'
                  },
                  title='Visualização Dados Reais x Dados Preditos')

    # Linha de transição
    fig.add_vline(x=data_limite, line_width=2, line_dash="dash", line_color="gray")

    # Adiciona anotação para data de transição
    fig.add_annotation(x=data_limite, y=df['y'].min(), text="Data de Transição: {}".format(data_limite.strftime('%d-%m-%Y')),
                       showarrow=True, arrowhead=1, yshift=10)

    # Configurações adicionais de layout
    fig.update_layout(xaxis_title='Data',
                      yaxis_title='Valor ($)',
                      legend_title='Tipo de Dado',
                      xaxis_rangeslider_visible=True)  # Habilita o slider para navegação

    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)

# Página Streamlit
st.title("🔄 Etapa de Carregamento e Previsão dos Dados")
st.markdown("Siga os passos abaixo para carregar os dados, configurar e executar o modelo de previsão:")

initialize_state()

if st.button('Carregar Dados'):
    df_base = load_data()
    if df_base is not None:
        st.session_state.df_base = df_base
        st.session_state.model_clicked = True

if st.session_state.model_clicked:
    st.subheader("Configuração do Modelo")
    days = st.slider('Número de Dias para Previsão', 1, 365, 30)
    if st.button("Executar Modelo"):
        predictions = execute_model(st.session_state.df_base, days)
        st.session_state.processed_df = combine_real_predicted_data(st.session_state.df_base, predictions)
        st.success("Modelo executado com sucesso!")

if st.session_state.processed_df is not None:
    st.subheader("Visualização dos Dados")
    st.subheader("A partir de qual ano quer visualizar os dados?")
    ano_escolhido = st.slider('Escolha o ano', 1980, 2024, 2023)

    # Converter o ano escolhido para o formato de data, considerando o primeiro dia do ano
    data_escolhida = pd.to_datetime(f"{ano_escolhido}-01-01")

    if st.button('Visualizar Gráfico'):
        # Filtrar o dataframe antes de visualizar
        visualize_data(st.session_state.processed_df, data_escolhida)

if st.session_state.processed_df is not None:
    # Botão para baixar o dataframe processado em formato CSV
    csv = st.session_state.processed_df.to_csv(index=False)  # Converter dataframe para CSV sem o índice
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='dados_previstos.csv',
        mime='text/csv',
    )
