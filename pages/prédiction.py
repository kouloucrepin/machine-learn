import streamlit as st
import main
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import roc_curve, roc_auc_score,confusion_matrix
import seaborn as sns
import scipy.stats as sct


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


s=main.data.select_dtypes("object").nunique()
var_qual =s[(s>1 ) & (s<=5)]
var_quant = main.data.select_dtypes(exclude="object").columns

dictio= {"var":[],"p-value":[],"status_var":[]}
for i in var_qual.index.to_list():
    if i!='Churn Label':
        st_chi2, st_p, st_dof, st_exp = sct.chi2_contingency(pd.crosstab(main.data['Churn Label'],
                                                                 main.data[i]).fillna(0).astype(int))
        dictio['p-value'].append(st_p)
        dictio['var'].append(i)
        dictio['status_var'].append(st_p<=0.05)
dictio = pd.DataFrame(dictio)

p_val  = dictio.query("status_var==True")
p_val = p_val.loc[p_val["p-value"]<=p_val["p-value"].mean(),:]

var_ual = p_val["var"].tolist()

corr_ = main.data[var_quant].corr().unstack().to_frame().reset_index()

def correlation(x):
    return  "_".join(sorted([x["level_0"],x["level_1"]]))
 
so=corr_.loc[(corr_[0].abs()>0.5),["level_0","level_1"]]
so["concat"]=so.apply(lambda x : correlation(x),axis=1)
a = so.groupby("level_0").size().to_frame().reset_index()
li_fort = a.loc[a[0]>=2,:].level_0.tolist()
var_uan = []
for i in var_quant:
    if i not in li_fort:
        var_uan.append(i)

X = pd.concat([main.data[var_ual],main.data[var_uan]],axis=1)
y = main.data["Churn Label"].replace({"Yes":1,"No":0}).values.reshape(-1,1)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
 
column_transformer = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), var_uan),
        ('cat', OneHotEncoder(drop="first"), var_ual)
    ]
)

pipeline = Pipeline([
    ('scaler', column_transformer),  # Étape de normalisation
    ('logistic', LogisticRegression(penalty='l1', C=1.0,solver = "liblinear"))  # Étape de régression logistique
])

pipeline.fit(x_train, y_train)


def roc_curve_plot(x_train=x_train,x_test=x_test,y_train=y_train):
    y_probs = pipeline.predict_proba(x_test)[:, 1]
    y_probt = pipeline.predict_proba(x_train)[:, 1]

    # Calculer la courbe ROC
    fpr, tpr, thresholds = roc_curve(y_test, y_probs)
    fprt, tprt, thresholdst = roc_curve(y_train, y_probt)

    roc_auc = roc_auc_score(y_test, y_probs)
    roc_auct = roc_auc_score(y_train, y_probt)

    fig, ax = plt.subplots()

    # Tracer la courbe ROC
    ax.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve_test_set (area = {roc_auc:.2f})')
    ax.plot(fprt, tprt, color='blue', lw=2, label=f'ROC curve_train_se (area = {roc_auct:.2f})')
    ax.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')

   # Ajouter des labels et un titre
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver Operating Characteristic')
    ax.legend(loc="lower right")
    return fig


def confusion_plot(x_train=x_train,x_test=x_test,y_train=y_train):
    cm = confusion_matrix(y_test, pipeline.predict(x_test))
    df_cm = pd.DataFrame(cm, index=[0,1], columns=[0,1])
    df_cm_tr = pd.DataFrame(confusion_matrix(y_train, pipeline.predict(x_train)),
                        index=[0,1], columns=[0,1])


    # Afficher la matrice de confusion avec Seaborn
    fig, ax = plt.subplots(2,1,figsize=(14,15))
    sns.heatmap(df_cm, annot=True, fmt='d', cmap='Blues',ax=ax[0])
    ax[0].set_xlabel('Étiquettes prédites')
    ax[0].set_ylabel('Étiquettes réelles')
    ax[0].set_title('Matrice de Confusion(test_set)')

    sns.heatmap(df_cm_tr, annot=True, fmt='d', cmap='Blues',ax=ax[1])
    ax[1].set_xlabel('Étiquettes prédites')
    ax[1].set_ylabel('Étiquettes réelles')
    ax[1].set_title('Matrice de Confusion(train_set)')
    return fig

_1,_2 = st.columns([3,2])
_1.pyplot(roc_curve_plot(x_train=x_train,x_test=x_test,y_train=y_train),use_container_width=True)

_2.pyplot(confusion_plot(),use_container_width=True)


a= pipeline.named_steps['scaler'].named_transformers_["cat"].get_feature_names_out().tolist()
b = pipeline.named_steps['scaler'].named_transformers_["num"].get_feature_names_out().tolist()
b.extend(a)


ax,fig = plt.subplots(figsize=(12,9))

pd.DataFrame({"variable":b,"importance":pipeline.named_steps['logistic'].coef_[0]}).set_index("variable").sort_values(by='importance',ascending=False).plot.bar(ax=fig)
fig.set_title("Repartition de l'importance des variable")
st.pyplot(ax)
