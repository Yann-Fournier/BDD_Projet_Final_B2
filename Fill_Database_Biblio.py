from faker import Faker
import pandas as pd
import sqlite3
import hashlib
import json

conn = sqlite3.connect('Database_Biblio.db')  # Se connecter à la base de données
cur = conn.cursor()  # Créer un curseur


def load_sql():
    with open("script.sql", 'r') as fichier:
        script_sql = fichier.read()

    try:
        cur.executescript(script_sql)  # execution du script
        conn.commit()  # enregistrement des changements
        print("Script SQL exécuté avec succès")

    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")


def load_data():
    # 5 Users (3 admins et 2 normaux)
    insert_user(0, "admin@biblio.com", hash_passwd("admin1234"), "", "Admin")
    insert_user(1, "yann@biblio.com", hash_passwd("yann1234"), "", "Yann Fournier")
    insert_user(2, "adriana@biblio.com", hash_passwd("adriana1234"), "", "Adriana Pullig")

    insert_user(10, "adriana@ynov.com", hash_passwd("yann"), "", "Yann")
    insert_user(11, "adriana@ynov.com", hash_passwd("adriana"), "", "Adriana")

    # Toutes les catégories
    fichier_json_url_categories = 'Scrapping/CSV/Categories.json'
    with open(fichier_json_url_categories, 'r') as fichier_categories:
        contenu_categories = fichier_categories.read()  # Le code bug si je ne transforme pas le json en str en premier
        url_categories = json.loads(contenu_categories)
        keys = url_categories.keys()

    cpt = 0
    for key in keys:
        insert_categorie(cpt, 0, key, False)
        cpt += 1

    # Tous les Auteurs
    auteurs = pd.read_csv("Scrapping/CSV/Save/Auteurs_combined.csv")
    for i in range(len(auteurs)):
        insert_auteur(i, auteurs["Nom"][i], auteurs["Description"][i], auteurs["Photo"][i])

    # Tous les Livres
    livres = pd.read_csv("Scrapping/CSV/Save/Shōnen_combined.csv")
    cur.execute("SELECT Id FROM Categories WHERE Nom = 'Shōnen';")  # Id = 55
    results_id_category = cur.fetchall()  # renvoie un tableau de tuple
    for i in range(len(livres)):
        query = "SELECT Id FROM Auteurs WHERE Nom = '" + str(livres["Auteur"][i]) + "';"
        cur.execute(query)
        results_id_auteur = cur.fetchall()  # renvoie un tableau de tuple
        insert_livre(i, results_id_auteur[0][0], results_id_category[0][0], str(livres["Nom"][i]),
                     str(livres["Description"][i]), str(livres["Photo"][i]), str(livres["Isbn"][i]),
                     str(livres["Editeur"][i]), float(livres["Prix"][i]))

    # Faker des Com
    insert_com(0,10, "Ce livre est génial. :)")
    insert_com(1, 11, "J'adore ce livre. Il a vraiment changer ma vie !!!!!!")

    # Commentaires
    for i in range(len(livres)):
        insert_commentaires(0, i)
        insert_commentaires(1, i)

    # Ajout de certains Auteurs suivis
    insert_users_suivi(10, 11)
    insert_users_suivi(11, 10)

    # Ajout de certains Users suivis
    insert_auteurs_suivi(10, 0)
    insert_auteurs_suivi(10, 1)
    insert_auteurs_suivi(10, 2)
    insert_auteurs_suivi(10, 3)
    insert_auteurs_suivi(10, 4)
    insert_auteurs_suivi(11, 5)
    insert_auteurs_suivi(11, 6)
    insert_auteurs_suivi(11, 7)
    insert_auteurs_suivi(11, 8)
    insert_auteurs_suivi(11, 9)

    print("Load des données bien exécuter")


def hash_passwd(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def insert_user(Id, Email, Mdp, Photo, Nom, data=None):
    if data is None:
        data = [
            Id, Email, Mdp, Photo, Nom
        ]
    conn.execute(
        "INSERT INTO Users (Id, Email, Mdp, Photo, Nom) VALUES(?, ?, ?, ?, ?)", data)
    conn.commit()


def insert_auteur(Id, Nom, Description, Photo, data=None):
    if data is None:
        data = [
            Id, Nom, Description, Photo
        ]
    conn.execute(
        "INSERT INTO Auteurs (Id, Nom, Description, Photo) VALUES(?, ?, ?, ?)", data)
    conn.commit()


def insert_categorie(Id, Id_Auteur, Nom, Is_Private, data=None):
    if data is None:
        data = [
            Id, Id_Auteur, Nom, Is_Private
        ]
    conn.execute(
        "INSERT INTO Categories (Id, Id_Auteur, Nom, Is_Private) VALUES(?, ?, ?, ?)", data)
    conn.commit()


def insert_livre(Id, Id_Auteur, Id_Categorie, Nom, Description, Photo, ISBN, Editeur, Prix, data=None):
    if data is None:
        data = [
            Id, Id_Auteur, Id_Categorie, Nom, Description, Photo, ISBN, Editeur, Prix
        ]
    conn.execute(
        "INSERT INTO Livres (Id, Id_Auteur, Id_Categorie, Nom, Description, Photo, ISBN, Editeur, Prix) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()


def insert_com(Id, Id_User, Com, data=None):
    if data is None:
        data = [
            Id, Id_User, Com
        ]
    conn.execute(
        "INSERT INTO Com (Id, Id_User, Com) VALUES(?, ?, ?)", data)
    conn.commit()


def insert_commentaires(Id_Com, Id_Livre, data=None):
    if data is None:
        data = [
            Id_Com, Id_Livre
        ]
    conn.execute(
        "INSERT INTO Commentaires (Id_Com, Id_Livre) VALUES(?, ?)", data)
    conn.commit()

def insert_users_suivi(Id_User, Id_User_Suivi, data=None):
    if data is None:
        data = [
            Id_User, Id_User_Suivi
        ]
    conn.execute(
        "INSERT INTO Users_Suivi (Id_User, Id_User_Suivi) VALUES(?, ?)", data)
    conn.commit()


def insert_auteurs_suivi(Id_User, Id_Auteur, data=None):
    if data is None:
        data = [
            Id_User, Id_Auteur
        ]
    conn.execute(
        "INSERT INTO Auteurs_Suivi (Id_User, Id_Auteur) VALUES(?, ?)", data)
    conn.commit()


#  Fonction pour remplir la database -----------------------------------------------------------------------------------
load_sql()
load_data()


# Fermer le curseur et la connexion ------------------------------------------------------------------------------------
cur.close()
conn.close()
