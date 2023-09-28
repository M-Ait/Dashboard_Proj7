"""import shap"""
import shap
import streamlit as st


# Informations demandes passées
def general(data_train, var_descriptions, data_test, shap_values):
    """Informations générales"""
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title("Informations générales")
    st.subheader("Exploration des données")

    st.text("Echantillon des informations utilisées")
    st.table(data_train)
    st.text("Descriptions des colonnes")
    if st.checkbox("Montrer la description des colonnes :eyes:"):
        rows = var_descriptions.sort_values(by='Row')
        colonne = st.selectbox(label='Choisir une colonne :',
                               options=rows.Row.unique())
        df_ = var_descriptions[var_descriptions['Row'] == colonne]
        df_.reset_index(drop=True, inplace=True)
        st.dataframe(df_[['Row', 'Description']].head(1))

    st.text("Statuts des prêts archivés")
    if st.checkbox("Montrer la distribution des statuts de paiement :eyes:"):
        st.image('static/pie_chart.png')

    st.subheader("Interprétabilité du modèle : SHAP")

    st.text("Impacts des variables sur la prédiction")
    if st.checkbox("Montrer l'impact des variables les plus importantes :eyes:"):
        st.write("""
        **A savoir**
                 
            Les variables sont classes de haut en bas par ordre d'importance 
            L'impact sur la prediction est representé par les shap_values en abscisse :
                  
            A gauche  -> impact négatif sur la prédiction
            A droite  -> impact positif sur la prédiction
        """)
        st.slider("Sélectionner le nombre de variables :", min_value=3, max_value=20,
                  value=3, step=1, key="max_display")
        shap.initjs()
        fig1 = shap.summary_plot(shap_values[0],
                                 data_test.drop(columns=['SK_ID_CURR']),
                                 max_display=st.session_state.max_display)
        st.pyplot(fig1)
# End of file
