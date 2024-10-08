import streamlit as st
import joblib

# Configuration de la page
st.set_page_config(
    page_title="Classification de la Qualité des Produits Cimentiers",
    page_icon=":factory:",
    layout='wide',
    initial_sidebar_state='expanded'
)

# Charger le modèle
try:
    rc2_model = joblib.load('RC2.pkl')
    # Vérifiez le type du modèle chargé
    st.write(f"Type du modèle RC2: {type(rc2_model)}")
    
    # Vérifiez si le modèle a la méthode 'predict'
    if hasattr(rc2_model, 'predict'):
        st.write("Le modèle a la méthode 'predict'.")
    else:
        st.write("Le modèle n'a pas la méthode 'predict'.")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle RC2: {e}")

# Autres parties de votre code...
