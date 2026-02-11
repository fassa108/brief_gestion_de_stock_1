import mysql.connector
import hashlib
import getpass
connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Binetougueye@2",
    database="gestion_stock"
)

if connexion :
    print('connexion a la base reussie')




def demander_entier(message):
    while True :
        valeur = input (message)
        try :
            if int(valeur) >= 0 :
                return int(valeur)
        except (ValueError,TypeError) as e :
            print("Vous devez saisir un nombre entier positif!!!")


def demander_decimal(message):
    while True :
        valeur = input (message)
        try :
            return float(valeur)
        except (ValueError,TypeError) as e :
            print("Vous devez saisir un nombre entier ou decimal!!!")


def demander_chaine_non_vide(message) :
    while True :
        valeur = input(message).strip()
        if valeur == "" :
            print("Le champs ne peut pas etre vide!!!")
        elif valeur.isdigit() :
            print("Vous ne devez pas ecrire uniquement des chiffres!!!")
        else :
            return valeur
def demander_mdp(message) :
    while True :
        valeur = getpass.getpass((message)).strip()
        if valeur == "" :
            print("Le champs ne peut pas etre vide!!!")
        
        else :
            return valeur



def ajout_utlisateur() :
    print('~'*8,"Ajout d'utilisateur",'~'*8)
    nom = demander_chaine_non_vide("Veuillez saisir votre nom : ")
    prenom = demander_chaine_non_vide("Veuillez saisir votre prenom : ")
    email = demander_chaine_non_vide("Veuillez saisir votre adresse email : ")
    mot_de_passe = demander_mdp("Veuillez saisir votre mot de passe : ")
    mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    requete = """INSERT INTO utilisateurs (nom,prenom,email, mot_de_passe) VALUES (%s, %s, %s, %s)"""

    with connexion.cursor() as curseur :
        curseur.execute(requete,(nom,prenom,email,mot_de_passe))
        connexion.commit()
        print("Utilisateur ajoute avec succes!")



def se_connecter() :
    while True :
        email_saisi = demander_chaine_non_vide("Veuillez saisir votre email : ")
        mdp_saisi = demander_mdp("Veuillez saisir votre mot de passe : ")
        requete = """SELECT * FROM utilisateurs WHERE email = %s"""
        with connexion.cursor() as curseur :
            curseur.execute(requete,(email_saisi,))
            resultat = curseur.fetchone()
            if resultat is not None :
                mdp_hash = hashlib.sha256(mdp_saisi.encode()).hexdigest()
                if mdp_hash != resultat[4] :
                    print("Email ou mot de passe incorrecte!!!")
                else :
                    profil_user = resultat[5]
                    menu_principal(resultat)
            else :
                print("Email ou mot de passe incorrecte!!!")

    

def authentification_par_action(id) :
    requete = """SELECT profil FROM utilisateurs WHERE id = %s"""
    with connexion.cursor() as curseur :
        curseur.execute(requete,(id,))
        profil = curseur.fetchone()
        if profil == 'admin' :

            return True
        else :
            return False





def ajout_categorie() :
    print('~'*8,"Ajout de categorie",'~'*8)
    while True :
        nom = demander_chaine_non_vide("Veuillez entrer le libelle de la categorie : ")
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
    choix = demander_entier("Veuillez saisir l'id de la categorie que vous voulez modifier : ")
    # choix = int(choix)
    for categorie in liste_categorie :
        if categorie[0] == choix :
            nouveau_nom_categorie = demander_chaine_non_vide("Veuillez sasir le nom de la nouvelle categorie : ")
            with connexion.cursor() as curseur :
                query = """UPDATE  categories SET libelle = %s WHERE id = %s"""
                curseur.execute(query,(nouveau_nom_categorie,choix))
                connexion.commit()
                print("La categorie a ete modifiee avec succes!")
        else :
            print("Cette categorie n'existe pas!!!")

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
            print("Pas de categorie pour le moment")
    return liste_categorie

