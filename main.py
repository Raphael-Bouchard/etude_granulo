from main_function import *


"""
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\    OBJECTIFS DU CODE    /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

Fichier permettant de gérer l'ensemble de la simulation
1) creation du sample
2) essaie triaxial
3) post traitement


 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\     DÉTAILS DU CODE     /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

Les étapes détaillées du code sont :
    1) Lecture du fichier de données input_data.py
    2) Vérifie si l'on veut créer des samples
        2.1) (Si oui), vérifie si l'ont doit créer un nvx fichier de résultat, où si on réutilise un ancien dossier
        2.2) Lancement de la creation des samples (DEM/CreaSample_yade.py)
    3) Vérifie si l'on veut procéder à l'essaie triaixial sur le sample
        3.1) (Si oui), vérifie la présence des fichiers de resultats
        3.2) Lance une boucle de simu pour traiter l'ensemble des fichiers trouvés (DEM/CompressTriax_yade.py)
    4) Vérifie si l'on veut procéder au psot-traitement sur le sample
        4.1) (Si oui), vérifie la présence des fichiers de resultats
        4.2) Lance une boucle de simu pour traiter l'ensemble des fichiers trouvés (Post_Traitement/posttraitement.py)


 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\   ORGANISATION DU CODE  /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

 Comme tous mes codes ce script est organisé de la manière suivante

    1) en en tete les import
    2) les functions utiles au code
    3) le corps du code

    PS : si aucune fonction n'est dans le script c'est qu'elles sont écrites
         dans un autre script portant le même nom suivi de '_function'
"""


"""
Ici on execute le fichier 'input_data.py'
Ce qui nous permet de recupérer toutes les variables définies à l'intérieur
et de les utiliser directement

A noter :
exec() Parameters

The exec() method takes three parameters:

    object - Either a string or a code object
    globals (optional) - a dictionary
    locals (optional) - a mapping object (commonly dictionary)

PS : Il faut savoir que dans ce code et DEM/CreaSample_yade.py, on l'utilise comme telle
     Mais que dans CompressTriax_yade.py il est dans une boucle et on a du ajouter (2fois)
     l'option globals() et je sias pas pourquoi
     A priori --> l'option local les transforme en variable locals
     A priori --> l'option global les transforme en variable globals
"""
exec(open('input_data.py').read())
# 'initial_chemin' est une variable tampon servant pour l'appelle de la fonction PathToSample()
# car comme on fait des operations sur la variable "chemin"
# cela nous permet onc de garder le chemin de base au cas ou on utilise
# la fonction ReutilisationAncienDossierResultats
initial_chemin = chemin


"""
On pourrait prevoir une commande pour les faire sur des processeurs differents
a voir etc ...

A cogiter quand tout fonctionnera en automatique
"""



"""
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\   CREATION DES SAMPLES  /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

Ce gère via la variable 'dictionnaire_simu {creation_sample}' dans input_data.py
"""
if dictionnaire_simu['creation_sample'] == True :
    """
    La boucle if ci dessous permet de créer ou non un nvx dossier de résultats
    Depend de la variable 'creation_chemin' dans input_data.py, on gere alors
    l'ensemble des dossiers de resultats
    """
    if creation_chemin == True :
        chemin = CreationNouveauDossierResultats(ListTargetVoidRatio,chemin)
    else :
        chemin = ReutilisationAncienDossierResultats(initial_chemin, chemin,dictionnaire_simu)

    print("")
    print("Lancement de yade pour la création des samples : ")
    print("")
    os.system('yade DEM/CreaSample_yade.py '+ os.getcwd()+'/'+ chemin)





