from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import json
import numpy as np


# Créez une instance de navigateur Chrome
driver = webdriver.Chrome()

fichier_json_url_Categories = 'CSV/Categories.json'
fichier_json_Pages = 'CSV/Pages.json'
# fichier_json_url_Categories = 'Scrapping/CSV/Categories.json'
# fichier_json_Pages = 'Scrapping/CSV/Pages.json'
with open(fichier_json_url_Categories, 'r') as fichier_Categories:
    contenuCategories = fichier_Categories.read()  # Le code bug si je ne transforme pas le json en str en premier
    urlCategories = json.loads(contenuCategories)
with open(fichier_json_Pages, 'r') as fichier_Pages:
    contenuPages = fichier_Pages.read()  # Le code bug si je ne transforme pas le json en str en premier
    indicesPagesPasPrises = json.loads(contenuPages)  # Les indices des pages qui n'ont pas été scrapper à cause de PB

# Configuration --------------------------------------------------------------------------------------------------------
driver.get('https://www.amazon.fr')
time.sleep(20)  # Au cas où il y aurait un kapcha à faire

#  Boucle des catégories --------------------------------------------------------------------
for key, value in urlCategories.items():

    print(key)
    indicesPagesPasPrises2 = []
    #  Boucle des pages ------------------------------------------------------------------------------------------------
    # for i in range(1, 76):
    for i in range(1, 6):
        # Initialisation tableaux à chaque nouvelle page ---------------------------------------------------------------
        nom = []
        description = []
        photo = []
        isbn = []
        editeur = []
        prix = []
        auteur = []
        categorie = []

        # Initialisation tableau auteur --------------------------------------------------------------------------------
        nomAuteur = []
        photoAuteur = []
        descAuteur = []

        try:
            # On va sur chacune des pages
            driver.get(value.format(i, i))

            #  Page simple ---------------------------------------------------------------------------------------------
            # Je divise la recupération des liens en deux requêtes, car sinon les xpath est trop grand et l'IDE n'est pas content
            divPrincipal = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]')
            divs = divPrincipal.find_elements(By.CLASS_NAME, 's-widget-spacing-small')
            linksInPage = []  # tableau des liens des livres de la page actuelle

            for div in divs:  # recuperation des liens des livres de la page actuelle
                try:
                    elm = div.find_element(By.XPATH, './div/div/span/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div[1]/a').text  # chemin relatif
                except:
                    elm = ""
                if elm == "":
                    try:
                        elm = div.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/span/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div[1]/a').text  # chemin complet
                    except:
                        elm = ""
                if elm == "":
                    try:
                        elm = div.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[9]/div/div/span/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div[1]/a').text  # chemin complet
                    except:
                        elm = ""

                if elm == "Poche" or elm == "Relié" or elm == "Broché" or elm == "Carte":
                    try:
                        linksInPage.append(div.find_element(By.XPATH, './div/div/span/div/div/div/div[1]/div/div[2]/div/span/a').get_attribute('href'))  # chemin relatif
                    except:
                        linksInPage.append(div.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/span/div/div/div/div[1]/div/div[2]/div/span/a').get_attribute('href'))  # chemin complet
            print(i, ":", len(linksInPage), "--------------------------------------------------------------------------------------")

            cpt = 0  # tkt compteur pour l'affichage
            for link in linksInPage:
                cpt += 1  # tkt
                # On va sur chacune des pages des livres pour récupérer les infos qui nous interesse.
                driver.get(link)

                # Nom --------------------------------------------------------------------------------------------------
                try:
                    name = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[8]/div[2]/div/h1/span[1]').text
                except:
                    name = ""
                if name == "":
                    try:
                        name = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[7]/div[2]/div/h1/span[1]').text
                    except:
                        name = ""
                name = name.replace("'", "&#39")
                nom.append(name)

                # Description ------------------------------------------------------------------------------------------
                try:
                    desc = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[1]/div[8]/div[28]/div[1]/div/div[1]').text
                except:
                    desc = ""
                if desc == "":
                    try:
                        desc = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[1]/div[7]/div[28]/div/div[1]').text
                    except:
                        desc = ""
                if desc == "":
                    try:
                        desc = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[1]/div[8]/div[27]/div/div[1]').text
                    except:
                        desc = ""
                if desc == "":
                    try:
                        desc = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[1]/div[7]/div[27]/div/div[1]').text
                    except:
                        desc = ""
                desc = desc.replace("'", "&#39")
                description.append(desc)

                #  Photo -----------------------------------------------------------------------------------------------
                try:
                    pic = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[1]/div[7]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/span/span/div/img').get_attribute('src')
                except:
                    pic = ""
                if pic == "":
                    try:
                        pic = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[1]/div[6]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/span/span/div/img').get_attribute('src')
                    except:
                        pic = ""
                photo.append(pic)

                # Detail -----------------------------------------------------------------------------------------------
                Isbn = ""
                edit = ""
                try:
                    details = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[4]/div[26]/div/div[1]/ul/li')
                    for det in details:
                        truc = det.find_element(By.XPATH, './span/span[1]').text
                        if truc.__contains__("ISBN-13"):
                            Isbn = det.find_element(By.XPATH, './span/span[2]').text
                        elif truc.__contains__("Éditeur"):
                            edit = det.find_element(By.XPATH, './span/span[2]').text
                except:
                    pass
                Isbn = Isbn.replace("'", "&#39")
                edit = edit.replace("'", "&#39")
                isbn.append(Isbn)
                editeur.append(edit)

                # Auteur -----------------------------------------------------------------------------------------------
                try:
                    aut = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[8]/div[3]/div/span[1]/a').text
                except:
                    aut = ""
                if aut == "":
                    try:
                        aut = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[7]/div[3]/div/span/a').text
                    except:
                        aut = ""
                aut = aut.replace("'", "&#39")
                auteur.append(aut)
                nomAuteur.append(aut)

                # Description Auteur -----------------------------------------------------------------------------------
                try:
                    descAut = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[25]/div[2]/div').text
                except:
                    descAut = ""
                if descAut == "":
                    try:
                        descAut = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[25]/div[2]/div[2]/p/span').text
                    except:
                        descAut = ""
                descAut = descAut.replace("'", "&#39")
                descAuteur.append(descAut)

                # Photo Auteur -----------------------------------------------------------------------------------------
                try:
                    picAut = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[28]/div/div/div[2]/div/div/div/div[1]/div[1]/div/img').get_attribute('src')
                except:
                    picAut = ""
                photoAuteur.append(picAut)

                #  Prix ------------------------------------------------------------------------------------------------
                price = 0.0
                try:
                    priceInt = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[4]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div/form/div/div/div[2]/div[1]/div[1]/span[2]/span[2]/span[1]').text
                    priceFloat = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[4]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div/form/div/div/div[2]/div[1]/div[1]/span[2]/span[2]/span[2]').text
                    price = priceInt + "." + priceFloat
                    price = float(price)
                except:
                    price = 0.0
                if price == 0.0:
                    try:
                        priceInt = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[4]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]/span[2]/span[1]').text
                        priceFloat = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[4]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]/span[2]/span[2]').text
                        price = priceInt + "." + priceFloat
                        price = float(price)
                    except:
                        price = 0.0
                if price == 0.0:
                    try:
                        priceInt = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[4]/div/div[1]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]/span[2]/span[1]').text
                        priceFloat = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[4]/div/div[1]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]/span[2]/span[2]').text
                        price = priceInt + "." + priceFloat
                        price = float(price)
                    except:
                        price = 0.0
                if price == 0.0:
                    try:
                        priceSTR = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[2]/div/div/div/div[2]/span/span/a/span[2]/span')
                        priceSTR = priceSTR[:-2]
                        priceSTR = priceSTR.replace(',', '.')
                        price = float(priceSTR)
                    except:
                        price = 0.0
                if price == 0.0:
                    try:
                        priceSTR = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/div[5]/div[4]/div[2]/div/div/div[2]/div[2]/span/span/a/span[2]/span')
                        priceSTR = priceSTR[:-2]
                        priceSTR = priceSTR.replace(',', '.')
                        price = float(priceSTR)
                    except:
                        price = 0.0
                if price == 0.0:
                    nombre_aleatoire = np.random.uniform(5.0, 20.0)
                    price = round(nombre_aleatoire, 2)
                prix.append(price)

                # Catégorie --------------------------------------------------------------------------------------------
                categorie.append(key)

                print(cpt, "/", len(linksInPage))

            #  Ajout des données dans la CSV ---------------------------------------------------------------------------
            if len(nom) == len(description) == len(photo) == len(isbn) == len(editeur) == len(prix) == len(auteur) == len(categorie):
                time.sleep(1)
                dfLivres = pd.DataFrame(
                    {"Nom": nom, "Prix": prix, "Description": description, "Isbn": isbn, "Photo": photo,
                     "Editeur": editeur, "Auteur": auteur, "Categorie": categorie})
                fileNameLivres = 'CSV/Livres' + key + '.csv'
                # fileNameLivres = "Scrapping/CSV/Livres" + str(key) + ".csv"
                if i == 1:
                    dfLivres.to_csv(fileNameLivres, index=False, encoding='utf-8')
                else:
                    dfLivres.to_csv(fileNameLivres, mode='a', index=False, header=False, encoding='utf-8')
            else:
                print("Len livres pas OK")
                print("Nom", len(nom))
                print("Description", len(description))
                print("Photo", len(photo))
                print("ISBN", len(isbn))
                print("Editeur", len(editeur))
                print("Prix", len(prix))
                print("Auteur", len(auteur))
                print("Categorie", len(categorie))
                indicesPagesPasPrises2.append(i)

            if len(nomAuteur) == len(descAuteur) == len(photoAuteur):
                time.sleep(1)
                dfAuteur = pd.DataFrame({"Nom": nomAuteur, "Description": descAuteur, "Photo": photoAuteur})
                fileNameAuteur = 'CSV/Auteurs' + key + '.csv'
                # fileNameAuteur = "Scrapping/CSV/Auteurs" + str(key) + ".csv"
                if i == 1:
                    dfAuteur.to_csv(fileNameAuteur, index=False, encoding='utf-8')
                else:
                    dfAuteur.to_csv(fileNameAuteur, mode='a', index=False, header=False, encoding='utf-8')
            else:
                print("Len auteurs pas OK")
                print("Nom auteur", len(nomAuteur))
                print("Description auteur", len(descAuteur))
                print("Photo auteur", len(photoAuteur))
        except:
            print("PB recupération des liens des livres")

            indicesPagesPasPrises2.append(i)

        #  Sauvegarde des pages qui n'ont pas été scrapper par catégories-----------------------------------------------
        indicesPagesPasPrises[key] = indicesPagesPasPrises2
    with open(fichier_json_Pages, 'w') as fichier:
        json.dump(indicesPagesPasPrises, fichier, indent=4)

# Fermer le navigateur
driver.quit()
print("Le scrap est fini !!!!!!!!!!!!!!!!!")
