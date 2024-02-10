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
FILE_PATH = 'datasets/zomato.csv'

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
    df.to_csv('datasets/data_processed.csv', index=False)
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
st.set_page_config(page_title='Culinaria', page_icon='🍽️', layout='wide')

st.header('Vorges Eat Marktplace: Dashboard Tipo Culinário')


#============================= Imagem Inicial ==========================
image = Image.open('culinary.jpg')
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

#============================================================================

# Filtro 1
countries = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar:',
    df2.loc[:,'country'].unique().tolist(),
    default=['Brazil','England','Qatar','South Africa','Canada','Australia']
)
st.sidebar.markdown("""---""")

# Filtro 2
price_type_filter = st.sidebar.multiselect(
    'Escolja o Tipo de Preço Avaliado:',
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

# Funções auxiliares para criação dos gráficos
def top_cuisines():

    cuisines = {
        "Italian": "",
        "American": "",
        "Arabian": "",
        "Japanese": "",
        "Brazilian": "",
    }

    cols = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "cuisines",
        "average_cost_for_two",
        "currency",
        "aggregate_rating",
        "votes",
    ]

    for key in cuisines.keys():

        lines = df2["cuisines"] == key

        cuisines[key] = (
            df2.loc[lines, cols]
            .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines

#========================================================================

def write_metrics():

    cuisines = top_cuisines()

    italian, american, arabian, japonese, brazilian = st.columns(len(cuisines))

    with italian:
        st.metric(
            label=f'Italian: {cuisines["Italian"]["restaurant_name"]}',
            value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Italian"]['country']}\n
            Cidade: {cuisines["Italian"]['city']}\n
            Média Prato para dois: {cuisines["Italian"]['average_cost_for_two']} ({cuisines["Italian"]['currency']})
            """,
            
            )

        with american:
            st.metric(
                label=f'American: {cuisines["American"]["restaurant_name"]}',
                value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
                help=f"""
                País: {cuisines["American"]['country']}\n
                Cidade: {cuisines["American"]['city']}\n
                Média Prato para dois: {cuisines["American"]['average_cost_for_two']} ({cuisines["American"]['currency']})
            """,
            )

        with arabian:
            st.metric(
                label=f'Arabian: {cuisines["Arabian"]["restaurant_name"]}',
                value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
                help=f"""
                País: {cuisines["Arabian"]['country']}\n
                Cidade: {cuisines["Arabian"]['city']}\n
                Média Prato para dois: {cuisines["Arabian"]['average_cost_for_two']} ({cuisines["Arabian"]['currency']})
            """,
            )

        with japonese:
            st.metric(
                label=f'Japanese: {cuisines["Japanese"]["restaurant_name"]}',
                value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
                help=f"""
                País: {cuisines["Japanese"]['country']}\n
                Cidade: {cuisines["Japanese"]['city']}\n
                Média Prato para dois: {cuisines["Japanese"]['average_cost_for_two']} ({cuisines["Japanese"]['currency']})
            """,
            )

        with brazilian:
            st.metric(
                label=f'Brazilian: {cuisines["Brazilian"]["restaurant_name"]}',
                value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
                help=f"""
                País: {cuisines["Brazilian"]['country']}\n
                Cidade: {cuisines["Brazilian"]['city']}\n
                Média Prato para dois: {cuisines["Brazilian"]['average_cost_for_two']} ({cuisines["Brazilian"]['currency']})
            """,
            )


    return None

# Escreva os cartões métricas na tela
write_metrics()

#========================================================================

# Tabela 

cols = [
    "restaurant_id",
    "restaurant_name",
    "country",
    "city",
    "cuisines",
    "average_cost_for_two",
    "aggregate_rating",
    "votes",
]


# Ordenar DataFrame pelos critérios desejados
df_top10 = df2.sort_values(by=["aggregate_rating", "votes", "average_cost_for_two"],
                          ascending=[False, False, True]).head(10)

# Exibir a tabela no Streamlit
st.dataframe(df_top10[cols].reset_index(drop=True))

st.write("Top 10 restaurantes com a maior média de avaliação, maior número de votos e com o preço médio para dois menor.")

st.markdown("""---""")

# GRAFICOS
with st.container():
    
    lines = df2["country"].isin(countries)

    grouped_df = (
            df2.loc[lines, ["aggregate_rating", "cuisines"]]
            .groupby("cuisines")
            .mean()
            .sort_values("aggregate_rating", ascending=False)
            .reset_index()
            .head(10)
        )

    fig = px.bar(
        grouped_df.head(10),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        color="cuisines",
        title=f"Top 10 Melhores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação",
        },
    )

    st.plotly_chart(fig)

    st.markdown("""---""")


    #GRAFICO 2
    lines = df2["country"].isin(countries)

    grouped_df = (
            df2.loc[lines, ["aggregate_rating", "cuisines"]]
            .groupby("cuisines")
            .mean()
            .sort_values("aggregate_rating", ascending=True)
            .reset_index()
            .head(10)
        )

    fig = px.bar(
        grouped_df.head(10),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        color="cuisines",
        title=f"Top 10 Piores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação",
        },
    )

    st.plotly_chart(fig)

    st.markdown("""---""")


    #GRAFICO 3

    st.markdown("##### Tabela com % preço por tipo culinário")
    
    # Agrupe os dados pelo tipo culinário
    grouped_data = df2.groupby('cuisines')['price_type'].value_counts(normalize=True).unstack() *100

    grouped_data_percent_formatted = grouped_data.applymap(lambda x: f'{x:.2f}%')

    #st.dataframe(grouped_data_percent_formatted)
    st.dataframe(grouped_data_percent_formatted.style.set_table_styles([{'selector': 'table', 'props': [('font-size', '16px')]}]))

    st.markdown("""---""")

    
    #GRAFICO 4

    st.markdown("##### Tabela com % preço por País")
    
    # Agrupe os dados pelo tipo culinário
    grouped_data_country = df2.groupby('country')['price_type'].value_counts(normalize=True).unstack() *100

    grouped_data_percent_formatted_country = grouped_data_country.applymap(lambda x: f'{x:.2f}%')

    #st.dataframe(grouped_data_percent_formatted)
    st.dataframe(grouped_data_percent_formatted_country.style.set_table_styles([{'selector': 'table', 'props': [('font-size', '16px')]}]))

    



