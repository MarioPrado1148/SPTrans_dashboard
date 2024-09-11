import streamlit as st
import pandas as pd
import random
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px

# Função para gerar dados simulados da SPTrans
@st.cache_data
def gerar_dados_sptrans_simulados(n_linhas=5, n_onibus=30):
    linhas = [f'{random.randint(1000,9999)}-{random.randint(10,99)}' for _ in range(n_linhas)]
    destinos = ['Terminal A', 'Terminal B', 'Centro', 'Bairro X', 'Bairro Y']

    data = {
        'linha': np.random.choice(linhas, n_onibus),
        'onibus_id': [random.randint(10000, 99999) for _ in range(n_onibus)],
        'latitude': [np.random.uniform(-23.7, -23.5) for _ in range(n_onibus)],  # São Paulo
        'longitude': [np.random.uniform(-46.7, -46.5) for _ in range(n_onibus)],
        'destino': np.random.choice(destinos, n_onibus),
        'horario_atualizacao': pd.date_range('2024-09-10 08:00', periods=n_onibus, freq='T').strftime('%Y-%m-%d %H:%M:%S'),
        'previsao_chegada': pd.date_range('2024-09-10 08:10', periods=n_onibus, freq='T').strftime('%Y-%m-%d %H:%M:%S')
    }

    df_simulado = pd.DataFrame(data)
    return df_simulado

# Função para criar o mapa com Folium
@st.cache_data
def criar_mapa(dados):
    mapa = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)
    for index, row in dados.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Linha: {row['linha']}<br>Destino: {row['destino']}<br>Chegada: {row['previsao_chegada']}",
            icon=folium.Icon(color="blue", icon="bus", prefix="fa")
        ).add_to(mapa)
    return mapa

# Função para criar gráfico de Linha x Horário de Chegada com Plotly
def plot_linha_horario(dados):
    fig = px.line(dados, x='previsao_chegada', y='linha', title="Horário de Chegada x Linha de Ônibus", labels={'previsao_chegada': 'Horário de Chegada', 'linha': 'Linha'})
    return fig

# Função para criar gráfico de Atraso por Linha com Plotly
def plot_atraso_linha(dados):
    # Simular atraso nos horários de chegada
    dados['tempo_real'] = pd.to_datetime(dados['previsao_chegada']) + pd.to_timedelta(np.random.randint(-5, 10, size=len(dados)), unit='m')
    dados['atraso'] = (pd.to_datetime(dados['tempo_real']) - pd.to_datetime(dados['previsao_chegada'])).dt.total_seconds() / 60.0
    fig = px.bar(dados, x='linha', y='atraso', title="Atraso Médio por Linha de Ônibus", labels={'linha': 'Linha', 'atraso': 'Atraso (minutos)'})
    return fig

# Função para criar gráfico de Pizza com Plotly
def plot_pizza_destino(dados):
    fig = px.pie(dados, names='destino', title="Proporção de Ônibus por Destino")
    return fig

# Título da aplicação
st.title("Dados Simulados de Ônibus - SPTrans - FIA")

# Barra lateral para selecionar a visualização
menu = st.sidebar.radio("Escolha a visualização:", ["Tabela", "Mapa Interativo", "Linha x Horário de Chegada", "Atraso por Linha", "Proporção de Ônibus por Destino"])

# Gerar dados simulados
dados_simulados = gerar_dados_sptrans_simulados()

# Mostrar visualizações com base na seleção do usuário
if menu == "Tabela":
    st.subheader("Tabela de Dados Simulados")
    st.dataframe(dados_simulados)

elif menu == "Mapa Interativo":
    st.subheader("Mapa dos Ônibus Simulados")
    mapa = criar_mapa(dados_simulados)
    st_folium(mapa, width=700, height=500)

elif menu == "Linha x Horário de Chegada":
    st.subheader("Gráfico de Linha x Horário de Chegada")
    fig = plot_linha_horario(dados_simulados)
    st.plotly_chart(fig)

elif menu == "Atraso por Linha":
    st.subheader("Gráfico de Atraso por Linha")
    fig = plot_atraso_linha(dados_simulados)
    st.plotly_chart(fig)

elif menu == "Proporção de Ônibus por Destino":
    st.subheader("Gráfico de Proporção de Ônibus por Destino")
    fig = plot_pizza_destino(dados_simulados)
    st.plotly_chart(fig)
