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
st.set_page_config(page_title='Países', page_icon='🌍', layout='wide')

st.header('Vorges Eat Marktplace: Dashboard Países')


# CSS Style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    

#============================= Imagem Inicial ==========================
image = Image.open('countries.jpg')
st.image(image, caption= 'Urban Cafe, Tehran, Iran', width=620)

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

# Filtro 1
countries = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar:',
    df2.loc[:,'country'].unique().tolist(),
    default=['Brazil','England','Qatar','South Africa','Canada','Australia']
)
st.sidebar.markdown("""---""")

# Filtro 2
price_type_filter = st.sidebar.multiselect(
    'Escolha o Tipo de Preço Avaliado:',
    df2.loc[:,'price_type'].unique().tolist(),
    default = ['expensive', 'gourmet', 'normal', 'cheap']
)
st.sidebar.markdown("""---""")

#========================================================================
#========================== Ativando filtros ============================
#========================================================================

# Filtro 1
linhas_selecionadas_countries = df2['country'].isin( countries )
df2 = df2.loc[linhas_selecionadas_countries, :]

# Filtro 2
linhas_selecionadas_price = df2['price_type'].isin( price_type_filter )
df2 = df2.loc[linhas_selecionadas_price, :]

#========================================================================
#========================== Layout no Streamlit =========================
#========================================================================
st.markdown('### Onde nossos restaurantes parceiros estão localizados?')


#========================= METRICAS (CARTÃO)
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dist_restaurant = df2['restaurant_id'].shape[0]
        col1.metric('Restaurante Únicos', dist_restaurant)
        
    
    with col2:
        dist_country = df2.loc[:, 'country'].nunique()
        col2.metric('Países Registrados', dist_country)
    
    
    with col3:
        dist_city = df2.loc[:, 'city'].nunique()
        col3.metric('Cidades Registradas', dist_city)
        
    
    with col4:
        dist_cuisine = df2.loc[:, 'cuisines'].nunique()
        col4.metric('Tipos Culinários', dist_cuisine)
        

#===========================  DESENHAR O MAPA
def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)
    
map_df = df2.loc[df2["country"].isin(countries), :]

create_map(map_df)
#=================================================================================

with st.container():
    # GRAFICO 1
    cols = ['restaurant_id','country']
    
    aux = ( df2.loc[:, cols].groupby('country')
                            .nunique()
                            .sort_values('restaurant_id', ascending= False)
                            .reset_index() )
    
    fig = px.bar( aux, x='country', y='restaurant_id', 
                       text='restaurant_id', 
                       title='Quantidade de Restaurantes por País', 
                       labels={'country': 'País', 'restaurant_id': 'Qtde Restaurantes'})
    
    st.plotly_chart(fig)
#=======================================================
    # GRAFICO 2
    cols = ['city','country']

    aux = ( df2.loc[:, cols].groupby('country')
                          .nunique()
                          .sort_values('city', ascending = False)
                          .reset_index() )

    fig = px.bar(aux, x='country', 
                  y='city', 
                  labels={'country': 'País', 'city': 'Cidade'},
                  color="country",
                  title='Quantidade de cidades registradas por País')

    st.plotly_chart(fig)
#=======================================================
    # GRAFICO 3
    cols = ['votes','country']

    aux = ( df2.loc[:, cols].groupby('country')
                          .mean()
                          .sort_values('votes', ascending = False)
                          .reset_index() )

    fig = px.bar( aux, x='country', 
                      y='votes',  
                      title='Média de Avaliações',
                      color="country",
                      labels={'country':'País', 'votes':'Média Avaliação'} )

    st.plotly_chart(fig)
#=======================================================
    # GRAFICO 4
    cols = ['average_cost_for_two','country']

    aux = ( df2.loc[:, cols].groupby('country')
                          .mean()
                          .sort_values('average_cost_for_two', ascending = False)
                          .reset_index() )

    fig = px.bar(aux, 
             x='country', 
             y='average_cost_for_two', 
             labels={'country':'País', 'average_cost_for_two':'Média de Preço de um prato para duas pessoas'}, 
            color="country",
             title='Média de Preço de um prato para duas pessoas')

    st.plotly_chart(fig)
#=======================================================
    # GRAFICO 5
    cols = ['aggregate_rating', 'country']

    aux= ( df2.loc[:, cols].groupby('country')
                         .mean()
                         .sort_values('aggregate_rating', ascending = False)
                         .reset_index() )

    fig = px.scatter( aux, 
           x='country', 
           y='aggregate_rating', 
           color='country',
           title = 'Média da Nota dos Restaurantes por País',
           labels={'country':'País','aggregate_rating':'Média da Nota do Restaurante'} )

    st.plotly_chart(fig)
    
    st.markdown(
    """
    ##### Observação:
    - **Indonésia** é o país com a maior nota média de avaliação com 4.60 seguido da **Filipinas** com nota média de 4.46, por outro lado, o **Brasil** é o país com menor nota média.
    
    """
)
