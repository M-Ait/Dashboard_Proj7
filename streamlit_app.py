"""import streamlit"""
import pickle
import streamlit as st
import pandas as pd
import home
import general
import client

st.set_page_config(layout="wide", page_title='Dashboard Projet 7')


@st.cache_data
def load_data():
    """Cache : pas besoin d'exécuter load_data() à chaque reload"""
    application = pd.read_csv('static/app_test.csv')
    #test = pd.concat([app_test1, app_test2], axis=0, ignore_index=True)
    past_application = pd.read_csv('static/data_train_head.csv')
    past_application['SK_ID_CURR'] = past_application['SK_ID_CURR'].astype(
        int)
    for col in past_application.columns:
        if past_application[col].max() == 1:
            past_application[col] = past_application[col].astype(int)
    description = pd.read_csv(r'static/HomeCredit_columns_description.csv',
                              encoding='unicode_escape')
    with open(r'static/shap_explainer_lgbm.p', 'rb') as file:
        shap_explain = pickle.load(file)
    with open(r'static/shap_values_lgbm.p', 'rb') as file:
        shap_value = pickle.load(file)
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
