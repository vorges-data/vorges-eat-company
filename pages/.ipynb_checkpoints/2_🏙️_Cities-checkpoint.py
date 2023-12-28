# Libraries
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#========================================================================
#==================== Variáveis Auxiliares ==============================
#========================================================================
FILE_PATH = '/home/vinicius/repos/projeto_ftc_vorges/datasets/zomato.csv'

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}


COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

#========================================================================
#==================== Funções Auxiliares ================================
#========================================================================

# renomear as colunas em snakecase
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    return df

# Substituir o código do país pelo seu nome
def country_name(country_id):
    return COUNTRIES[country_id]


# Substituir o código da cor por seu nome
def color_name(color_code):
    return COLORS[color_code]

# Substituir o price_range pelas nomes
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
# Ajustar as ordens das colunas
def adjust_columns_order(dataframe):
    df = dataframe.copy()
    new_cols_order = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "address",
        "locality",
        "locality_verbose",
        "longitude",
        "latitude",
        "cuisines",
        "price_type",
        "average_cost_for_two",
        "currency",
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "aggregate_rating",
        "rating_color",
        "color_name",
        "rating_text",
        "votes",
    ]
    return df.loc[:, new_cols_order]

# Processar e ransformar os dados
def process_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna()
    df = rename_columns(df)
    df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_tye(x))
    df["country"] = df.loc[:, "country_code"].apply(lambda x: country_name(x))
    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    df = df.drop_duplicates()
    df = adjust_columns_order(df)
    df.to_csv('/home/vinicius/repos/projeto_ftc_vorges/datasets/data_processed.csv', index=False)
    return df

# Carregar os dados
df_raw = pd.read_csv(FILE_PATH)

# Copy
df1 = df_raw.copy()

# Chamar a função para renomear as colunas
df1 = rename_columns( df1 )


# Chamar a função para processar os dados
df2 = process_data(FILE_PATH)

#========================================================================
#========================== Menu Lateral ================================
#========================================================================
st.set_page_config(page_title='Cidades', page_icon='🏙️', layout='wide')

st.header('Vorges Eat Marktplace: Dashboard Cidades')


#============================= Imagem Inicial ==========================
image = Image.open('cities.jpg')
st.image(image, caption= 'New York, United States', width=620)

st.markdown("""---""")

#===========================
# Criar o menu lateral
#===========================
image = Image.open('Logo Preto Sem Fundo.png')
st.sidebar.image( image, width = 120)

st.sidebar.markdown('# Vorges Eat')
st.sidebar.markdown('## Seu Marketplace de Restaurantes')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filtros')

# Filtro
countries = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar:',
    df2.loc[:,'country'].unique().tolist(),
    default=['Brazil','England','Qatar','South Africa','Canada','Australia']
)
st.sidebar.markdown("""---""")

st.sidebar.selectbox(
    'Tipo de Preço Avaliado:',
    df2.loc[:,'price_type'].unique().tolist()
    #default = ['expensive', 'gourmet', 'normal', 'cheap']
)
st.sidebar.markdown("""---""")