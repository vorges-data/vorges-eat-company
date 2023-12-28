import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Home', page_icon= '📊')


image = Image.open('Logo Preto Sem Fundo.png')
st.sidebar.image( image, width = 120)

st.sidebar.markdown('# Vorges Eat')
st.sidebar.markdown('## Seu Marketplace de Restaurantes')
st.sidebar.markdown("""---""")
st.sidebar.write('**Missão:** Organizar e conectar o cliente ao empreendedor')
st.sidebar.write('**Valores:** Satisfação máxima do cliente e do empreendedor')
st.sidebar.write('**Visão:** Entregar e oferecer o melhor serviço de Restaurantes')
st.sidebar.markdown("""---""")
st.sidebar.write('Faça o Download dos dados aqui:')
#===================================== Botão de Download ====================
data_processed = pd.read_csv('datasets/data_processed.csv')

st.sidebar.download_button(
        label = 'Download',
        data = data_processed.to_csv( index=False, sep=';'),
        file_name = 'data_processed',
        mime = 'text/csv'
)

#============================================================================

st.write('# Vorges Eat Company Dashboard')

#============================= Vídeo Inicial ==========================
#image2 = Image.open('home.jpg')
#st.image(image2, caption= 'Seja Bem-Vindo (a)', width=620)

video_file = open('vorges-eat.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)


st.markdown("""---""")

st.markdown(
    """
    A empresa Vorges Eat é uma marketplace de restaurantes. Sendo o seu core business facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Vorges Eat, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
    ### Como utilizar este Dashboard?
    No menu lateral deste Web App há cinco páginas de visões estratégicas da Vorges Eat:
    - Visão País: Métricas dos países parceiros da Vorges Eat;
    - Visão Cidades: Métricas das cidades onde estão instalados os restaurantes;
    - Visão Tipo Culinário: Métricas das comidas típicas oferecidas pelos restaurante.
    - Estatística Descritiva dos Dados
    - Perguntas de Negócio
    
    Portanto, acesse o menu lateral e escolha a página que gostaria de visualizar!
    
    ### Time de Desenvolvimento:
    - Team Data Science at Vorges Company
    
    ### Contact:
    - Vinicius Borges: https://www.linkedin.com/in/viniciusleitedata/
    - Blog Vorges: www.vorges.com.br
    
    ### Observação:
    - Os códigos utilizados para gerar este Web App podem ser vistos no GitHub, os códigos gerados para responder as perguntas de negócio do CEO podem ser vistos no Blog da Vorges e também no GitHub.
    - No menu lateral você pode fazer o Download do Dataset utilizado neste projeto, o dataset está tratado e prontinho para receber suas análises!
    - O conjunto de dados foi retirado da plataforma Kaggle, o link para acesso aos dados: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
    """
)
st.markdown("""---""")