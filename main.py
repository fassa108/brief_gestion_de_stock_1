import mysql.connector

connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Binetougueye@2",
    database="gestion_stock"
)

if connexion :
    print('connexion a la base reussie')












def ajout_categorie() :
    print('~'*8,"Ajout de categorie",'~'*8)
    while True :
        nom = input("Veuillez entrer le libelle de la categorie : ")
        if nom.isdigit() : 
            print("Attention le nom ne doit pas etre des chiffres!!!")
        else : 
            with connexion.cursor() as curseur :
                requete = """INSERT INTO categories (libelle) VALUES (%s)"""
                curseur.execute(requete,(nom,))
                connexion.commit()
                print(f"Categorie {nom} ajoutee avec succes!")
                break
    

def modification_categorie() :
    liste_categorie = affichage_categorie()
    choix = input("Veuillez saisir l'id de la categorie que vous voulez modifier : ")
    choix = int(choix)
    for categorie in liste_categorie :
        if categorie[0] == choix :
            nouveau_nom_categorie = input("Veuillez sasir le nom de la nouvelle categorie : ")
            with connexion.cursor() as curseur :
                query = """UPDATE  categories SET libelle = %s WHERE id = %s"""
                curseur.execute(query,(nouveau_nom_categorie,choix))
                connexion.commit()
                print("La categorie a ete modifiee avec succes!")

def affichage_categorie():
    print('Liste des categories : ')
    with connexion.cursor() as curseur : 
        requete = """SELECT * FROM categories"""
        curseur.execute(requete)
        liste_categorie = curseur.fetchall()
        if len(liste_categorie) != 0 :
            for categorie in liste_categorie : 
                print(f"ID : {categorie[0]} | Nom : {categorie[1]}")
        else : 
            print("Cette categorie n'existe pas")
    return liste_categorie

def supprime_categorie() :
    liste_categorie = affichage_categorie()
    while True :
        id = input("Veuillez saisir l' id de la categorie que vous voulez supprimer : ")
        if id.isdigit() :
            id = int(id)
            for categorie in liste_categorie :
                if categorie[0] == id : 
                    with connexion.cursor() as curseur :
                        requete = """DELETE FROM categories WHERE id = %s"""
                        curseur.execute(requete,(id,))
                        connexion.commit()
                        print("La suppression a ete effectuer avec succes!")
                        break

                else : 
                    print("Cette categorie n'existe pas")

def ajout_produit() :
    print('~'*8,"Ajout d'un produit",'~'*8)
    while True :
        libelle = input("Veuillez saisir le libelle du produit : ")
        prix = int(input("Veuillez sisir le prix du produit : "))
        quantite = int(input("Veuillez saisir la quantite du produit : "))
        liste_categorie = affichage_categorie()
        id_cat = int(input("Veuillez saisir l'id de la categorie correspondante : "))

        with connexion.cursor() as curseur :
            requete = """INSERT INTO produits (nom,prix,quantite,id_categorie) VALUES (%s, %s, %s, %s)"""
            curseur.execute(requete,(libelle,prix,quantite,id_cat))
            connexion.commit()
            print("Le produit a ete ajoute avec succes!")
            break


def afficher_produit() :
    with connexion.cursor() as curseur :
        requete = """SELECT p.*, c.libelle FROM produits p JOIN categories c ON p.id_categorie = c.id """
        curseur.execute(requete)
        liste_produit = curseur.fetchall()
        if len(liste_produit) != 0 :
            for produit in liste_produit :
                print(f"ID : {produit[0]} | libelle : {produit[1]} | prix : {produit[2]} | quantite : {produit[3]} | categorie : {produit[5]}")
        else : 
            print("Aucun produit pour le moment")
        print('~'*75,'\n')
    return liste_produit

def modifier_qte_produit():
    liste_produit = afficher_produit()
    id_produit_saisi = int(input("Veuilles choisir l'id du produit dont vous voulez modifier la quantite : "))
    for produit in liste_produit :
        if id_produit_saisi == produit[0] :
            new_quantite = float(input("Veuillez saisir la nouvelle quantite : "))
            
            with connexion.cursor() as curseur :
                requete = """UPDATE produits SET quantite = %s """
                curseur.execute(requete,(new_quantite,))
                print("La quantite a ete modifiee avec succees!")
        else : 
            print("Le produit n'existe pas")
    

def supprimer_produit() :
    liste_produit = afficher_produit()

    id_produit = int(input("Veuillez saisir l'id du produit que vous voulez supprimer : "))
    
    for produit in liste_produit :
        if id_produit == produit[0] :
            with connexion.cursor() as curseur :
                requete = """DELETE FROM produits WHERE id = %s"""
                curseur.execute(requete,(id_produit,))
                connexion.commit()
                print("Le produit a ete supprime avec succes!")
        else : 
            print("Le produit n'existe pas")

def rechercher_produit() :
    mot_cle = input('Veuillez saisir le libelle du produit a rechercher : ')
    with connexion.cursor() as curseur :
        mot_cle = f"%{mot_cle}%"
        requete = """SELECT p.*,c.libelle FROM produits p JOIN categories c ON p.id_categorie = c.id WHERE  nom LIKE %s"""
        curseur.execute(requete,(mot_cle,))
        resultat = curseur.fetchall()
        if len(resultat) != 0:
            for produit in resultat :
                print(f"ID : {produit[0]} | libelle : {produit[1]} | prix : {produit[2]} | quantite : {produit[3]} | categorie : {produit[5]}")
        else : 
            print("Aucun produit contenant ce mot cle")

