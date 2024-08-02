import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import plotly.express as px


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






###importation de la base de donnée
data = pd.read_csv("telco.csv",sep=",")

def recodage(x):
    if x<3:
        return str(x)
    else:
        return '>=3'
data["Number of Dependents"] = data["Number of Dependents"].apply(lambda x :  recodage(x)).astype("object")
data[['Satisfaction Score', 'Churn Score',"Zip Code"]] = data[['Satisfaction Score', 'Churn Score',"Zip Code"]].astype("object")


@st.cache_data(show_spinner=False)
def graphe_bar(variable = "Gender",titre="Repartition des clients par sexes",font_size=15,t=60,paper="lightgray",orient='v',width=550,height=350,top=None,color="blue"):
    if top:
        s=data[variable].astype('str').value_counts().sort_values(ascending=True).tail(top)
    else:
        s=data[variable].astype('str').value_counts().sort_values(ascending=True)
    fig = px.bar(s,orientation=orient,text_auto=True,
                 height=height,width=width,title=titre,
                 color_discrete_sequence=[color])
    fig.update_traces(textposition="inside",
                      textfont_size=13)
    fig.update_layout(showlegend=False,xaxis=dict(title='',color='white'),
                      yaxis=dict(title="",color='white'),
                      margin=dict(r=0,l=0,t=t,b=0),
                      title=dict(x=0.1,font_color="white",font_size=font_size),
                 paper_bgcolor=paper,plot_bgcolor=paper)
    if orient=="h":
        fig.update_xaxes(showgrid=False ,showticklabels=False)
    else:
        fig.update_yaxes(showgrid=False ,showticklabels=False)
    #fig.show(config={"modeBarButtonsToRemove":["pan2d","select2d","lasso2d","zoom2d","zoomOut2d","zoomIn2d","resetScale2d"]})
    return fig

@st.cache_data(show_spinner=False)
def histogram(variable="",titre="repartition des clients par age",width=750,height=370,paper="lightgray"):
    fig=px.histogram(data[[variable,"Churn Label"]],x=variable,title=titre,nbins=100,width=width,height=height,color="Churn Label")
    fig.update_layout(margin=dict(t=30,l=0,r=0,b=5),
                  title=dict(x=0.2,font_color="white"),
                  paper_bgcolor=paper,plot_bgcolor=paper,showlegend=False,
                  xaxis=dict(title="",showgrid=True,color='white'),
                      yaxis=dict(title="",showgrid=True,showticklabels=True,color='white'))
    
    #fig.show(config={"modeBarButtonsToRemove":["pan2d","select2d","lasso2d","zoom2d","zoomOut2d","zoomIn2d","resetScale2d"]})

    return fig


@st.cache_data(show_spinner=False)
def graphe_pie(variable="Churn Label",titre="Répartion des clients par sexe",size=15,paper="lightgray",width=400,height=250):
    fig = px.pie(data[variable].value_counts().to_frame().reset_index(),names=variable,
             values="count",hole=0.5,height=350,title=titre,width=width)
    fig.update_traces(textinfo='label+percent+value',showlegend=False)
    fig.update_layout(margin=dict(t=60,l=0,r=0,b=5),
                  title=dict(x=0.2,font_color="white",font_size=size),paper_bgcolor=paper,plot_bgcolor=paper,height=height)
    #fig.show(config={"modeBarButtonsToRemove":["pan2d","select2d","lasso2d","zoom2d","zoomOut2d","zoomIn2d","resetScale2d"]})

    return fig


@st.cache_data(show_spinner=False)
def box_plot(x='CLTV',y='Churn Label',title='Répartition du CLTV des client par status de churn',width=350,height=300):
    fig=px.box(data, y=y, x=x,color="Churn Label",color_discrete_map={"Yes":"orange","No":"blue"})
    fig.update_layout(margin=dict(t=60,l=0,r=0,b=5),
                      xaxis=dict(showgrid=False,color='white',title="",tickfont_size=10),
                      yaxis=dict(showgrid=False,color='white',title="",showticklabels=False),
                  title=dict(x=0.1,font_color="white",font_size=17,
                             text=title),
                      paper_bgcolor="#4F4F4F",plot_bgcolor="#4F4F4F",height=height,width=width,
                 legend=dict(orientation="h",title='',x=0.8,y=0.6,font_color="white"))
    return fig

@st.cache_data(show_spinner=False)
def bar_biplot(var1="Churn Label",var2="Dependents",height=600,t=60,width=300,legend_x=0.7,paper="#4F4F4F",title='repartition des client par status matrimonail et de churn',font_size=15):
    fig = px.bar(pd.crosstab(data[var1],data[var2]),text_auto=True,
            title=title)

    fig.update_layout(margin=dict(t=t,l=0,r=0,b=5),
                  title=dict(x=0.2,font_color="white",font_size=font_size),width=width,
                  paper_bgcolor=paper,plot_bgcolor=paper,height=height,
                 legend=dict(x=legend_x,y=0.95,orientation='h',title="",font_color="white"),
                 xaxis=dict(showgrid=False,title="",color="white"),
                  yaxis=dict(showgrid=False,title="",showticklabels=False))
    fig.update_traces(width=0.7)
    #fig.show(config={"modeBarButtonsToRemove":["pan2d","select2d","lasso2d","zoom2d","zoomOut2d","zoomIn2d","resetScale2d"]})
    
    return fig

