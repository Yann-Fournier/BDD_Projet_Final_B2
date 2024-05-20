import sqlite3

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
    print("ok")


#  Fonction pour remplir la database -----------------------------------------------------------------------------------
# load_sql()
# load_data()


# Fermer le curseur et la connexion ------------------------------------------------------------------------------------
cur.close()
conn.close()