def afficher_p_plus_cher() :
    requete1 = """SELECT p.*, c.libelle FROM produits p JOIN categories c ON p.id_categorie = c.id ORDER BY prix DESC LIMIT 1"""
 
    with connexion.cursor() as curseur1 :
        curseur1.execute(requete1)
        produit_cher = curseur1.fetchone()

        print('~'*8,"Le produit le plus cher",'~'*8)
        print(f"ID : {produit_cher[0]} | libelle : {produit_cher[1]} | prix : {produit_cher[2]} | quantite : {produit_cher[3]} | categorie : {produit_cher[5]}")
        print('~'*70)

def afficher_total_financier() :
    requete2 = """SELECT SUM(quantite*prix) FROM produits"""

    with connexion.cursor() as curseur2 :
        curseur2.execute(requete2)
        montant = curseur2.fetchone()
        print(f"La valeur totale financiere : {montant}FCFA")
        print('~'*70)


def afficher_nb_produit_by_cat() :

    requete3 = """SELECT COUNT(p.id), c.libelle FROM produits p JOIN categories c ON p.id_categorie = c.id GROUP BY c.libelle"""
    
    with connexion.cursor() as curseur :
        curseur.execute(requete3)
        nb_produit_by_cat = curseur.fetchall()

        print('~'*8," Le nombre de produit par categorie ",'~'*8)
        for element in nb_produit_by_cat :
            print(f"categorie : {element[1]} : {element[0]} produit.s ")
            print('~'*70)



def dashboard() :
    print('~'*70)
    print(" TABLEAU DE BORD ")
    print('~'*70)

    afficher_p_plus_cher()
    afficher_total_financier()
    afficher_nb_produit_by_cat()



def effectuer_vente() :
    with connexion.cursor() as curseur :
        requete = """SELECT p.*, c.libelle FROM produits p JOIN categories c ON p.id_categorie = c.id """
        curseur.execute(requete)
        liste_produit = curseur.fetchall()
        if len(liste_produit) != 0 :
            for produit in liste_produit :
                print(f"ID : {produit[0]} | libelle : {produit[1]} | prix : {produit[2]} | quantite : {produit[3]} | categorie : {produit[5]}")

            id_produit = int(input("Veuillez saisir l'id du produit que vous voulez acheter : "))

            for produit in liste_produit :
                if id_produit == produit[0] :
                    quantite = float(input("Veuillez sasir la quantite souhaite : "))
                    if quantite > produit[3] :
                        produit("Le stock est insuffisant pour cet achat!!!")
                    else :
                        quantite_restant = produit[3] - quantite
                        requete_vente = """INSERT INTO l_ventes (id_produit,quantite) VALUES(%s, %s)"""
                        requete_produit = """UPDATE produits SET quantite = %s WHERE id = %s"""
                        with connexion.cursor() as curseur :
                            curseur.execute(requete_vente,(id_produit,quantite))
                            curseur.execute(requete_produit,(quantite_restant,id_produit))
                            connexion.commit()
                            print("La vente a ete effectuer avec succes!!")
                
               
        else : 
            print("Aucun produit pour le moment")
        print('~'*75,'\n')
    


def afficher_liste_vente() :
    print("Liste des ventes :")
    with connexion.cursor() as curseur :
        requete = """SELECT v.id, p.nom, v.quantite, (v.quantite*p.prix) as montant FROM l_ventes v JOIN produits p ON v.id_produit = p.id"""
        curseur.execute(requete)
        liste_vente = curseur.fetchall()
        if len(liste_vente) != 0 :
            for vente in liste_vente :
                print(f"ID : {vente[0]} | PRODUIT : {vente[1]} | QUANTITE : {vente[2]} | MONTANT : {vente[3]}")
                print('~'*70,'\n')
        else : 
            print("Aucune vente pour le moment ")











print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\t\t GESTION DE PRESENCE")
print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
while True :
    choix = input("Veuillez faire un choix selon ce que vous voulez faire : "
        "\n1 - Ajouter une categorie" 
        "\n2 - modifier une categorie" 
        "\n3 - supprimer une categorie"
        "\n4 - Afficher la listes des categories"
        "\n5 - Ajouter un produit"
        "\n6 - Afficher la liste des produits" \
        "\n7 - Modifier la quantite d'un produit" 
        "\n8 - Supprimer un produit" \
        "\n9 - Rechercher un produit"
        "\n10 - Voir le Dashboard" \
        "\n11 - Effectuer une vente " \
        "\n12 - Afficher la liste des ventes"
        "\n13 - Quitter \n"
        "=========================================\n\t : ")
    if choix.isdigit() :
        choix = int(choix)
        match choix:
            case 1:
                ajout_categorie()
                
                
            case 2:
                modification_categorie()
            
            
            case 3:
                supprime_categorie()
                
            case 4:
                affichage_categorie()
                
            case 5:
                ajout_produit()
            
            case 6:
                afficher_produit()
            
            case 7:
                modifier_qte_produit()

            case 8:
                supprimer_produit()

            case 9:
                rechercher_produit()

            case 10:
                dashboard()

            case 11:
                effectuer_vente()

            case 12:
                afficher_liste_vente()

            case 13 :
                exit

            case _:
                print("Choix invalide")

    else :
        print("Erreur! Votre choix doit etre un nombre entier : ")