def supprime_categorie() :
    liste_categorie = affichage_categorie()
    while True :
        id = demander_entier("Veuillez saisir l' id de la categorie que vous voulez supprimer : ")
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
        libelle = demander_chaine_non_vide("Veuillez saisir le libelle du produit : ")
        prix = demander_decimal("Veuillez sisir le prix du produit : ")
        quantite = demander_entier("Veuillez saisir la quantite du produit : ")
        liste_categorie = affichage_categorie()
        id_cat = demander_entier("Veuillez saisir l'id de la categorie correspondante : ")

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
    id_produit_saisi = demander_entier("Veuilles choisir l'id du produit dont vous voulez modifier la quantite : ")
    for produit in liste_produit :
        if id_produit_saisi == produit[0] :
            new_quantite = demander_entier("Veuillez saisir la nouvelle quantite : ")
            
            with connexion.cursor() as curseur :
                requete = """UPDATE produits SET quantite = %s WHERE id = %s"""
                curseur.execute(requete,(new_quantite,id_produit_saisi))
                print("La quantite a ete modifiee avec succees!")
        else : 
            print("Le produit n'existe pas")
    

def supprimer_produit() :
    liste_produit = afficher_produit()

    id_produit = demander_entier("Veuillez saisir l'id du produit que vous voulez supprimer : ")
    
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
    mot_cle = demander_chaine_non_vide('Veuillez saisir le libelle du produit a rechercher : ').strip()
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

            id_produit = demander_entier("Veuillez saisir l'id du produit que vous voulez acheter : ")

            for produit in liste_produit :
                if id_produit == produit[0] :
                    quantite = demander_entier("Veuillez sasir la quantite souhaite : ")
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




def menu_connexion() :
    while True :

        print("Veuillez taper ")
        print("1 . Connexion")
        print("2 . Inscription")
        print("0 . Quitter la programme")
        choix_saisi = demander_entier("\t : ")
        
        match choix_saisi :
            case 1 :
                user = se_connecter()
            case 2:
                ajout_utlisateur()
            case 0 :
                exit()




def menu_principal(utilisateur):
    id = utilisateur[0]
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\t\t GESTION DE STOCK")
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    

    while True :
        print("Veuillez faire un choix selon ce que vous voulez faire : ")
        print("1 - Afficher la liste des produits") 
        print("2 - Rechercher un produit") 
        print("3 - Effectuer un achat")
        if utilisateur[5] == 'admin':
            print("4 - Voire la liste des categories")
            print("5 - Ajouter une categorie")
            print("6 - modifier une categorie")
            print("7 - supprimer une categorie") 
            print("8 - ajouter un produit")
            print("9 - Modifier la quantite d'un produit")
            print("10 - Supprimer un produit")
            print("11 - Voir la liste des ventes") 
            print("12 - afficher le dashboard") 
            print("13 - ajouter un utilisateur")
        print("0 - Quitter \n","="*30)
        choix = demander_entier("\n\t : ")
        
        match choix:
            
            case 1:
                afficher_produit()
                
                
            case 2:
                rechercher_produit()
            
            
            case 3:
                effectuer_vente()
                
            case 4:
                
                if authentification_par_action(id) :
                    affichage_categorie()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 5:
                if authentification_par_action(id) :
                    ajout_categorie()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")
            
            case 6:
                if authentification_par_action(id) :
                    modification_categorie()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")
            
            case 7:
                if authentification_par_action(id) :
                    supprime_categorie()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 8:
                if authentification_par_action(id) :
                    ajout_produit()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 9:
                if authentification_par_action(id) :
                    modifier_qte_produit()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 10:
                if authentification_par_action(id) :
                    supprimer_produit()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 11:
                if authentification_par_action(id) :
                    afficher_liste_vente()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 12:
                if authentification_par_action(id) :
                    dashboard()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")

            case 13 :
                if authentification_par_action(id) :
                    ajout_utlisateur()
                else :
                    print("Vous n'etes pas autoriser a effectuer cette action!!!")
            
            case 0:
                    menu_connexion()

            case _:
                print("Choix invalide")

        



menu_connexion()