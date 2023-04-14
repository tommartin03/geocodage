#imports
import requests


def push(fichier):
    """Envoie une requete à la Ban et crée un fichier avec les valeurs de retour
    """    
    #le fichier csv à push
    try:
        csv_donnes = open(fichier)
    except:
        exit("Impossible d'ouvrir le fichier")
    #url API
    url = 'https://api-adresse.data.gouv.fr/kjnlknlnsearch/csv/dd'
    #paramètres pour la requete
    params = {
        'columns': ['ADRESSE'],
        'postcode': 'CODE_POSTAL',
        'citycode': 'NUM_INSEE'
    }   
    #execution de la requete avec les params du dessus et le fichier csv push
    test = requests.post(url, data=params, files={"data": csv_donnes}, timeout=5000)
    #fermer le fichier
    csv_donnes.close()
    #on verifie si on obtient un retour positif de la requete
    if test.status_code == 200:
        print(test.text)
    else:
        exit("Erreur API BAN : "+test.reason)

def main():
    """Main du script
    """    
    push("./Ass_Mat_SIG_.csv")

if __name__ == "__main__":
    main()






