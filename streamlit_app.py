import streamlit as st
import pandas as pd
import random
import numpy as np
import folium
from streamlit_folium import st_folium

# Função para gerar dados simulados da SPTrans
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

# Título da aplicação
st.title("Dados Simulados de Ônibus - SPTrans")

# Gerar dados simulados
dados_simulados = gerar_dados_sptrans_simulados()

# Exibir os dados na aplicação (tabela)
st.subheader("Tabela de Dados Simulados")
st.dataframe(dados_simulados)

# Criar o mapa
st.subheader("Mapa dos Ônibus Simulados")
mapa = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)

# Adicionar os pontos dos ônibus ao mapa
for index, row in dados_simulados.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Linha: {row['linha']}<br>Destino: {row['destino']}<br>Chegada: {row['previsao_chegada']}",
        icon=folium.Icon(color="blue", icon="bus", prefix="fa")
    ).add_to(mapa)

# Mostrar o mapa interativo no Streamlit
st_folium(mapa, width=700, height=500)
