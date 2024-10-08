# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import streamlit as st
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
page = st.sidebar.radio(
    'Choisissez une option', 
    ['🏠 Accueil', '⚙️ Classification avec RC2j', '⚙️ Classification avec RC28j', '📋 Informations Techniques'],
    format_func=lambda x: x[:30] + '...' if len(x) > 30 else x
)

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
import streamlit as st
import pandas as pd

# Charger le modèle et les meilleurs paramètres
optimal_model = joblib.load('optimal_model.pkl')
best_params = joblib.load('best_params.pkl')

# Charger les données à partir du fichier Excel
dataset = pd.read_excel('Base de donnée Stage.xlsx', header=2)  # Charger le fichier Excel

# Fonction pour nettoyer les colonnes numériques
def clean_numeric_columns(df):
    for col in df.columns:
        # Remplacer les virgules par des points pour la conversion en float
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        # Remplacer les fractions par leur valeur numérique moyenne
        df[col] = df[col].str.split('/').apply(lambda x: float(x[0]) / float(x[1]) if len(x) == 2 else float(x[0]) if x else np.nan)
        # Convertir en float, en forçant les erreurs à NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Nettoyer les données
dataset = clean_numeric_columns(dataset)

# Supprimer la première colonne et les cinq dernières colonnes
dataset = dataset.drop(dataset.columns[0], axis=1)  # Supprimer la première colonne
dataset = dataset.iloc[:, :-5]  # Supprimer les cinq dernières colonnes

# Remplacer les valeurs NaN par la moyenne de chaque colonne
dataset.fillna(dataset.mean(), inplace=True)

# Définir X et y
X = dataset.drop('RC 2j', axis=1)  # Variables indépendantes
y = dataset['RC 2j']  # Variable dépendante

# Fonction pour prédire les paramètres optimaux
def predict_optimal_parameters(target_value, model, best_params):
    # Entraîner le modèle avec les meilleurs paramètres
    optimal_model = RandomForestRegressor(**best_params)
    optimal_model.fit(X, y)  # Entraîner le modèle sur X et y

    # Prédire les valeurs en fonction de RC 2j
    predictions = optimal_model.predict(X)

    # Identifier les paramètres correspondant à la valeur cible
    optimal_parameters = X.iloc[np.abs(predictions - target_value).argmin()]
    return optimal_parameters

# Fonction de la page rc2
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
        <h1 style='text-align: center; color: #2F4F4F;'>Classification des produits cimentiers en se basant sur RC2j</h1>
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

# Charger le modèle et les meilleurs paramètres pour RC28j
rc28_model = joblib.load('optimal_model_RC28.pkl')
best_params_rc28 = joblib.load('best_params_RC28.pkl')

# Fonction pour nettoyer les colonnes numériques
def clean_numeric_columns(df):
    for col in df.columns:
        # Remplacer les virgules par des points pour la conversion en float
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        # Remplacer les fractions par leur valeur numérique moyenne
        df[col] = df[col].str.split('/').apply(lambda x: float(x[0]) / float(x[1]) if len(x) == 2 else float(x[0]) if x else np.nan)
        # Convertir en float, en forçant les erreurs à NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

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
        <h1 style='text-align: center; color: #2F4F4F;'>Classification des produits cimentiers en se basant sur RC28j</h1>
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

            if 34 <= prediction[0] <= 55:  # Assumer que la sortie est une résistance RC28j
                st.markdown("<p class='custom-success'>✅ Vu que la résistance RC28j varie entre 34 et 55 MPa, alors votre produit est de bonne qualité.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='custom-error'>❌ Vu que la résistance RC28j est inférieure à 34 MPa, alors votre produit n'est pas de bonne qualité.</p>", unsafe_allow_html=True)

    # Section pour prédire les paramètres optimaux
    st.subheader("Prédiction des Paramètres Optimaux")

    # Demander à l'utilisateur d'entrer la valeur souhaitée de RC28j
    rc28j_value = st.number_input("Entrez la valeur souhaitée de RC28j :", min_value=0.0)

    # Bouton pour prédire les paramètres optimaux
    if st.button("Prédire les Paramètres Optimaux"):
        optimal_parameters = predict_optimal_parameters(rc28j_value, rc28_model, best_params_rc28)
        st.write("Les paramètres optimaux pour la valeur de RC28j souhaitée sont :")
        st.write(optimal_parameters)