"""
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\     ESSAIE TRIAXIAL     /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

Condition de lancement de l'essaie triaxial
Ce gère via la variable 'dictionnaire_simu {essaie_triaxial}' dans input_data.py

Dans la boucle ci-dessous nous allons faire une liste de l'ensemble des essaies triaxial
a faire en fonction des fichier de résultats présent
SI vous ne voulait en faire qu'un ou autre etc.. a vous de gérer vos fichiers de résultats
et/ou lancer les essaie triax à la main via CompressTriax_yade.py
"""
if dictionnaire_simu['essaie_triaxial'] == True :
    # option est variable permettant de modifier certains parametres dans certaines fonctions
    # tel que MiseEnPlaceSimu() par exemple --> en fait ça joue dans SelectionFichieraTraiter()
    # qui est présent dans MiseEnPlaceSimu() voila pourquoi
    option = "essaie_triax"
    """
    La fonction MiseEnPlaceSimu() nous permet de récuperer deux listes
        1) La liste des chemin menant aux dossiers contenant les fichiers de sample
        2) La liste des noms des fichiers de sample présent dans les dossiers dont les noms sont présent dans la prmeiere liste
    """
    liste_chemin_sample, Liste_des_fichiers_pour_essaie_triax = MiseEnPlaceSimu(initial_chemin,option)
    """
    On vérifie ici que la liste des fichiers à traiter n'est pas vide, afin d'éviter
    de lancer yade pour rien
    """
    if len(Liste_des_fichiers_pour_essaie_triax)!=0 :
        print("")
        print("Lancement de yade pour les essaies Triaxaux")
        print("")
        """
        Ici on lance pleins de fois yade contrairement a la creation des samples.
        Mais pourquoi?

        La reponse est simple la focntion os.system() ne prend en variable que des strings
        Et passer la liste des chemins jusqu'au sample en un enorme string, puis faire
        un traitement dans CompressTriax_yade.py pour la reséparer et le transformer en une liste de string,
        est plus chiant que de faire une boucle for et d'ouvrir un certains nbre de fois yade,
        surtout que l'ouverture de yade ets pas si long que ça comparé au temps d'une simulation
        """
        for i in range(0,len(Liste_des_fichiers_pour_essaie_triax)) :
            print("")
            print("")
            print("On traite le dossier",liste_chemin_sample[i]," avec le fichier",Liste_des_fichiers_pour_essaie_triax[i])
            print("")
            os.system('yade DEM/CompressTriax_yade.py ' + os.getcwd()+'/'+ liste_chemin_sample[i] +" "+ Liste_des_fichiers_pour_essaie_triax[i])


"""
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\     POST TRAITEMENT     /!\ /!\ /!\ /!\ /!\ /!\
 /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

Condition de lancement du post traitement
Ce gère via la variable 'dictionnaire_simu {post_traitement}' dans input_data.py
"""
if dictionnaire_simu['post_traitement'] == True :
    # option est variable permettant de modifier certains parametres dans certaines fonctions
    # tel que MiseEnPlaceSimu() par exemple
    option = "post_traitement"
    liste_chemin_sample, Liste_des_fichiers_pour_post_traitement = MiseEnPlaceSimu(initial_chemin,option)
    """
    On vérifie ici que la liste des fichiers à traiter n'est pas vide, afin d'éviter
    de lancer yade pour rien
    """
    if len(Liste_des_fichiers_pour_post_traitement) !=0 :
        print("")
        print("Lancement du code posttraitement.py")
        print("")
        nom_couple_tous_les_fichiers =''
        for i in range(0,len(Liste_des_fichiers_pour_post_traitement)) :
            """
            Ici on juxtapose tous les chemins et noms de ficheir a traiter avec le symbole '%'
            Puis dans le fichier de post traitement on separe le tout pour récupérer
            nos listes de dossier et de fichiers
            --> permet d'appeler le code de  post-traitement une seule fois

            la fonction os.getcwd() donne le chemin absolu jusqu'au repertoire courant
            """
            nom_couple_tous_les_fichiers +=  os.getcwd()+'/'+liste_chemin_sample[i]+'/'+Liste_des_fichiers_pour_post_traitement[i]+'%'
        os.system('python3 Post_Traitement/posttraitement.py ' + nom_couple_tous_les_fichiers +" " + os.getcwd())
