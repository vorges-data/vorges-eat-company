# Libraries
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
from PIL import Image
import streamlit as st
#import matplotlib.pyplot as plt
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
# Descrição dos dados
def describe_attributes(dataframe):
    return dataframe.describe()


# Função que retorna as variáveis numéricas
def get_numerical_attributes(dataframe):
    return dataframe.select_dtypes(include=['int64', 'float64'])

# Função que retorna as variáveis categóricas
def get_cat_attributes(dataframe):
    return dataframe.select_dtypes(exclude=['int64','float64'])

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

# Função - Medidas Estatísticas
def get_first_order_statistics(dataframe):
    # Métricas de Tendência Central
    mean = pd.DataFrame(dataframe.apply(np.mean)).T
    median = pd.DataFrame(dataframe.apply(np.median)).T

    # Métricas de dispersão
    min_ = pd.DataFrame(dataframe.apply(min)).T
    max_ = pd.DataFrame(dataframe.apply(max)).T
    range_ = pd.DataFrame(dataframe.apply(lambda x: x.max() - x.min())).T
    std = pd.DataFrame(dataframe.apply(np.std)).T
    skew = pd.DataFrame(dataframe.apply(lambda x: x.skew())).T
    kurtosis = pd.DataFrame(dataframe.apply(lambda x: x.kurtosis())).T

    # Métricas de Concatenação
    m = pd.concat([min_, max_, range_, mean, median, std, skew, kurtosis]).T.reset_index()
    m.columns = ['attributes', 'min', 'max', 'range', 'mean', 'median', 'std', 'skew', 'kurtosis']
    
    return m


# Carregar os dados
df_raw = pd.read_csv(FILE_PATH)

# Copy
df1 = df_raw.copy()

# Chamar a função para renomear as colunas
df1 = rename_columns( df1 )


# Chamar a função para processar os dados
df2 = process_data(FILE_PATH)


def dataframe_dimensions(dataframe):
    print(f'Número de linhas: {dataframe.shape[0]}')
    print(f'Número de colunas: {dataframe.shape[1]}')
    
    return None



#========================================================================
#========================== Menu Lateral ================================
#========================================================================
#======================================================================
st.set_page_config(page_title='Business', page_icon='💼', layout='wide')

st.header('Vorges Eat Marktplace: Perguntas de Negócio')


image2 = Image.open('Logo Preto Sem Fundo.png')
st.sidebar.image( image2, width = 120)

st.sidebar.markdown('# Vorges Eat')
st.sidebar.markdown('## Seu Marketplace de Restaurantes')
st.sidebar.markdown("""---""")
st.sidebar.write('**Missão:** Organizar e conectar o cliente ao empreendedor')
st.sidebar.write('**Valores:** Satisfação máxima do cliente e do empreendedor')
st.sidebar.write('**Visão:** Entregar e oferecer o melhor serviço de Restaurantes')



#============================= Imagem Inicial ==========================
image = Image.open('business.jpg')
st.image(image, caption= 'Business Meeting', width=620)


st.markdown("""---""")

# ======================== Texto explicando o objetico da página =======
st.markdown(
    """
    ### Objetivos:
    - O CEO da Vorges Eat, Vinicius Borges, foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a empresa, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder algumas perguntas sobre o Business Core da companhia.
    - Abaixo há 5 páginas que detalham as respostas obtidas pelo time de Data Science da Vorges para os segmentos: Geral; País; Cidade; Restaurantes e Tipos Culinários.
    
    """
)


#========================================================================
#========================== Layout no Streamlit =========================
#========================================================================

#===========================
# Criar abas para página
#===========================
tab1, tab2, tab3, tab4, tab5 = st.tabs( ['Geral', 'País', 'Cidade', 'Restaurantes', 'Tipos de Culinária'])