def info_tech_page():
    st.title("📋 Informations Techniques")

    # Utilisation du Markdown avec HTML pour ajouter des couleurs
    st.markdown("""
        <style>
        .info-box {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .info-box h4 {
            color: #007bff;
        }
        .info-box p {
            color: #495057;
        }
        .highlight {
            color: #dc3545;
            font-weight: bold;
        }
        .metrics-table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
        .metrics-table th, .metrics-table td {
            border: 1px solid #e0e0e0;
            padding: 10px;
            text-align: left;
        }
        .metrics-table th {
            background-color: #007bff;
            color: #fff;
        }
        .metrics-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .metrics-table td {
            color: #495057;
        }
        </style>
        <div class="info-box">
            <h4>Description des Paramètres :</h4>
            <p><span class="highlight">PAF CV</span> : Perte au feu du cendre volante, mesurant la réduction du poids due à la décomposition thermique.</p>
            <p><span class="highlight">SiO2</span> : Dioxyde de silicium, un composant clé dans la production de ciment, essentiel pour la résistance mécanique du produit fini.</p>
            <p><span class="highlight">Al2O3</span> : Oxyde d'aluminium, utilisé pour réguler le temps de prise du ciment et améliorer ses propriétés mécaniques.</p>
            <p><span class="highlight">Fe2O3</span> : Oxyde de fer, qui influence la couleur et certaines caractéristiques chimiques du clinker.</p>
            <p><span class="highlight">CaO</span> : Oxyde de calcium, un composant majeur dérivé du calcaire, responsable de la formation de silicates de calcium, principaux contributeurs à la résistance du ciment.</p>
            <p><span class="highlight">MgO</span> : Oxyde de magnésium, un composé secondaire dont une concentration élevée peut affecter les propriétés du ciment.</p>
            <p><span class="highlight">SO3 cl</span> : Oxyde de soufre dans le clinker, reflétant la quantité de soufre issue du combustible utilisé.</p>
            <p><span class="highlight">K2O</span> : Oxyde de potassium, un alkali qui affecte la formation des phases dans le clinker et la réactivité du ciment.</p>
            <p><span class="highlight">PAF cl</span> :La perte au feu du clinker est un paramètre qui mesure la quantité de matière volatile qui est libérée lorsque le clinker est chauffé à une température élevée, généralement autour de 1000-1100 °C .</p>
            <p><span class="highlight">CaOl</span> : Oxyde de calcium libre, représentant la quantité de chaux non réagit, signe d'une cuisson incomplète.</p>
            <p><span class="highlight">C3A</span> : Tricalcium aluminate, responsable de la prise rapide du ciment et de sa résistance initiale.</p>
            <p><span class="highlight">C3S</span> : Tricalcium silicate, principal facteur de la résistance mécanique à court terme (2 à 7 jours) du ciment.</p>
            <p><span class="highlight">SO3 g</span> : Oxyde de soufre dans le gypse, régulateur du temps de prise du ciment.</p>
            <p><span class="highlight">%clinker</span> : Pourcentage de clinker dans le mélange cimentaire, principal constituant réactif du ciment.</p>
            <p><span class="highlight">% CV</span> : Pourcentage du cendre volante.</p>
            <p><span class="highlight">% gypse</span> : Pourcentage de gypse ajouté, utilisé pour réguler le temps de prise du ciment.</p>
            <p><span class="highlight">Refus 40 μm</span> : Proportion des particules supérieures à 40 microns après broyage, affectant la finesse du ciment et sa réactivité.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Classification avec RC2j")
    st.write("""
        La classification des produits cimentiers est réalisée à l'aide de l'algorithme Random Forest, qui a démontré les meilleures performances pour cette tâche.
    """)

    # Tableau des performances du modèle Random Forest pour RC2j
    st.markdown("""
    <table class="metrics-table">
        <thead>
            <tr>
                <th>Métrique</th>
                <th>Valeur</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Précision</strong></td>
                <td>0.8214</td>
            </tr>
            <tr>
                <td><strong>Précision</strong></td>
                <td>0.8424</td>
            </tr>
            <tr>
                <td><strong>F1-score</strong></td>
                <td>0.8973</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Affichage de l'image de la matrice de confusion avec un titre
    st.image("matice_confusion_2.png", caption="Matrice de confusion pour le modèle Random Forest", use_column_width=True)
    st.image("courbe_roc_2.png", caption="La courbe de ROC pour le modèle Random Forest", use_column_width=True)

    st.subheader("Classification avec RC28j")
    st.write("""
        La classification des produits cimentiers pour RC28j est également réalisée à l'aide de l'algorithme Random Forest, en raison de ses excellentes performances.
    """)

    # Tableau des performances du modèle Random Forest pour RC28j
    st.markdown("""
    <table class="metrics-table">
        <thead>
            <tr>
                <th>Métrique</th>
                <th>Valeur</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Précision</strong></td>
                <td>0.9464</td>
            </tr>
            <tr>
                <td><strong>Précision</strong></td>
                <td>0.9478</td>
            </tr>
            <tr>
                <td><strong>F1-score</strong></td>
                <td>0.9724</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Affichage de l'image de la matrice de confusion pour RC28j avec un titre
    st.image("matice_confusion_28.png", caption="Matrice de confusion pour le modèle Random Forest (RC28j)", use_column_width=True)
    st.image("roc.png", caption="La courbe de ROC pour le modèle Random Forest (RC28j)", use_column_width=True)



# Affichage du contenu en fonction du choix de l'utilisateur
if page == '🏠 Accueil':
    home()
elif page == '⚙️ Classification avec RC2j':
    rc2_page()
elif page == '⚙️ Classification avec RC28j':
    rc28_page()
elif page == '📋 Informations Techniques':
    info_tech_page()