@st.cache_data(show_spinner=False)
def fig_particuiere():
    fig=px.bar(pd.crosstab(data["Churn Label"],data["City"]).T.loc[data["City"].value_counts().head(15).index.tolist(),:],text_auto=True)

    fig.update_layout(margin=dict(t=30,l=0,r=0,b=5),
                      xaxis=dict(showgrid=False,color='white',title="",tickfont_size=10),
                      yaxis=dict(showgrid=False,color='white',title="",showticklabels=False),
                  title=dict(x=0.2,font_color="white",font_size=15,
                             text='Répartition des client par 20 top lieux de residence et par status de churn'),
                      paper_bgcolor="#4F4F4F",plot_bgcolor="#4F4F4F",height=300,width=750,
                 legend=dict(orientation="h",title='',x=0.8,y=0.8,font_color="white"))
    #fig.show(config={"modeBarButtonsToRemove":["pan2d","select2d","lasso2d","zoom2d","zoomOut2d","zoomIn2d","resetScale2d"]})

    return fig


nb_client=data.shape[0]
nb_churn = (data["Churn Label"]=='Yes').sum()
nb_not_churn=(data["Churn Label"]=='No').sum()

total_vil = data["City"].nunique()

_1,_2,_3,_4=st.columns(4)

_1.metric("Nombre de client",nb_client)
_2.metric("effectifs des désabonées",nb_churn)
_3.metric("effectifs d'abonées",nb_not_churn)
_4.metric("effectifs des villes deservie",total_vil)
style_metric_cards(border_left_color="#4F4F4F")

_1,_2 = st.columns([1,2])

with _1: 
    select = st.selectbox("Gender  |-|  Marital Status  |-|  Dependents",["Gender","Married","Dependents"],key="var_1")
    if st.session_state.var_1 =="Gender":
            st.plotly_chart(graphe_pie(variable="Gender",
           titre="Distribution des clients par sexe",
           paper="#4F4F4F",width=260,height=260),use_container_width=True)
    elif st.session_state.var_1 =="Married":
        st.plotly_chart(graphe_pie(variable="Married",titre="Distribution des clients par <br> statut marital",
           paper="#4F4F4F",width=260,height=260),use_container_width=True)
    elif st.session_state.var_1 =="Dependents":
        st.plotly_chart(graphe_pie(variable="Dependents",titre="Distribution des clients par<br> statut de charge",
           paper="#4F4F4F",width=260,height=260),use_container_width=True)
        
    st.plotly_chart(graphe_bar(variable = "City",titre="Top 20 des lieux de residences des clients",
           orient="h",height=400,width=500,top=20,paper="#4F4F4F"),use_container_width=True)
    
with _2:
    st.plotly_chart(histogram(variable="Age",titre="repartition des clients par age",width=750,height=340,paper="#4F4F4F"),use_container_width=True)         
    
    select2 = st.selectbox("Chrun vs ---   Gender  |-|  Marital Status  |-|  Dependents",["Gender","Married","Dependents"],key="var_2")
    if st.session_state.var_2 =="Gender":
            st.plotly_chart(bar_biplot(var1="Churn Label",var2="Gender",
           title="Répartition des clients par sexes et par status de churn",
           height=300,width=700,paper="#4F4F4F"),use_container_width=True)
    elif st.session_state.var_2 =="Married":
        st.plotly_chart(bar_biplot(var1="Churn Label",var2="Married",
           title='Répartition des clients par status matrimonial et par sexe',
           height=300,width=700,paper="#4F4F4F"),use_container_width=True)
        
    elif st.session_state.var_2 =="Dependents":
        st.plotly_chart(bar_biplot(var1="Churn Label",var2="Dependents",
           title="repartition du churn par chage des clients ",
           height=325,width=700,paper="#4F4F4F"),use_container_width=True)
        
_1,_2=st.tabs(["Graphiue","carte"])

with _1:
    st.plotly_chart(fig_particuiere(),use_container_width=True)

with _2:
    grouped_df = data[['Latitude', 'Longitude',"City","Churn Label"]].groupby('City').agg({
    'Latitude': 'mean',
    'Longitude': 'mean',
    'Churn Label': 'count'  # Utiliser la somme pour représenter la taille
     }).reset_index()
    
    fig = px.scatter_mapbox(grouped_df, lat='Latitude',title="Repartition des clients par city", 
                            lon='Longitude', size='Churn Label',hover_name='City', zoom=6,height=600)

     # Mettre à jour le style de la carte
    fig.update_layout(mapbox_style="open-street-map",title=dict(x=0.2,font_size=30),
                      paper_bgcolor="#4F4F4F",
                      plot_bgcolor="#4F4F4F",margin=dict(t=60,l=0,r=0,b=5))
    st.plotly_chart(fig,use_container_width=True)