# GERAL
with tab1:
    st.markdown('# Perguntas Gerais')
    st.markdown('##### 1. Quantos restaurantes únicos estão registrados?')
    st.write('Há 6.929 restaurantes únicos registrados.')
    
    st.markdown('##### 2. Quantos países únicos estão registrados?')
    st.write('Há 15 países únicos registrados.')
    
    st.markdown('##### 3. Quantas cidades únicas estão registradas?')
    st.write('Há 125 cidades únicas registradas.')
    
    st.markdown('##### 4. Qual o total de avaliações feitas?')
    st.write('Há um total de 4.194.533 avaliações feitas.')
    
    st.markdown('##### 5. Qual o total de tipos de culinária registrados?')
    st.write('Há um total de 165 tipos culinários.')


# PAÍS
with tab2:
    st.markdown('# Perguntas sobre os Países')
    
    # ====================  QUESTAO 1 ====================================
    st.markdown('##### 1. Qual o nome do país que possui mais cidades registradas?')
    st.write('Como mostrado na tabela abaixo a **Índia** é o país com mais cidades registradas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:,['country','city']].groupby('country')
                             .nunique()
                             .sort_values('city',ascending=False)
                             .reset_index() )
    
    st.dataframe( aux )
    
    # ====================  QUESTAO 2 ====================================
    st.markdown('##### 2. Qual o nome do país que possui mais restaurantes registrados?')
    st.write('A **Índia** é o país com mais restauramtes registrados.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['country','restaurant_id']].groupby('country')
                                     .nunique()
                                     .sort_values('restaurant_id', ascending=False)
                                     .reset_index() )
    st.dataframe( aux )
    
    # ====================  QUESTAO 3 ====================================
    st.markdown('##### 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?')
    st.write('A **Índia** é o país com mais restauramtes com nível de preço igual a 4.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['aggregate_rating'] >= 4 , ['restaurant_id','country'] ]
                                        .groupby('country')
                                        .count()
                                        .sort_values('restaurant_id', ascending=False)
                                        .reset_index() )
    st.dataframe( aux )
    
    
      # ====================  QUESTAO 4 ====================================
    st.markdown('##### 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?')
    st.write('A **Índia** é o país com maior quantidade de tipos culinários distintos.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['cuisines','country']].groupby('country')
                                  .nunique()
                                  .sort_values('cuisines', ascending=False)
                                  .reset_index() )
    
    st.dataframe( aux )
    
    # ====================  QUESTAO 5 ====================================
    st.markdown('##### 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?')
    st.write('A **Índia** é o país com maior quantidade de avaliações feitas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['votes','country']].groupby('country')
                               .count()
                               .sort_values('votes', ascending=False)
                               .reset_index() )
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 6 ====================================
    st.markdown('##### 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?')
    st.write('A **Índia** é o país que possui a maior quantidade de restaurantes que fazem entrega.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['is_delivering_now'] == 1, ['restaurant_id','country'] ].groupby('country')
                                                                     .count()
                                                                     .sort_values('restaurant_id', ascending=False)
                                                                     .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 7 ====================================
    st.markdown('##### 7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?')
    st.write('A **Índia** é o país que possui a maior quantidade de restaurantes que aceitam reservas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['has_online_delivery'] == 1, ['restaurant_id','country'] ]
                                          .groupby('country')
                                          .count()
                                          .sort_values('restaurant_id', ascending=False)
                                          .reset_index() )
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 8 ====================================
    st.markdown('##### 8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?')
    st.write('A **Indonesia** é o país que possui na média a maior quantidade de avaliações registradas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['votes','country']].groupby('country')
                               .mean()
                               .sort_values('votes', ascending=False)
                               .reset_index())
    
    st.dataframe( aux )
    
    # ====================  QUESTAO 9 ====================================
    st.markdown('##### 9. Qual o nome do país que possui, na média, a maior nota média registrada?')
    st.write('A **Indonesia** é o país que possui na média a maior nota média registrada.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['aggregate_rating','country']].groupby('country')
                                          .mean()
                                          .sort_values('aggregate_rating', ascending=False)
                                          .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 10 ====================================
    st.markdown('##### 10. Qual o nome do país que possui, na média, a menor nota média registrada?')
    st.write('O **Brasil** é o país que possui na média a menor nota média registrada.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['aggregate_rating','country']].groupby('country')
                                          .mean()
                                          .sort_values('aggregate_rating', ascending=True)
                                          .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 11 ====================================
    st.markdown('##### 11. Qual a média de preço de um prato para dois por país?')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['average_cost_for_two','country']].groupby('country')
                                              .mean()
                                              .sort_values('average_cost_for_two', ascending=False)
                                              .reset_index() )
    st.dataframe( aux )
    
#===============================================================================================================

# CIDADES
with tab3:
    st.markdown('# Perguntas sobre as Cidades')
    
    # ====================  QUESTAO 1 ====================================
    st.markdown('##### 1. Qual o nome da cidade que possui mais restaurantes registrados?')
    st.write('**Abu Dhabi** e outras cidades mais possuem mais restaurantes registrados.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['restaurant_id','city']].groupby('city')
                                    .count()
                                    .sort_values('restaurant_id', ascending=False)
                                    .reset_index() )
    st.dataframe( aux )
    
     

    
    # ====================  QUESTAO 2 ====================================
    st.markdown('##### 2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?')
    st.write('**Londres** é a cidade que mais possui restaurantes com nota média acima de 4.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['aggregate_rating'] >= 4 , ['restaurant_id','city']].groupby('city')
                                                                 .count()
                                                                 .sort_values('restaurant_id', ascending= False)
                                                                 .reset_index() )
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 3 ====================================
    st.markdown('##### 3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?')
    st.write('**Gangtok** é a cidade que mais possui restaurantes com nota média abaixo de 2.5.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['aggregate_rating'] < 2.5, ['restaurant_id','city']]
                                        .groupby('city')
                                        .count()
                                        .sort_values('restaurant_id', ascending=False)
                                        .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 4 ====================================
    st.markdown('##### 4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?')
    st.write('**Adelaide** é a cidade que possui o maior valor médio de um prato para casal.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['average_cost_for_two','city']].groupby('city')
                                           .mean()
                                           .sort_values('average_cost_for_two', ascending=False)
                                           .reset_index() )
    
    st.dataframe( aux )

    
    # ====================  QUESTAO 5 ====================================
    st.markdown('##### 5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?')
    st.write('**Birmingham** é a cidade que possui maior quantidade de tipos culinários distintos.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['cuisines','city']].groupby('city')
                               .nunique()
                               .sort_values('cuisines', ascending=False)
                               .reset_index().head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 6 ====================================
    st.markdown('##### 6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?')
    st.write('**Bangalore** é a cidade que possui maior quantidade de restaurantes que fazem reservas.')
    
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['has_table_booking'] == 1, ['restaurant_id','city']].groupby('city')
                                                                 .count()
                                                                 .sort_values('restaurant_id', ascending=False)
                                                                 .reset_index().head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 7 ====================================
    st.markdown('##### 7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?')
    st.write('**Vadodara** e **Amritsar** são as cidades que possuem a maior quantidade de restaurantes que fazem entregas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['is_delivering_now'] == 1, ['restaurant_id','city']]
                                        .groupby('city')
                                        .count()
                                        .sort_values('restaurant_id', ascending=False)
                                        .reset_index().head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 8 ====================================
    st.markdown('##### 8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?')
    st.write('**Bhopal** é a cidade que possui maior quantidade de restaurantes que aceitam pedidos online.')
    
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[ df2['has_online_delivery'] == 1, ['restaurant_id','city'] ]
                                            .groupby('city')
                                            .count()
                                            .sort_values('restaurant_id', ascending=False)
                                            .reset_index()
                                            .head(10))
    
    st.dataframe( aux )
    

#==================================================================================================


    
# RESTAURANTES
with tab4:
    st.markdown('# Perguntas sobre os Restaurantes')
    
    # ====================  QUESTAO 1 ====================================
    st.markdown('##### 1. Qual o nome do restaurante que possui a maior quantidade de avaliações?')
    st.write('**Bawarchi** é o nome do restaurante que possui a maior quantidade de avaliações.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['restaurant_id','restaurant_name','country','votes']]
                                    .sort_values(['votes', 'restaurant_id'], ascending=[False, True])
                                    .head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 2 ====================================
    st.markdown('##### 2. Qual o nome do restaurante com a maior nota média?')
    st.write('**Indian Grill Room** e outros restaurantes são os restaurantes que possuem a maior nota média.')
    
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['restaurant_id','restaurant_name', 'country','aggregate_rating']]
                                .sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                                .head(10))
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 3 ====================================
    st.markdown('##### 3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?')
    st.write('**d Arrys Verandah Restaurant** é o restaurante com o maior valor de um prato para casal.')
    
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','average_cost_for_two']
    aux = ( df2.loc[: , cols].sort_values(['average_cost_for_two','restaurant_id'], ascending=[False, True])
                                                                        .head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 4 ====================================
    st.markdown('##### 4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?')
    st.write('**Loca Como tu Madre** e outros restaurantes possuem a menor média de avaliação no Brasil.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id', 'restaurant_name','country','aggregate_rating','cuisines']
    aux = ( df2.loc[ df2['cuisines'] == 'Brazilian', cols]
                        .sort_values(['aggregate_rating','restaurant_id'], ascending=[True, True])
                        .head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 5 ====================================
    st.markdown('##### 5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?')
    st.write('**Braseiro da Gávea e Aprazível** são os restaurantes com a maior média de avaliação no Brasil.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']
    lines = (df2['country'] == 'Brazil') & (df2['cuisines'] == 'Brazilian')
    
    aux = df2.loc[lines, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).head(10)
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 6 ====================================
    st.markdown('##### 6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?')
    st.write('**Sim**, conforme mostrado na tabela abaixo os restaurantes que aceitam pedidos online na média possuem maior quantidade de avaliações.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['votes','has_online_delivery']].groupby('has_online_delivery')
                                           .mean()
                                           .sort_values('votes', ascending=False)
                                           .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 7 ====================================
    st.markdown('##### 7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?')
    st.write('**Sim**, os restaurantes que fazem reservas possuem na média um maior valor médio no prato para duas pessoas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['average_cost_for_two','has_table_booking']]
                        .groupby('has_table_booking')
                        .mean()
                        .sort_values('average_cost_for_two', ascending=False)
                        .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 8 ====================================
    st.markdown('##### 8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?')
    st.write('**Sim**, conforme demonstrado na tabela abaixo.')
    
    
    # Tabela dataframe com os nomes dos países
    lines = (df2['country'] == 'United States of America') & ((df2['cuisines'] == 'BBQ') | (df2['cuisines'] == 'Japanese'))
    
    aux = (df2.loc[lines, ['average_cost_for_two', 'cuisines'] ]
                                         .groupby('cuisines')
                                         .mean()
                                         .sort_values('average_cost_for_two', ascending=False)
                                         .reset_index())
    
    st.dataframe( aux )
    
    
#===============================================================================================================

    
# TIPO CULINÁRIO

with tab5:
    st.markdown('# Perguntas sobre os Tipos Culinários')
    
    # ====================  QUESTAO 1 ====================================
    st.markdown('##### 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?')
    st.write('**Darshan** e outros restaurantes são os que possuem culinária italiana com a maior média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Italian'
    
    aux = df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True]).reset_index().head(20)
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 2 ====================================
    st.markdown('##### 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?')
    st.write('**Avenida Paulista e outros restaurantes** de culinária italiana que possuem a menor média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Italian'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[True, True])
                                                                     .reset_index()
                                                                     .head(10))
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 3 ====================================
    st.markdown('##### 3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?')
    st.write('**Burger & Lobster e outros restaurantes** de culinária americana que possuem a maior média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'American'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                                                                     .reset_index()
                                                                     .head(30) )
    
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 4 ====================================
    st.markdown('##### 4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?')
    st.write('**Alston Bar & Beef** é o restaurante de culinária americana com a menor média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'American'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[True, True])
                                                                     .reset_index()
                                                                     .head(10) )
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 5 ====================================
    st.markdown('##### 5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?')
    st.write('**Mandi@36** é o restaurante de culinária arabe com a maior média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Arabian'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                                                                     .reset_index()
                                                                     .head(10))
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 6 ====================================
    st.markdown('##### 6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?')
    st.write('**Raful** é o restaurante de culinária arabe com a menor média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Arabian'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[True, True])
                                                                     .reset_index()
                                                                     .head(10) )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 7 ====================================
    st.markdown('##### 7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?')
    st.write('**Sushi Samba e outros restaurantes** de culinária japonesa possuem a maior média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Japanese'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                                                                     .reset_index()
                                                                     .head(20))
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 8 ====================================
    st.markdown('##### 8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?')
    st.write('**Banzai Sishi** é o restaurante de culinária japonesa com a menor média de avaliação.')
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Japanese'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[True, True])
                                                                     .reset_index()
                                                                     .head(10) )
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 9 ====================================
    st.markdown('##### 9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?5. Qual o total de tipos de culinária registrados?')
    st.write('**Kanaat Lokantasi** é o restaurante de culinária caseira com a maior média de avaliação.')
    
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Home-made'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                                                                     .reset_index() )
    
    st.dataframe( aux )
    
    
    # ====================  QUESTAO 10 ====================================
    st.markdown('##### 10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?')
    st.write('**GurMekan Restaurant** é o restaurante de culinária caseira com a menor média de avaliação.')
    
    
    # Tabela dataframe com os nomes dos países
    cols = ['restaurant_id','restaurant_name','country','cuisines','aggregate_rating']
    lines = df2['cuisines'] == 'Home-made'
    
    aux = ( df2.loc[lines, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[True, True])
                                                                     .reset_index() )
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 11 ====================================
    st.markdown('##### 11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?')
    st.write('**Modern Australian** é o tipo culinário no qual possui o maior valor médio no prato para duas pessoas.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['average_cost_for_two','country','cuisines']].groupby('cuisines')
                                               .max()
                                               .sort_values('average_cost_for_two', ascending=False)
                                               .reset_index()
                                               .head(10))
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 12 ====================================
    st.markdown('##### 12. Qual o tipo de culinária que possui a maior nota média?')
    st.write('**Indian** é o tipo culinário que possui a maior nota média.')
    
    # Tabela dataframe com os nomes dos países
    aux = ( df2.loc[:, ['aggregate_rating','cuisines']].groupby('cuisines')
                                           .max()
                                           .sort_values('aggregate_rating', ascending=False)
                                           .reset_index()
                                           .head(1) )
    
    st.dataframe( aux )
    
    
    
    # ====================  QUESTAO 13 ====================================
    st.markdown('##### 13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?')
    st.write('**North Indian** é o tipo culinário que mais possui restaurantes que aceitam pedidos online e realizam entregas.')
    
    
    # Tabela dataframe com os nomes dos países
    lines = (df2['has_online_delivery'] == 1) & (df2['is_delivering_now'] == 1)
    
    aux = (df2.loc[:, ['restaurant_id','cuisines'] ]
                                         .groupby('cuisines')
                                         .count()
                                         .sort_values('restaurant_id', ascending=False)
                                         .reset_index()).head(1)
    
    st.dataframe( aux )
    
    
    
