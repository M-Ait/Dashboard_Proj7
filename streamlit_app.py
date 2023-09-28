"""import streamlit"""
import pickle
import streamlit as st
import pandas as pd
import numpy as np
import home
import general
import client

st.set_page_config(layout="wide", page_title='Dashboard Projet 7')


@st.cache_data(persist=True)
def load_data():
    """Cache : pas besoin d'exécuter load_data() à chaque reload"""
    application1 = pd.read_csv('static/app_test1.csv')
    application2 = pd.read_csv('static/app_test2.csv')
    application = pd.concat([application1, application2], axis=0, ignore_index=True)

    past_application = pd.read_csv('static/data_train_head.csv')
    past_application['SK_ID_CURR'] = past_application['SK_ID_CURR'].astype(int)
    for col in past_application.columns:
        if past_application[col].max() == 1:
            past_application[col] = past_application[col].astype(int)

    description = pd.read_csv('static/HomeCredit_columns_description.csv',
                              encoding='unicode_escape')
    with open('static/shap_explainer_lgbm.p', 'rb') as file:
        shap_explain = pickle.load(file)

    with open('static/shap_val01.p', 'rb') as file:
        shap_val01 = pickle.load(file)
    with open('static/shap_val02.p', 'rb') as file:
        shap_val02 = pickle.load(file)
    with open('static/shap_val11.p', 'rb') as file:
        shap_val11 = pickle.load(file)
    with open('static/shap_val12.p', 'rb') as file:
        shap_val12 = pickle.load(file)
    shap_val0 = np.concatenate((shap_val01, shap_val02), axis=0)
    shap_val1 = np.concatenate((shap_val11, shap_val12), axis=0)
    shap_value = [shap_val0, shap_val1]
    return application, past_application, description, shap_explain, shap_value


applications, past_applications, descriptions, shap_explainer, shap_values = load_data()


def main():
    """Layout de l'app"""
    st.sidebar.write('# Prêt à dépenser')
    st.sidebar.write("## Utilisateur :", st.session_state.user)
    st.sidebar.title('Navigation')
    options = st.sidebar.radio('Choisir une page :',
                               ['Accueuil', 'Informations générales', 'Informations client'])

    if options == 'Accueuil':
        home.home()
    elif options == 'Informations générales':
        general.general(past_applications, descriptions,
                        applications, shap_values)
    elif options == 'Informations client':
        client.client(applications, shap_values, shap_explainer)


# Initialization
if 'user' not in st.session_state:
    st.session_state.user = ''
if 'password' not in st.session_state:
    st.session_state.password = ''
if 'loginOK' not in st.session_state:
    st.session_state.loginOK = False

if ~st.session_state.loginOK:
    user_placeholder = st.empty()
    pwd_placeholder = st.empty()
    user = user_placeholder.text_input(
        "Entrez un nom d'utilisateur:", value="")
    st.session_state.user = user
    pwd = pwd_placeholder.text_input(
        "Mot de passe:", value="", type="password")
    st.session_state.password = pwd
    if st.session_state.password == 'mdp':
        st.session_state.loginOK = True
        user_placeholder.empty()
        pwd_placeholder.empty()
        main()
    else:
        st.error("Mot de passe incorrect")
else:
    main()

# End of file
