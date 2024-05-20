import sqlite3

# Se connecter à la base de données (ou créer le fichier .db s'il n'existe pas)
conn = sqlite3.connect('Database_Biblio.db')

# Créer un curseur
cur = conn.cursor()


def load_sql():
    # Lire le contenu du fichier .sql
    with open("script.sql", 'r') as fichier:
        script_sql = fichier.read()

    try:
        # Exécuter le script SQL
        cur.executescript(script_sql)

        # Valider les changements
        conn.commit()

        print("Script SQL exécuté avec succès")

    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")


def load_data():
    print("ok")


# load_sql()

# Fermer le curseur et la connexion
cur.close()
conn.close()
