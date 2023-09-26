"""import requests"""
import requests
import shap
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO


def client(app_test, shap_values, shap_explainer):
    """Informations relatives à un client"""
    st.title("Informations client")
    url = "https://flask-proj7.onrender.com"
    response = requests.get(url + "/possible_input", timeout=120).json()
    list_client_id = response['possible_client_ID']
    left, right = st.columns(2)
    left.write("Sélectionner un identifiant :")
    client_id = right.selectbox(label="Liste d'identifiants valides",
                                options=list_client_id)

    st.write(":tada:  Client identifié   :   ", client_id)
    
    st.subheader("Données et score de prédiction")

    st.text("Informations client")
    if st.checkbox("Montrer les informations :eyes:"):
        client_infos = app_test.loc[app_test['SK_ID_CURR']==client_id]
        st.dataframe(client_infos)
    
    st.text("Score et prédiction")
    if st.checkbox("Montrer la prédiction :eyes:"):
        st.write("""
        **A savoir**
                
            La prédiction est un score de 0 à 1
            Le seuil de refus est à 0.1
            Une prédiction inférieure à 0.1 est une acceptation du crédit
        """)
        response1 = requests.get(url + "/predict/" + str(client_id), timeout=10).json()
        prediction_initiale = int(response1['prediction_initiale'])
        prediction_revisitee = int(response1['prediction_revisitee'])
        probabilite_refus = response1['probabilite_refus']
        if prediction_initiale==1:
            pred = "Demande de prêt refusée"
            l, r = st.columns(2)
            l.write(f"Prédiction initiale :")
            r.write(f":red[**{pred}**]")
        else:
            pred = "Demande de prêt acceptée"
            l, r = st.columns(2)
            l.write(f"Prédiction initiale :")
            r.write(f":green[**{pred}**]")
        if prediction_revisitee==1:
            pred1 = "Demande de prêt refusée"
            l1, r1 = st.columns(2)
            l2, r2 = st.columns(2)
            l1.write("Score (probabilité de refus de la demande) : ")
            r1.write(f":red[**{probabilite_refus}**]")
            l2.write("Prédiction finale (après ajustement du seuil) : ")
            r2.write(f":red[**{pred1}**]")
        else:
            pred1 = "Demande de prêt acceptée"
            l1, r1 = st.columns(2)
            l2, r2 = st.columns(2)
            l1.write("Score (probabilité de refus de la demande) : ")
            r1.write(f":green[**{probabilite_refus}**]")
            l2.write("Prédiction finale (après ajustement du seuil) : ")
            r2.write(f":green[**{pred1}**]")

    st.subheader("Interprétation du score")

    st.text("Valeurs SHAP")
    if st.checkbox("Montrer l'impact des variables sur le score :eyes:"):
        st.write("""
        **A savoir**
                 
            Les variables sont classées de haut en bas par ordre d'importance 
            Les variables en rouge font augmenter le score et donc le risque de defaut de paiement
            Inversement pour les variables en bleu
        """)
        app_test.reset_index(inplace=True, drop=True)
        data = app_test.drop(columns=['SK_ID_CURR'])
        index = app_test.loc[app_test['SK_ID_CURR']==client_id].index
        force_plot = shap.plots.force(shap_explainer.expected_value[1],
                                      shap_values[1][index],
                                      data.iloc[index, :],
                                      matplotlib=True,
                                      text_rotation=45)
        st.pyplot(force_plot)

    st.text("Dépendences inter-variables")
    if st.checkbox("Montrer les graphes de dépendences :eyes:"):
        X = st.selectbox(label="Variable principale / Abscisse :", options=data.columns)
        Y = st.selectbox(label="En fonction de :", options = data.columns)

        fig, ax = plt.subplots(figsize=(10, 5))
        shap.dependence_plot(X,
                             shap_values[0],
                             data,
                             interaction_index=Y,
                             ax=ax)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)

        """
        dependence_plot = shap.dependence_plot(X,
                                               shap_values[0],
                                               data,
                                               interaction_index=Y)
        st.pyplot(dependence_plot)
        """
        
# End of file
