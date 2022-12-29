# pour créer une application web interactive en Python
import streamlit as st

# pour manipuler des données structurées au format json
import json

# pour l'analyse et la visualisation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import folium

# pour intégrer des cartes interactives Folium dans une application Streamlit
import streamlit_folium

# Affichage de l'application en plein écran
st.set_page_config(page_title="Data analyse - VISUALISATION", page_icon="logo_SNCF.png", layout="centered")

# Ajouter un titre et un logo à la page web
st.image(image = "logo_SNCF.png")
st.title("Data analyse - VISUALISATION")

# on lit les fichiers csv
df_count = pd.read_csv("dataframes/objets_perdus_par_semaine.csv")
df_semaine_type = pd.read_csv("dataframes/itemlost_type_week.csv")
df_data = pd.read_csv("dataframes/data_voy_objet_code.csv")
df_data['date'] = pd.to_datetime(df_data['date'], format='%Y')


# on renomme les colonnes pour la lecture interactive du graphique dans la question 2
df_semaine_type = df_semaine_type.rename(columns={'type_objet':"types d'objets", 'nombre_objets_perdus':"nombre d'objets perdus"})


# on ouvre le fichier "departements-france.geojson" en mode lecture et le charge dans une variable mon_fichier
with open("departements-france.geojson") as mon_fichier:
    # on chargé les données dans la variable geo sous la forme d'un dictionnaire
    geo = json.load(mon_fichier)



# Création des onglets de l'application en utilisant la fonction st.tabs
tab1,tab2,tab3 = st.tabs(["Question n°1","Question n°2","Question n°3"])


with tab1 :
    ### Partie visualisation - Afficher sur un histogramme la répartition de des valeurs (un point correspond à une semaine dont la valeur est la somme). ###

    # Créez une figure et un axe avec Matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))

    # Donnez un titre à l'histogramme et nommez les axes
    ax.set_title("Nombre de semaines en fonction du nombre d'objets perdus (2016-2021)")
    ax.set_xlabel("Nombre d'objets perdus")
    ax.set_ylabel("Nombre de semaines")

    # Appliquez un style
    sns.set_style("darkgrid")

    # Tracez l'histogramme
    sns.histplot(data=df_count, x="nombre_objets_perdus", bins=52, edgecolor='black', fill='#006699', ax=ax)

    # Affichez la figure dans votre application Streamlit en utilisant st.pyplot
    st.pyplot(fig)


with tab2:
    # on définit la liste des types d'objets (on ajoute l'option "tous les types")
    liste_type = np.append(df_semaine_type["types d'objets"].unique(), 'tous les types')

    # Afficher une liste déroulante permettant de sélectionner les types d'objets à afficher dans le graphique
    selected_types = st.multiselect("Sélectionnez les types d'objets à afficher :", liste_type)

    # Filtrer les données en fonction de la sélection de l'utilisateur
    df = df_semaine_type[df_semaine_type["types d'objets"].isin(selected_types)]


    if selected_types == ["tous les types"]:
        df_filtered = df_count.rename(columns={'nombre_objets_perdus':"nombre d'objets perdus"})
        fig = px.line(df_filtered, x="date", y="nombre d'objets perdus",title="Evolution du nombre d'objets perdus sur la période 2016-2021")  
    else:
        df_filtered = df[df["types d'objets"].isin(selected_types)]
        
        # on trace une courbe avec plotly express (px)
        fig = px.line(df_filtered, x="date", y="nombre d'objets perdus",title="Evolution du nombre d'objets perdus sur la période 2016-2021", color="types d'objets")  

    # on définit le titre et les noms des axes
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Nombre d'objets perdus",
        legend_title="Types d'objets",
        showlegend=True,
    )

    # Affichage
    st.plotly_chart(fig)


with tab3:

    # on sélectionne le type d'objet et l'année pour filtrer les données
    mask_objet = st.selectbox("Choisissez un type d'objet",df_data["type_objet"].unique(),key='quest3objet')
    mask_date = st.selectbox("Choisissez une annee", df_data["date"].dt.year.unique(), key='quest3year')
    
    # on filtre les données vérifiant les conditions 
    new_df = df_data[(df_data["date"].dt.year == int(mask_date)) & (df_data["type_objet"] == mask_objet)]
    
    # on crée un objet cartographique Folium centré sur la France
    france = folium.Map(location = [46.763656, 2.429795], zoom_start = 6)

    # voir notebook data_analyse_visualisation pour comprendre les lignes
    folium.Choropleth(
        geo_data=geo,
        name="France departements",
        data=new_df,
        columns=["code_departement","nombre d'objets perdus par type"],
        key_on="feature.properties.code",
        fill_color="YlGn",
        legend_name=f"Nombre d'objets de type {mask_objet} perdus en {mask_date}",
    ).add_to(france)

    # Affichage de la carte sur le streamlit
    streamlit_folium.st_folium(france)