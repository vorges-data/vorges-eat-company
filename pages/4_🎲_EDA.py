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
st.set_page_config(page_title='EDA', page_icon='🎲', layout='wide')

st.header('Vorges Eat Marktplace: Dashboard Estatística Descritiva')
st.markdown("""---""")


#============================= Imagem Inicial ==========================
image2 = Image.open('eda.jpg')
st.image(image2, caption= 'Exploratory Data Analysis', width=620)


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

with st.container():
    col1, col2 = st.columns( 2 )
    
    with col1:
        
            # ==================================== TEXTO DIMENSAO DADOS =============
            qt_lines = df1.shape[0]
            qt_cols  = df1.shape[1]
            
            st.markdown('##### Dimensão dos Dados antes do Processamento')
            st.write(f'Número de linhas: {qt_lines}')
            st.write(f'Número de colunas: {qt_cols}')
            #=============================================
            
            qt_lines_2 = df2.shape[0]
            qt_cols_2  = df2.shape[1]
            
            st.markdown('##### Dimensão dos Dados após o Processamento')
            st.write(f'Número de linhas: {qt_lines_2}')
            st.write(f'Número de colunas: {qt_cols_2}')
            #=============================================
            
    with col2:
            #======================================== RESUMO ======================
            st.markdown('##### Resumo')
            
            # Número de dados perdidos
            diff_data = qt_lines - qt_lines_2
            st.write(f'Quantidade de dados perdidos: {diff_data}')
            
            # Calcular a porcenagem de dados perdidos
            percent_data = (((qt_lines_2 / qt_lines) -1)*100)*-1
            st.write('Após o Processamento dos Dados perdemos {:.2f}% dos dados.'.format(percent_data))

            
st.write("""---""")
        
#============================== Containers das Tabelas ========================

with st.container():
    col1, col2 = st.columns( 2 )
    
    # Tabela das variáveis numéricas
    with col1:
        st.markdown('##### Variáveis Numéricas')
        
        numerical_data = get_numerical_attributes(df1)
        numerical_data_df = pd.DataFrame( numerical_data.columns, columns = ['Colunas Numéricas'] )
        st.dataframe(numerical_data_df)
        
        
    # Tabela das variáveis categóricas
    with col2:
        st.markdown('##### Variáveis Categóricas')
        
        cat_data = get_cat_attributes(df1)
        cat_data_df = pd.DataFrame( cat_data.columns, columns = ['Colunas Categóricas'] )
        st.dataframe(cat_data_df)


st.write("""---""")

#========================GRAFICO DE HISTOGRAMA VARIAVEIS NUM ======================
st.markdown('##### Distribuição das variáveis numéricas')
image = Image.open('hist.png')
st.image(image, caption= 'Variáveis Numéricas')

st.write("""---""")



#========================== TABELA ESTATISTICA ====================================
st.markdown('### Estatística de Primeira Ordem')
df_aux = get_first_order_statistics(numerical_data)
st.dataframe(df_aux)
st.markdown(
    """
    ### Significado das medidas estatística:
    
    - **Min:** Mínimo-> O menor valor observado em um conjunto de dados. Ou seja, é o valor mais baixo que aparece na amostra ou população que está sendo analisada.
    
    - **Max:** Máximo-> O maior valor observado em um conjunto de dados. Ou seja, é o valor mais alto que aparece na amostra ou população que está sendo analisada.
    
    - **Range:** Amplitude-> É a diferença entre o maior e o menor valor observados em um conjunto de dados. Ou seja, é a amplitude dos valores que aparecem na amostra ou população que está sendo analisada.
    
    - **Mean:** Média-> A medida média na estatística é a soma dos valores observados em um conjunto de dados dividida pelo número de observações. Em outras palavras, é o valor central que representa o conjunto de dados de forma geral. É frequentemente chamado de "média aritmética".
    
    - **Median:** Mediana-> A medida mediana na estatística é o valor que divide a amostra ou população em duas partes iguais, sendo que metade dos valores é menor ou igual a essa medida, e a outra metade é maior ou igual. É uma medida de tendência central que representa o valor médio do conjunto de dados. É menos sensível a valores extremos do que a média aritmética.
    
    - **Std:** Desvio-Padrão-> A medida de desvio padrão na estatística é uma medida de dispersão em torno da média. Ele indica o quão longe os valores individuais estão da média, ou seja, o quão "espalhados" estão os dados. Quanto maior o desvio padrão, mais os dados estão espalhados em relação à média. Por outro lado, quanto menor o desvio padrão, mais próximos os dados estão da média.
    
    - **Skew:** Assimetria-> A medida de skew (ou assimetria, em português) na estatística é uma medida que indica o grau de assimetria da distribuição dos dados em relação à média. Quando uma distribuição é simétrica, a medida de skew é zero. Quando a distribuição é assimétrica à direita, ou seja, possui uma cauda longa na direção dos valores maiores, a medida de skew é positiva. Quando a distribuição é assimétrica à esquerda, ou seja, possui uma cauda longa na direção dos valores menores, a medida de skew é negativa.
    
    - **Kurtosis:** Curtose-> A medida de kurtosis na estatística é uma medida que indica o grau de achatamento ou picosidade da distribuição dos dados em relação à distribuição normal. Quando os dados são mais achatados e possuem menos pico do que a distribuição normal, a medida de kurtosis é negativa. Quando os dados possuem mais pico do que a distribuição normal, a medida de kurtosis é positiva.
    
    """
)

st.write("""---""")

#========================== DESCRIÇÃO ESTATÍSTICA ====================================
st.markdown('### Descrição dos Dados')
describe_data = describe_attributes( df1 )
st.dataframe( describe_data )

st.write("""---""")

# ======================= TABELA PAISES UNICOS =======================================
st.markdown('### Conjunto de países do Dataset')
country_unique = pd.DataFrame(df2['country'].unique(), columns=['País'])
st.dataframe(country_unique)
