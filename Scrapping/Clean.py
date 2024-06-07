import pandas as pd
import glob


def concat_livre_csv():
    fichiers_csv_livres = glob.glob('CSV/Livres*.csv')
    dataframes_livres = [pd.read_csv(fichier_livres) for fichier_livres in fichiers_csv_livres]
    dataframe_combine_livres = pd.concat(dataframes_livres, ignore_index=True)

    # On itère à travers le dataframe pour remplacer les apostrophes pour éviter les pb dans les requêtes sql
    # for i in range(len(dataframe_combine_livres)):
    #     if str(dataframe_combine_livres["Nom"][i]) != "nan":
    #         dataframe_combine_livres["Nom"][i].replace("'", " ")
    #     if str(dataframe_combine_livres["Description"][i]) != "nan":
    #         dataframe_combine_livres["Description"][i].replace("'", " ")
    #     if str(dataframe_combine_livres["Editeur"][i]) != "nan":
    #         dataframe_combine_livres["Editeur"][i].replace("'", " ")
    #     if str(dataframe_combine_livres["Auteur"][i]) != "nan":
    #         dataframe_combine_livres["Auteur"][i].replace("'", " ")

    # On supprime les lignes ou le nom est vide
    dataframe_combine_livres = dataframe_combine_livres.dropna(subset=['Nom'])
    # On supprime les lignes ou l'auteur est vide
    dataframe_combine_livres = dataframe_combine_livres.dropna(subset=['Auteur'])
    # On supprime les lignes ou les noms sont en double
    dataframe_combine_livres = dataframe_combine_livres.drop_duplicates(subset=['Nom'])
    dataframe_combine_livres.to_csv('CSV/Combined_Books.csv', index=False, encoding='utf-8')


def concat_auteur_csv():
    fichiers_csv_auteurs = glob.glob('CSV/Auteurs*.csv')
    dataframes_auteurs = [pd.read_csv(fichier_auteurs) for fichier_auteurs in fichiers_csv_auteurs]
    dataframe_combine_auteurs = pd.concat(dataframes_auteurs, ignore_index=True)

    # On itère à travers le dataframe pour remplacer les apostrophes pour éviter les pb dans les requêtes sql
    # for i in range(len(dataframe_combine_auteurs)):
    #     if str(dataframe_combine_auteurs["Nom"][i]) != "nan":
    #         dataframe_combine_auteurs["Nom"][i].replace("'", " ")
    #     if str(dataframe_combine_auteurs["Description"][i]) != "nan":
    #         dataframe_combine_auteurs["Description"][i].replace("'", " ")

    # On supprime les lignes ou le nom est vide
    dataframe_combine_auteurs = dataframe_combine_auteurs.dropna(subset=['Nom'])
    # On supprime les lignes ou les noms sont en double
    dataframe_combine_auteurs = dataframe_combine_auteurs.drop_duplicates(subset=['Nom'])
    dataframe_combine_auteurs.to_csv('CSV/Combined_Authors.csv', index=False, encoding='utf-8')


concat_auteur_csv()
concat_livre_csv()
