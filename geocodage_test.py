#imports
import csv
import os 
import openpyxl
import requests


def convert(chemin_excel):
    """Convertis un fichier Excel en CSV

    Args:
        cheminExcel (_type_): fichier CSV à convertir
    """    
    #traitement excel
    excle_workbook = openpyxl.load_workbook(chemin_excel)
    active_workbook = excle_workbook.active
    
    #traitement csv
    #ouvre et crée un nouveau fichier avec l'encodage 'ISO-8859-1' pour l'API
    with open("Données_Ass_Mat.csv", "w", newline='', encoding='ISO-8859-1') as fichier_csv:
        #permets d'écrire des lignes dans le fichier CSV en utilisant une virgule (,) comme délimiteur de champ
        ecrire = csv.writer(fichier_csv, delimiter=',',quotechar ='"',quoting=csv.QUOTE_ALL)
        #la variable ligne est une ligne du fichier Excel qui a été convertie en une liste de cellules.
        for ligne in active_workbook.iter_rows():
             #filtre les colonnes à écrire 
            donnees_ligne = [str(cell.value) for i, cell in enumerate(ligne) if i in [0,7,8,9,10,11,12,13]] #index des colonnes à écrire
            #écrit chaque élément de cette liste de cellules pour chaque cellule dans la ligne.
            ecrire.writerow(donnees_ligne)

def push():
    """Envoie une requete à la Ban et crée un fichier avec les valeurs de retour
    """    
    #le fichier csv à push
    csv_donnes = open("./Données_Ass_Mat.csv", encoding='ISO-8859-1')
    #url API
    url = 'https://api-adresse.data.gouv.fr/search/csv/'
    #paramètres pour la requete
    params = {
        'columns': ['ADRESSE', 'ADRESSE2', 'ADRESSE3', 'LIEU_DISTRIBUTION', 'COMMUNE', 'NUM_INSEE'],
        'postcode': 'CODE_POSTAL',
        'citycode': 'NUM_INSEE', 
    }
    #execution de la requete avec les params du dessus et le fichier csv push
    test = requests.post(url, data=params, files={"data": csv_donnes}, timeout=5000)
    #on verifie si on obtient un retour positif de la requete
    if test.status_code == 200:
        #nouveau fichier avec les valeurs de retour de la Ban
        with open("Ban_Ass_Mat.csv", "wb") as file:
            #on écrit dans le fichier
            file.write(test.content)
    else:
        print("Erreur lors de la requête.")

def filtrer():
    """Filtre les colonnes en enlevant les colonnes de données sensibles et inutiles
    """    
    #la liste des colones souhaitées
    result_columns= ['result_id', 'CODE_INDI_ANO', 'result_score', 'latitude', 'longitude']
    #ouvre et crée un nouveau fichier final
    with open("Resultats_Ass_Mat.csv", "w", newline='', encoding='ISO-8859-1') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',',quoting=csv.QUOTE_ALL)
        #ouvre le fichier sans filtre
        with open("Ban_Ass_Mat.csv", newline='', encoding='ISO-8859-1') as donnees_csv:
            #lit le fichier 
            reader = csv.reader(donnees_csv, delimiter=',',quotechar ='"',quoting=csv.QUOTE_ALL)
            header = next(reader) # lire la première ligne (l'en-tête)
            # les indexe des colones resultats dans le fichier ban.csv
            indexes = [header.index(colonne) for colonne in result_columns if colonne in header]
            # écrire l'en-tête du fichier de sortie
            writer.writerow([header[i] for i in indexes])
            # écrire les lignes de données en gardant seulement les colonnes nécessaires
            for ligne in reader:
                writer.writerow([ligne[i] for i in indexes])

def supression_fichier():
    """Supprime les fichiers de transition
    """    
    fichier_convert = "./Données_Ass_Mat.csv"
    fichier_retour_ban = "./Ban_Ass_Mat.csv"
    #supprime les fichers
    os.remove(fichier_convert)
    os.remove(fichier_retour_ban)

def main():
    """Main du script
    """    
    #convertion du fichier Excel en CSV
    convert("./Ass_Mat_SIG.xlsx")
    #execution de la requete et création du d'un fichier de résultat
    push()
    #filtrer les colonnes
    filtrer()
    #supprimer les fichiers de transition
    #supression_fichier()

if __name__ == "__main__":
    main()






