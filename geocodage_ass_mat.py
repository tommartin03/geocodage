#imports
import requests
import csv

def push(fichier):
    """Envoie une requete à la Ban et crée un fichier avec les valeurs de retour
    """    
    #le fichier csv à push
    csv_donnes = open(fichier)
    #url API
    url = 'https://api-adresse.data.gouv.fr/search/csv/'
    #paramètres pour la requete
    params = {
        'columns': ['ADRESSE'],
        'postcode': 'CODE_POSTAL',
        'citycode': 'NUM_INSEE'
    }   
    #execution de la requete avec les params du dessus et le fichier csv push
    test = requests.post(url, data=params, files={"data": csv_donnes}, timeout=5000)
    #on verifie si on obtient un retour positif de la requete
    if test.status_code == 200:
        print(test.text)

    else:
        print("Erreur lors de la requête.")

def main():
    """Main du script
    """    
    push("./Ass_Mat_SIG_.csv")

if __name__ == "__main__":
    main()






