"""import streamlit"""
import streamlit as st

def home():
    """Page d'accueuil"""
    st.title("Page d'accueuil")
    st.image('static/PretADepenser.png', width=300)
    st.write("""
    **1. Informations générales**
             
        Informations sur les demandes de prêt archivées
        Informations sur les données utilisées et interprétaion du modèle de prédiction
            
    **2. Informations client**
             
        Informations sur les demandes de prêt en cours
        Informations anonymisées du client, prediction et interprétation résultat
    """)

    st.error("""
        IMPORTANT
        
        Si la page "Informations client" n'a pas été utilisée depuis au moins 15 minutes,
        le chargement de la page peut prendre jusqu'à 3.5 minutes
        """)

    # End of file
    