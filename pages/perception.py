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

_1,_2 = st.columns([5,4])

with _1 :
    st.selectbox("Services et ligne d'approvisionnement",["Phone Service","Multiple Lines","Unlimited Data",
                                                          "Internet Type","Online Security"],key="key_3")
    if st.session_state.key_3== "Phone Service":
        st.plotly_chart(main.graphe_pie(variable="Phone Service",titre="Distribution des clients par statut <br> telephoniue du service ",
           paper="#4F4F4F",width=280,height=380),use_container_width=True)
    elif st.session_state.key_3== "Multiple Lines":
        st.plotly_chart(main.graphe_pie(variable="Multiple Lines",titre="Distribution des clients par statut de disponibilité de <br> ligne multiple",
           paper="#4F4F4F",width=280,height=380),use_container_width=True)
        
    elif st.session_state.key_3== "Internet Type":
        st.plotly_chart(main.graphe_pie(variable="Internet Type",titre="Distribution du moyen d'approvitionnement en <br> internet des client",
           paper="#4F4F4F",width=280,height=380),use_container_width=True) 
          
    elif st.session_state.key_3== "Unlimited Data":
        st.plotly_chart(main.graphe_pie(variable="Unlimited Data",titre="Distribution des clients par status de payement <br> supplementaire",
           paper="#4F4F4F",width=280,height=380),use_container_width=True) 
         
    elif st.session_state.key_3== "Online Security":
        st.plotly_chart(main.graphe_pie(variable="Online Security",titre="Distribution des clients par status du type de <br> securité beneficié",
           paper="#4F4F4F",width=280,height=380),use_container_width=True) 
        
   
with _2:
    st.plotly_chart(main.graphe_bar(variable = "Payment Method",titre="Repartition des clients par  moyen de payement",
           paper="#4F4F4F",orient="h",color="#C4593C",
          width=400,height=470,font_size=15),use_container_width=True)

_1,_2 = st.columns([5,4])

with _1:
    fig = px.funnel(main.data["Offer"].fillna("aucun").
          value_counts(dropna=False).to_frame().
          reset_index(),y="Offer",
          x="count")

    fig.update_layout(margin=dict(t=30,l=0,r=0,b=5),
                      xaxis=dict(showgrid=False,color='white',title="",tickfont_size=10),
                      yaxis=dict(showgrid=False,color='white',title="",showticklabels=False),
                  title=dict(x=0.2,font_color="white",font_size=15,
                             text='Répartition des client par types de services accepté'),
                      paper_bgcolor="#4F4F4F",plot_bgcolor="#4F4F4F",height=355,width=500,
                 legend=dict(orientation="h",title='',x=0.2,y=0.8,font_color="white"))
    fig.update_traces(textinfo='label+value')
    st.plotly_chart(fig,use_container_width=True)
    
with _2:
    t1,t2 = st.tabs(["Total Charges","Total Revenue"])
    t1.plotly_chart(main.box_plot(x='Total Charges',y='Churn Label',
                             title='Répartition du frais totaux des client par status de churn',
                             width=350,height=300),use_container_width=True)
    t2.plotly_chart(main.box_plot(x='Total Revenue',y='Churn Label',
                             title='Répartition du revenu totaux généré par <br> les client par status de churn',
                             width=350,height=300),use_container_width=True)
    
t1,t2 = st.tabs(["Offer","Contract"])
t1.plotly_chart(main.bar_biplot(var1="Offer",var2="Churn Label",legend_x=0.5,
           title='Répartition des clients par type d"offre accepté et par score de satisfation',
           height=400,width=700,paper="#4F4F4F"),use_container_width=True)
t2.plotly_chart(main.bar_biplot(var1="Contract",var2="Churn Label",legend_x=0.5,
           title='Répartition des clients par type d"offre accepté et par score de satisfation',
           height=400,width=700,paper="#4F4F4F"),use_container_with=True )
