# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Configuration de la page
st.set_page_config(
    page_title="Classification de la Qualité des Produits Cimentiers",
    page_icon=":factory:",
    layout='wide',
    initial_sidebar_state='expanded'
)

# Charger les modèles
rc2_model = joblib.load('RC2_classification_randomforest.pkl')['random_forest']
rc28_model = joblib.load('RC28_classification_randomforest.pkl')['random_forest']
# Charger le modèle et les meilleurs paramètres
optimal_model = joblib.load('optimal_model.pkl')
best_params = joblib.load('best_params.pkl')

# Charger les données
data = pd.read_excel('Base de donnée Stage.xlsx', header=2)

# Chargement du CSS personnalisé
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Affichage du logo dans la barre latérale
st.sidebar.image('cimar.png')

# Options de la barre latérale avec boutons radio et emojis
st.sidebar.subheader('Sélectionnez une page')
page = st.selectbox('Choisir une page', 
        ('🏠 Accueil', '⚙️ Classification<br>et optimisation en utilisant RC2j', '⚙️ Classification<br>et optimisation en utilisant RC28j', '📋 Informations Techniques'), 
        format_func=lambda x: x.replace("<br>", "\n"))

# Fonction pour afficher la page d'accueil
def home():
    st.markdown("""
        <div class="main-content">
            <div class="app-background">
                <div class="rectangle">
                    <h1 class="title">Classification des produits cimentiers CPJ45 de l'usine de Jorf</h1>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Fonction pour afficher la page RC2j
def rc2_page():
    st.markdown("""
        <style>
        .custom-col { padding: 10px; border-radius: 10px; }
        .custom-col1 { background-color: #f0f8ff; }
        .custom-col2 { background-color: #e6ffe6; }
        .custom-col3 { background-color: #fffacd; }
        .custom-col4 { background-color: #f5f5dc; }
        .custom-form { border: 2px solid #ddd; padding: 20px; border-radius: 15px; }
        .custom-success { color: #28a745; }
        .custom-error { color: #dc3545; }
        </style>
        <h1 style='text-align: center; color: #2F4F4F;'>Classification et optimisation en utilisant RC2j</h1>
        """, unsafe_allow_html=True)
    
    st.write("Veuillez entrer les valeurs demandées ci-dessous :")

    with st.form(key='rc2_form'):
        # Entrée des valeurs pour les paramètres
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-col custom-col1">', unsafe_allow_html=True)
            PAF_CV = st.number_input('PAF CV', value=0.0)
            SiO2 = st.number_input('SiO2', value=0.0)
            Al2O3 = st.number_input('Al2O3', value=0.0)
            Fe2O3 = st.number_input('Fe2O3', value=0.0)
            CaO = st.number_input('CaO', value=0.0)
            MgO = st.number_input('MgO', value=0.0)
            SO3_cl = st.number_input('SO3 cl', value=0.0)
            K2O = st.number_input('K2O', value=0.0)
            PAF_cl = st.number_input('PAF cl', value=0.0)
            CaOl = st.number_input('CaOl', value=0.0)
            C3A = st.number_input('C3A', value=0.0)
            C3S = st.number_input('C3S', value=0.0)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="custom-col custom-col2">', unsafe_allow_html=True)
            SO3_g = st.number_input('SO3 g', value=0.0)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-col custom-col3">', unsafe_allow_html=True)
            percent_clinker = st.number_input('%clinker', value=0.0)
            percent_CV = st.number_input('% CV', value=0.0)
            percent_gypse = st.number_input('% gypse', value=0.0)
            Refus_40_m = st.number_input('Refus 40 μm', value=0.0)
            st.markdown('</div>', unsafe_allow_html=True)

        submit_button = st.form_submit_button("Soumettre", use_container_width=True)

        if submit_button:
            input_data = pd.DataFrame({
                'PAF CV ': [PAF_CV],
                'SiO2': [SiO2],
                'Al2O3': [Al2O3],
                'Fe2O3': [Fe2O3],
                'CaO': [CaO],
                'MgO': [MgO],
                'SO3 cl': [SO3_cl],
                'K2O': [K2O],
                'PAF cl': [PAF_cl],
                'CaOl ': [CaOl],
                'C3A': [C3A],
                'C3S': [C3S],
                'SO3 g': [SO3_g],
                '%clinker': [percent_clinker],
                '% CV': [percent_CV],
                '% gypse': [percent_gypse],
                'Refus 40 μm': [Refus_40_m]
            })

            prediction = optimal_model.predict(input_data)

            if prediction[0] == 1:
                st.markdown("<p class='custom-success'>✅ Vu que la résistance RC2j dépasse 13.5 MPa, alors votre produit est de bonne qualité.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='custom-error'>❌ Vu que la résistance RC2j est inférieure à 13.5 MPa, alors votre produit n'est pas de bonne qualité.</p>", unsafe_allow_html=True)

    # Section pour prédire les paramètres optimaux
    st.subheader("Prédiction des Paramètres Optimaux")

    # Demander à l'utilisateur d'entrer la valeur souhaitée de RC2j
    rc2j_value = st.number_input("Entrez la valeur souhaitée de RC2j :", min_value=0.0)

    # Bouton pour prédire les paramètres optimaux
    if st.button("Prédire les Paramètres Optimaux"):
        optimal_parameters = predict_optimal_parameters(rc2j_value, optimal_model, best_params)
        st.write("Les paramètres optimaux pour la valeur de RC2j souhaitée sont :")
        st.write(optimal_parameters)

# Fonction pour afficher la page RC28j
def rc28_page():
    st.markdown("""
        <style>
        .custom-col { padding: 10px; border-radius: 10px; }
        .custom-col1 { background-color: #f0f8ff; }
        .custom-col2 { background-color: #e6ffe6; }
        .custom-col3 { background-color: #fffacd; }
        .custom-col4 { background-color: #f5f5dc; }
        .custom-form { border: 2px solid #ddd; padding: 20px; border-radius: 15px; }
        .custom-success { color: #28a745; }
        .custom-error { color: #dc3545; }
        </style>
        <h1 style='text-align: center; color: #2F4F4F;'>Classification et optimisation en utilisant RC28j</h1>
        """, unsafe_allow_html=True)
    
    st.write("Veuillez entrer les valeurs demandées ci-dessous :")

    with st.form(key='rc28_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-col custom-col1">', unsafe_allow_html=True)
            PAF_CV = st.number_input('PAF CV', value=0.0)
            SiO2 = st.number_input('SiO2', value=0.0)
            Al2O3 = st.number_input('Al2O3', value=0.0)
            Fe2O3 = st.number_input('Fe2O3', value=0.0)
            CaO = st.number_input('CaO', value=0.0)
            MgO = st.number_input('MgO', value=0.0)
            SO3_cl = st.number_input('SO3 cl', value=0.0)
            K2O = st.number_input('K2O', value=0.0)
            PAF_cl = st.number_input('PAF cl', value=0.0)
            CaOl = st.number_input('CaOl', value=0.0)
            C3A = st.number_input('C3A', value=0.0)
            C3S = st.number_input('C3S', value=0.0)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="custom-col custom-col2">', unsafe_allow_html=True)
            SO3_g = st.number_input('SO3 g', value=0.0)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-col custom-col3">', unsafe_allow_html=True)
            percent_clinker = st.number_input('%clinker', value=0.0)
            percent_CV = st.number_input('% CV', value=0.0)
            percent_gypse = st.number_input('% gypse', value=0.0)
            Refus_40_m = st.number_input('Refus 40 μm', value=0.0)
            st.markdown('</div>', unsafe_allow_html=True)

        submit_button = st.form_submit_button("Soumettre", use_container_width=True)

        if submit_button:
            input_data = pd.DataFrame({
                'PAF CV ': [PAF_CV],
                'SiO2': [SiO2],
                'Al2O3': [Al2O3],
                'Fe2O3': [Fe2O3],
                'CaO': [CaO],
                'MgO': [MgO],
                'SO3 cl': [SO3_cl],
                'K2O': [K2O],
                'PAF cl': [PAF_cl],
                'CaOl ': [CaOl],
                'C3A': [C3A],
                'C3S': [C3S],
                'SO3 g': [SO3_g],
                '%clinker': [percent_clinker],
                '% CV': [percent_CV],
                '% gypse': [percent_gypse],
                'Refus 40 μm': [Refus_40_m]
            })

            prediction = rc28_model.predict(input_data)

            if prediction[0] == 1:
                st.markdown("<p class='custom-success'>✅ Vu que la résistance RC28j dépasse 24 MPa, alors votre produit est de bonne qualité.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='custom-error'>❌ Vu que la résistance RC28j est inférieure à 24 MPa, alors votre produit n'est pas de bonne qualité.</p>", unsafe_allow_html=True)

# Fonction pour afficher les informations techniques
def technical_info():
    st.markdown("""
        <h1 style='text-align: center; color: #2F4F4F;'>Informations Techniques</h1>
        <p style='text-align: justify;'>Dans cette section, vous pouvez fournir des informations techniques sur les produits cimentiers, les méthodes de production, et les normes de qualité.</p>
        """, unsafe_allow_html=True)

# Afficher la page sélectionnée
if page == '🏠 Accueil':
    home()
elif page == '⚙️ Classification et optimisation en utilisant RC2j':
    rc2_page()
elif page == '⚙️ Classification et optimisation en utilisant RC28j':
    rc28_page()
elif page == '📋 Informations Techniques':
    technical_info()
