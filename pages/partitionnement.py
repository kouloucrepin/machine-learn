import streamlit as st
import main
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import matplotlib.pyplot as plt
from wordcloud import WordCloud


st.set_page_config(layout="wide")
st.markdown("""<style>
.stApp {
    background-color: lightgray;  # Remplacez 'lightblue' par la couleur de votre choix
}
[data-testid="stSidebar"] {
        background-color: lightblue;
        font-color:white
    }
    
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h5,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h6 {
        color: white;  /* Remplacez par la couleur de votre choix */
    }
.stApp header {
        background-color: lightgray;
    }
</style>""", unsafe_allow_html=True)


total_vil = main.data["City"].nunique()

_1,_2,_3,_4=st.columns(4)

_1.metric("Nombre de client",main.nb_client)
_2.metric("effectifs des désabonées",main.nb_churn)
_3.metric("effectifs d'abonées",main.nb_not_churn)
_4.metric("effectifs des villes deservie",total_vil)
style_metric_cards(border_left_color="#4F4F4F")

_1,_2 = st.columns([3,2])

with _1:
    st.plotly_chart(main.bar_biplot(var1="Satisfaction Score",var2="Churn Label",
           title='Répartition des clients par status matrimonial et <br> par score de satisfation',
           height=350,width=700,paper="#4F4F4F"),use_container_width=True)

with _2:
    st.plotly_chart(main.box_plot(x='CLTV',y='Churn Label',
             title='Répartition du CLTV des client par <br> status de churn',
             width=350,height=350),use_container_width=True)

frequencies = main.data.loc[:,"Churn Reason"].value_counts()

# Génération du wordcloud
wordcloud = WordCloud(width=800, height=400, background_color='#4F4F4F').generate_from_frequencies(frequencies)


fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_title("Visualisation des raison du churn")
ax.axis('off') 
st.pyplot(fig)
