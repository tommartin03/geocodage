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
    # traitement excel
    excel_workbook = openpyxl.load_workbook(chemin_excel)
    active_workbook = excel_workbook.active

    # colonnes à garder
    columns = ['ADRESSE', 'ADRESSE2', 'ADRESSE3', 'LIEU_DISTRIBUTION', 'COMMUNE', 'NUM_INSEE', 'CODE_POSTAL', 'NUM_INSEE']

    # traitement csv
    # ouvre et crée un nouveau fichier avec l'encodage 'ISO-8859-1' pour l'API
    with open("Données.csv", "w", newline='', encoding='ISO-8859-1') as fichier_csv:
        # permets d'écrire des lignes dans le fichier CSV en utilisant une virgule (,) comme délimiteur de champ
        ecrire = csv.writer(fichier_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        # la variable ligne est une ligne du fichier Excel qui a été convertie en une liste de cellules.
        for ligne in active_workbook.iter_rows():
            #affiche les colonnes voulues
        
            
            
        


            
def push():
    """Envoie une requete à la Ban et crée un fichier avec les valeurs de retour
    """    
    #le fichier csv à push
    csv_donnes = open("./Données.csv", encoding='ISO-8859-1')
    #url API
    url = 'https://api-adresse.data.gouv.fr/search/csv/'
    #paramètres pour la requete
    params = {
        'columns': ['ADRESSE', 'ADRESSE2', 'ADRESSE3', 'LIEU_DISTRIBUTION', 'COMMUNE', 'NUM_INSEE'],
        'postcode': 'CODE_POSTAL',
        'citycode': 'NUM_INSEE', 
        'result_columns': ['result_id', 'CODE_INDI_ANO', 'result_score', 'latitude', 'longitude']
    }
    #execution de la requete avec les params du dessus et le fichier csv push
    test = requests.post(url, data=params, files={"data": csv_donnes}, timeout=5000)
    #on verifie si on obtient un retour positif de la requete
    if test.status_code == 200:
        #nouveau fichier avec les valeurs de retour de la Ban
        with open("Ban.csv", "wb") as file:
            #on écrit dans le fichier
            file.write(test.content)
    else:
        print("Erreur lors de la requête.")


def supression_fichier():
    """Supprime les fichiers de transition
    """    
    fichier_convert = "./Données.csv"
    #supprime les fichers
    os.remove(fichier_convert)

def main():
    """Main du script
    """    
    #convertion du fichier Excel en CSV
    convert("./Ass_Mat_SIG.xlsx")
    #execution de la requete et création du d'un fichier de résultat
    push()
    #supprimer les fichiers de transition


if __name__ == "__main__":
    main()






