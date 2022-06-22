import pandas as pd
import streamlit as st
import altair as alt
from time import strftime
import numpy as np

url = "CC_mere_et_fille.csv"


st.set_page_config(page_title='CC Inventaire', layout='wide')


#########FUNCTIONS#############


def highlight_survived(s):
    return ['background-color: rgba(255, 0, 0, 0.2)']*len(s) if s.Vendu else ['background-color: rgba(0, 255, 0, 0.2)']*len(s)

def color_survived(val):
    color = 'red' if val else 'green'
    return f'background-color: {color}'

def color_boolean(val):
    color =''
    if val == '1':
        color = 'red'
    elif val == '0':
        color = 'green'
    return 'color: %s' % color


################################

menu = st.sidebar.selectbox('Menu', [ 'Voir Inventaire', 'Ajouter Produit', 'Modifier/Vente Produit', 'Analysis', 'Coûts' , 'Recherche'])

if menu == 'Voir Inventaire':
    cc_df = pd.read_csv(url)
    cc_df.drop(cc_df.columns[cc_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    cc_df['Matière'] = cc_df['Matière'].str.title()
    cc_df['Couleur'] = cc_df['Couleur'].str.title()
    cc_df['Matière 2'] = cc_df['Matière 2'].str.title()
    cc_df['Couleur 2'] = cc_df['Couleur 2'].str.title()
    cc_df['Modèle'] = cc_df['Modèle'].str.capitalize()
    cc_df['Taille'] = cc_df['Taille'].str.upper()
    cc_df['Fait par'] = cc_df['Fait par'].str.upper()
    cc_df['Gamme'] = cc_df['Gamme'].str.upper()
    cc_df['Collection'] = cc_df['Collection'].str.title()
    cc_df["Vendu"] = cc_df["Vendu"].astype(int)
    cc_df["Année"] = cc_df["Année"].astype(int)
    cc_df["Prix"] = cc_df["Prix"].astype(int)




    sold = st.sidebar.checkbox('Afficher uniquement les sacs vendus')
    dispo = st.sidebar.checkbox('Afficher les sacs disponibles')
    expander = st.sidebar.expander("Informations")
    expander.text('-rouge: sac vendu')
    expander.text('-vert: sac disponible')
    expander.text("-Filtrer les sacs par vendus ou ")
    expander.text("disponibles dans l'inventaire avec les")
    expander.text(" deux bouttons sur la sidebar")

    if sold:
        st.header('Inventaire des sacs vendus')
        st.dataframe(cc_df[cc_df['Vendu'] > 0], width=1280, height=640)
    
    if not sold and not dispo:
        st.header("Inventaire de l'ensemble des sacs")
        cc_df = cc_df.style.applymap(color_boolean)
        st.dataframe(cc_df, axis=1), width=1280, height=640)

    if dispo:
        st.header('Inventaire des sacs disponibles')
        st.dataframe(cc_df[cc_df['Vendu'] < 1], width=1280, height=640)

    st.write(' - Nombre de sacs disponibles: ' + str(len(cc_df[cc_df['Vendu'] < 1])))
    st.write(' - Nombre de sacs vendus: ' + str(len(cc_df[cc_df['Vendu'] > 0])))


elif menu == 'Ajouter Produit':
    st.header('Ajouter un Produit')

    expander = st.sidebar.expander("Informations")
    expander.text("-Respecter la standardisation des mots, ")
    expander.text("s'il est ecrit avec une majuscule, ")
    expander.text('mettre une majuscule')


    cc_df = pd.read_csv(url)
    cc_df.drop(cc_df.columns[cc_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    cc_df['Matière'] = cc_df['Matière'].str.title()
    cc_df['Couleur'] = cc_df['Couleur'].str.title()
    cc_df['Matière 2'] = cc_df['Matière 2'].str.title()
    cc_df['Couleur 2'] = cc_df['Couleur 2'].str.title()
    cc_df['Modèle'] = cc_df['Modèle'].str.capitalize()
    cc_df['Taille'] = cc_df['Taille'].str.upper()
    cc_df['Fait par'] = cc_df['Fait par'].str.upper()
    cc_df['Gamme'] = cc_df['Gamme'].str.upper()
    cc_df['Collection'] = cc_df['Collection'].str.title()
    cc_df["Vendu"] = cc_df["Vendu"].astype(int)
    cc_df["Année"] = cc_df["Année"].astype(int)
    cc_df["Prix"] = cc_df["Prix"].astype(int)



    modele = st.text_input("Nom du modèle  ") # + str(cc_df['Modèle'].unique())
    fait_par =  st.text_input("Fait par  ") # + str(cc_df['Fait par'].unique())
    taille = st.text_input("Taille  ") #  + str(cc_df['Taille'].unique())
    collection = st.text_input('Collection  ') #  + str(cc_df['Collection'].unique())
    matiere = st.text_input('Matière 1  ') #  + str(cc_df['Matière'].unique())
    couleur = st.text_input('Couleur 1  ') # + str(cc_df['Couleur'].unique())
    matiere_2 = st.text_input('Matière 2  ') #  + str(cc_df['Matière 2'].unique())
    couleur_2 = st.text_input('Couleur 2  ') #  + str(cc_df['Couleur 2'].unique())
    prix = st.number_input('Prix  ' + str(cc_df['Prix']), min_value=0, max_value=10000, value=0, step=1)
    vendu = st.number_input('Vendu  ' + str(cc_df['Vendu']), min_value=0, max_value=10, value=0, step=1)
    annee = st.number_input('Année de production  ', min_value=2000, max_value=2040, value=int(strftime("%Y")), step=1)
    gamme = st.text_input('Gamme  ') #  + str(cc_df['Gamme'].unique())
    num_produit = st.number_input('Numero de produit  ',  min_value=0, max_value=10000, value=1, step=1)




    validation = st.button('Valider')
    if validation:

        new_row = {'Modèle': modele, 'Taille': taille, 'Fait par': fait_par, 
        'Collection': collection, 'Matière': matiere, 'Couleur': couleur, 
        'Matière 2': matiere_2, 'Couleur 2': couleur_2, 'Prix': int(prix), 'Vendu': int(vendu),
        'Année': int(annee), 'Gamme': gamme, 'Numéro produit': int(num_produit)}

        cc_df = cc_df.append(new_row, ignore_index=True)
        cc_df.to_csv('CC_mere_et_fille - Feuille 1.csv')

        st.subheader('done')

elif menu == 'Modifier/Vente Produit':
    st.header('Modification de Produits')
    cc_df = pd.read_csv(url)
    cc_df.drop(cc_df.columns[cc_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    cc_df['Matière'] = cc_df['Matière'].str.title()
    cc_df['Couleur'] = cc_df['Couleur'].str.title()
    cc_df['Matière 2'] = cc_df['Matière 2'].str.title()
    cc_df['Couleur 2'] = cc_df['Couleur 2'].str.title()
    cc_df['Modèle'] = cc_df['Modèle'].str.capitalize()
    cc_df['Taille'] = cc_df['Taille'].str.upper()
    cc_df['Fait par'] = cc_df['Fait par'].str.upper()
    cc_df['Gamme'] = cc_df['Gamme'].str.upper()
    cc_df['Collection'] = cc_df['Collection'].str.title()
    cc_df["Vendu"] = cc_df["Vendu"].astype(int)
    cc_df["Année"] = cc_df["Année"].astype(int)
    cc_df["Prix"] = cc_df["Prix"].astype(int)


    lookup = st.text_input('Terme à rechercher:')

    df2 = cc_df[cc_df.apply(lambda row: row.astype(str).str.contains(lookup, case=False).any(), axis=1)]
    st.dataframe(df2.style.apply(highlight_survived, axis=1), width=1280, height=640)

    ligne = st.sidebar.number_input('Numero de ligne du sac à modifier', min_value=0, max_value=10000, value=0, step=1)

    mod_selector = st.sidebar.selectbox('Action sur sac', ['Mettre dans inventaire', 'Sac vendu', 'Supprimer la ligne', 'Modifier produit'])

    if mod_selector == 'Modifier produit':
        mod_col = st.sidebar.selectbox('Attribut du produit à modifier', cc_df.columns.tolist())
        mod_eff = st.sidebar.text_input('Modification à effectuer ')


    validation_selector = st.sidebar.button('Valider')
    
    if validation_selector:
        if mod_selector == 'Sac vendu':
            cc_df.at[ligne,'Vendu'] = 1
            cc_df.to_csv(url)
            st.sidebar.subheader('Done')

        
        elif mod_selector == 'Mettre dans inventaire':
            cc_df.at[ligne,'Vendu'] = 0
            cc_df.to_csv(url)
            st.sidebar.subheader('Done')


        elif mod_selector == 'Supprimer la ligne':
            cc_df = cc_df.drop([ligne])
            cc_df.to_csv(url)
            st.sidebar.subheader('Done')


        elif mod_selector == 'Modifier produit':
            if mod_col in ['Année', 'Prix', 'Numéro produit']:
                cc_df.at[ligne, mod_col] = int(mod_eff)
                cc_df.to_csv(url)            
                st.sidebar.subheader('Done')
            else:
                cc_df.at[ligne, mod_col] = mod_eff
                cc_df.to_csv(url)            
                st.sidebar.subheader('Done')


elif menu == 'Analysis':
    st.header('Analyse des ventes')
    st.markdown('</br>', unsafe_allow_html=True)

    cc_df = pd.read_csv(url)
    cc_df.drop(cc_df.columns[cc_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    vendu_df = cc_df[cc_df['Vendu'] > 0]
    dispo_df = cc_df[cc_df['Vendu'] < 1]

    st.subheader('- Les sacs les plus vendus: ')
    expander = st.expander("Voir graphique")
    expander.bar_chart(vendu_df['Modèle'].value_counts(ascending=True))

    st.subheader('- Les sacs disponibles: ')
    expander = st.expander("Voir graphique")
    expander.bar_chart(dispo_df['Modèle'].value_counts(ascending=True))

    st.subheader('- Les couleurs qui plaisent le plus: ')
    expander = st.expander("Voir graphique")
    expander.bar_chart(vendu_df['Couleur'].value_counts(ascending=True))

    st.subheader('- Les matières principales qui plaisent le plus: ')
    expander = st.expander("Voir graphique")
    expander.bar_chart(vendu_df['Matière'].value_counts(ascending=True))

    st.subheader('- Les matières secondaires qui plaisent le plus: ')
    expander = st.expander("Voir graphique")
    expander.bar_chart(vendu_df['Matière 2'].value_counts(ascending=True))

    st.markdown('</br>', unsafe_allow_html=True)
    st.markdown('</br>', unsafe_allow_html=True)

    st.header("Montant de l'inventaire produit par année")
    st.markdown('</br>', unsafe_allow_html=True)

    st.subheader("- Montant total des sacs produits en 2017 s'élève à : " + str(cc_df[cc_df['Année'] == 2017]['Prix'].sum()) + ' CHF')
    st.subheader("- Montant total des sacs produits en 2018 s'élève à : " + str(cc_df[cc_df['Année'] == 2018]['Prix'].sum()) + ' CHF')
    st.subheader("- Montant total des sacs produits en 2019 s'élève à : " + str(cc_df[cc_df['Année'] == 2019]['Prix'].sum()) + ' CHF')
    st.subheader("- Montant total des sacs produits en 2020 s'élève à : " + str(cc_df[cc_df['Année'] == 2020]['Prix'].sum()) + ' CHF')
    st.subheader("- Montant total des sacs produits en 2021 s'élève à : " + str(cc_df[cc_df['Année'] == 2021]['Prix'].sum()) + ' CHF')
    st.subheader("- Montant total des sacs produits en 2022 s'élève à : " + str(cc_df[cc_df['Année'] == 2022]['Prix'].sum()) + ' CHF')
    st.subheader("- Montant total des sacs produits en 2023 s'élève à : " + str(cc_df[cc_df['Année'] == 2023]['Prix'].sum()) + ' CHF')

    st.markdown('</br>', unsafe_allow_html=True)
    st.markdown('</br>', unsafe_allow_html=True)


    st.header('Revenus totaux')
    st.markdown('</br>', unsafe_allow_html=True)

    st.subheader("- Montant de l'ensemble des sacs vendus depuis le debut: " + str(cc_df[cc_df['Vendu'] >= 1]['Prix'].sum()) + ' CHF')


elif menu == 'Coûts':
    st.header('Analyse des coûts')


elif menu == 'Recherche':
    st.header('Recherche de Produits')
    cc_df = pd.read_csv(url)
    cc_df.drop(cc_df.columns[cc_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

    search = st.sidebar.radio('Selection du type de recherche:', ['Simple', 'Avancé'])


    if search == 'Simple':
        st.header('Recherche simple')
        lookup = st.text_input('Terme à rechercher:')

        df2 = cc_df[cc_df.apply(lambda row: row.astype(str).str.contains(lookup, case=False).any(), axis=1)]
        st.dataframe(df2.style.apply(highlight_survived, axis=1), width=1280, height=640)

    if search == 'Avancé':
        col1, col2, col3 = st.columns(3)
        cc_df["Vendu"] = cc_df["Vendu"].astype(str)
        cc_df["Année"] = cc_df["Année"].astype(str)
        cc_df["Prix"] = cc_df["Prix"].astype(str)

        with col1:
            st.write("### Critère 1")
            crit1 = st.selectbox("Selection du 1er critère de recherche", cc_df.columns)
            lookup1 = st.text_input('1er Terme à rechercher:')

            cc_df = cc_df[cc_df[crit1].str.contains(lookup1, case=False, na=False)]

        with col2:
            st.write("### Critère 2")
            crit2 = st.selectbox("Selection du 2eme critère de recherches", cc_df.columns)
            lookup2 = st.text_input('2eme Terme à rechercher:')

            cc_df = cc_df[cc_df[crit2].str.contains(lookup2, case=False, na=False)]

        with col3:
            st.write("### Critère 3")
            crit3 = st.selectbox("Selection du 3eme critère de recherches", cc_df.columns)
            lookup3 = st.text_input('3eme Terme à rechercher:')

            cc_df = cc_df[cc_df[crit3].str.contains(lookup3, case=False, na=False)]        
        
        st.dataframe(cc_df.style.apply(highlight_survived, axis=1), width=1280, height=640)
