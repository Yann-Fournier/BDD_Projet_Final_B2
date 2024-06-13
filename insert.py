import pandas as pd
import sqlite3
lines = []

conn = sqlite3.connect('Database_Biblio.db')  # Se connecter à la base de données
cur = conn.cursor()  # Créer un curseur

# Utilisateurs
query_user = "SELECT * FROM Users;"
cur.execute(query_user)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Users (Id, Email, Mdp, Photo, Nom, Is_Admin) VALUES (" + str(results[i][0]) + ", '" + str(results[i][1]) + "', '" + str(results[i][2]) + "', '" + str(results[i][3]) + "', '" + str(results[i][4]) + "', " + str(results[i][5]) + ");\n")


# Auth
query_user = "SELECT * FROM Auth;"
cur.execute(query_user)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Auth (Id, Token) VALUES (" + str(results[i][0]) + ", '" + str(results[i][1]) + "');\n")

# Categories
query_user = "SELECT * FROM Categories;"
cur.execute(query_user)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Categories (Id, Nom) VALUES (" + str(results[i][0]) + ", '" + str(results[i][1]) + "');\n")

# Auteurs
query_auteur = "SELECT * FROM Auteurs;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Auteurs (Id, Nom, Description, Photo) VALUES (" + str(results[i][0]) + ", '" + str(results[i][1]) + "', '" + str(results[i][2]) + "', '" + str(results[i][3]) +"');\n")

# Livres
query_auteur = "SELECT * FROM Livres;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Livres (Id, Id_Auteur, Id_Categorie, Nom, Description, Photo, ISBN, Editeur, Prix) VALUES (" + str(results[i][0]) + ", " + str(results[i][1]) + ", " + str(results[i][2]) + ", '" + str(results[i][3]) + "', '" + str(results[i][4]) +"', '" + str(results[i][5]) +"', '" + str(results[i][6]) +"', '" + str(results[i][7]) +"', " + str(results[i][8]) +");\n")

# Collections
query_auteur = "SELECT * FROM Collections;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Collections (Id, Id_User, Nom, Is_Private) VALUES (" + str(results[i][0]) + ", " + str(results[i][1]) + ", '" + str(results[i][2]) + "', " + str(results[i][3]) +");\n")

# Collec
query_auteur = "SELECT * FROM Collec;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Collec (Id_Livre, Id_Collection) VALUES (" + str(results[i][0]) + ", " + str(results[i][1]) + ");\n")
    
# Commentaires
query_auteur = "SELECT * FROM Commentaires;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Commentaires (Id, Id_User, Id_Livre, Com) VALUES (" + str(results[i][0]) + ", " + str(results[i][1]) + ", " + str(results[i][2]) + ", '" + str(results[i][3]) + "');\n")

# Users_Suivi
query_auteur = "SELECT * FROM Users_Suivi;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Users_Suivi (Id_User, Id_User_Suivi) VALUES (" + str(results[i][0]) + ", " + str(results[i][1]) + ");\n")

# Auteurs_Suivi
query_auteur = "SELECT * FROM Auteurs_Suivi;"
cur.execute(query_auteur)
results = cur.fetchall()  # renvoie un tableau de tableau
for i in range(len(results)):
    lines.append("INSERT INTO Auteurs_Suivi (Id_User, Id_Auteur) VALUES (" + str(results[i][0]) + ", " + str(results[i][1]) + ");\n")
     
# Ouvrir (ou créer) un fichier en mode écriture
with open('insert.sql', 'w', encoding='utf-8') as file:
    file.writelines(lines)
