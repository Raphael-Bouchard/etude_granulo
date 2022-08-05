import os
import re
import sys
import shutil
from datetime import datetime




"""
Fichier contenant toutes les fonctions utilisées dans le fichier main.py
"""

################################################################################
#### /!\ Toutes functions servant à gérer l'ensemble des simulations  /!\   ####
### /!\ Bien lire la description de chaque fonction avant de les modifiers  ####
################################################################################


"""
Fonction qui créé un dossier de résultat pour stocker les samples aux formats
souhaités
Plus on copie le fichier d'input au niveau des dossier void ratio pour se rappeler
de nos parametres

input : Liste[float] et string
        Liste des void ratio souhaités
        chemin jusqu'aux resultats

Output : string
         chemin incrementé du dossier '/date_et_heure'
"""
def CreationNouveauDossierResultats(ListTargetVoidRatio,chemin) :
    """
    Ici on verifie le dernier caractere du nom du chemin et on le supprime si c'est un
    '/', parce que ça pourrait créer des problème dans la gestion des dossiers/fichiers
    de résultat
    """
    if chemin[-1] == '/' :
        chemin = chemin[:len(chemin)-1]



    """
    Vérifie si le dossier donné par la variable 'chemin' dans input_data.py existe. Si oui, ne fait rien, si non, le créé
    """
    if os.path.exists(chemin) == False :
        os.mkdir(chemin)

    """
    On recupere la date au format souhaité, qui servira de nom de dossier de résulat
    """
    name_time = str(datetime.now().strftime('%Y-%m-%d_%H:%M'))


    chemin+="/"+name_time
    """
    On va créer dans le dossier donné par la variable 'chemin' dans input_data.py, un dossier ayant pour nom la date_et_l'heure
    """
    if os.path.exists(chemin):
        print("""les fichiers de résultat seront ecris dans le dossier""", chemin+'/'+name_time,"""
A condition d'avoir mis la variable 'dictionnaire_simu {creation_sample = True }' """)
    else:
        os.mkdir(chemin)
        print("""les fichiers de résultat seront ecris dans le dossier""", chemin+'/'+name_time,"""
A condition d'avoir mis la variable 'dictionnaire_simu {creation_sample = True }' """)



    """
    On copie notre fichier d'input au niveau des resultats
    """
    shutil.copy('input_data.py',chemin)
    """
    On garde en mémoire le chemin : sample/date_et_heure/
    """
    return  chemin



"""
Cette fonction sert a reutiliser le dernier dossier de resultat
C'est a dire qu'on va supprimer tout ce qu'il y a l'intérieur  Pour pouvoir y écrire les nouveau resultats
Cette fonction n'est utilisé que si la variable "creation_chemin" = False

si tu mets : 1) chemin = ''                                   --> s'arrete
             2) chemin = 'un nom de dossier qui n'existe pas' --> s'arrete

/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
/!\ Comme toute fonction qui supprime des fichiers/dossiers Si vous voulez la modifier    /!\
/!\ Ne le faite pas directement là ou vous avez tous vos resultats etc...                 /!\
/!\ Vous créez un autre dossier pour faire des tests avant de supprimer tout votre travail/!\
/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\


Input : string
        la variable chemin contenu dans le fichier input_data.py

output : string
        la variable chemin contenu dans le fichier input_data.py, avec le cractere '/' supprimé
        si c'est le dernier caractere
"""
def ReutilisationAncienDossierResultats(initial_chemin, chemin, dictionnaire_simu):

    """
    Ici on verifie le dernier caractere du nom du chemin et on le supprime si c'est un
    '/', parce que ça pourrait créer des problème dans la gestion des dossiers/fichiers
    de résultat
    """
    if chemin[-1] == '/' :
        chemin = chemin[:len(chemin)-1]



    if chemin =='' :
        print("""Vous n'avez pas mis de nom de dossier, votre manoeuvre va donc supprimer l'ensemble de vos fichiers
au niveau de là ou vous avez lancé le code, ce qui est UNE ENORME CONNERIE !  Le code va donc être stoppé """)
        exit("T'es pas futefute")

    if not os.path.exists(chemin) :
        print("""Le chemin indiqué via la la variable chemin n'existe pas, on ne peut donc pas réutiliser un dossier qui n'existe pas.
Vous avez plusieurs possibilités pour règler ce soucis :
        1) Passer la variable "creation_chemin" a True dans 'input_data.py', pour créer un nouveau dossier de résultat
        2) Mettre simplement la variable 'chemin' dans 'input_data.py' avec un nom dossier qui existe vraiment

/!\ Dernier avertissement, nous rappelons que dans le cadre de la reutilisation d'un dossier de resultat (i.e vous voulez utiliser l'option 2)
Le code est fait de telle manière que dans le dossier que vous allez indiquer dans la variable 'chemin', nous allons récupérer le dernier dossier
par ordre alphabetique, et supprimer tout ce qui est dedans, alors faites attention /!\ """)
        exit("T'es pas futefute")

    # la on recupere la liste des noms des dossiers contenu au niveau de chemin
    # normalement chemin = 'sample' (mais vous pouvez le modifier si il faut)
    # donc normalement liste_chemin contient la liste de tous les dossiers
    # de type 'date_et_heure', triée par ordre alphabetique
    liste_chemin= RecupUniquementListeDossier(chemin)
    """
    On verifie que le chemin donné dans input_data contient des dossiers, pouvant servir pour les resultats
    Sinon on en créé un
    """
    if len (liste_chemin) == 0:
        """
        On recupere la date au format souhaité, qui servira de nom de dossier de résulat
        """
        name_time = str(datetime.now().strftime('%Y-%m-%d_%H:%M'))
        chemin+="/"+name_time

        """
        On va créer dans le dossier donné par la variable 'chemin' dans input_data.py, un dossier ayant pour nom la date_et_l'heure
        """
        os.mkdir(chemin)
        print("les fichiers de résultat seront ecris dans le dossier", chemin)
    else :
        # on ajoute a chemin le dernier de la liste, donc le 'plus recent'
        chemin = chemin +'/'+liste_chemin[-1]

    # commme le nom de la fonction précendente l'indique, cette focntion recupere
    # les chemin menant aux samples présent dans le dossier date_et_heure le
    # plmus recent
    liste_chemin_sample = RecupPathToSample(initial_chemin)
    # cette boucle sert a supprimer les dossier de type void_ratio present dans
    #le dossier date_et_heure le plsu recent
    if dictionnaire_simu['creation_sample'] == True :
        for i in range(0, len(liste_chemin_sample)) :
            shutil.rmtree(liste_chemin_sample[i])
        # cette boucle supprime les fichier present dans le dossier date_et_heure
        # le plus recent
        for filename in os.listdir(chemin) :
            os.remove(chemin + "/" + filename)
            # on copie le nouveau dossier d'inout dans le dossier date_et_heure le plsu recent
            # qui va servir pour notre simulation
        shutil.copy('input_data.py',chemin)

    return  chemin




"""
Fonction permettant de recupérer une liste triée par ordre alphabétique
contenant l'ensemble des noms des dossiers contenu au niveau de 'chemin'

input  : chemin vers un dossier (string)
output : liste de nom            (list)
"""
def RecupUniquementListeDossier(chemin) :

    liste_fichier = os.listdir(chemin) # on liste les doissier de date et on les trie par ordre alhabétique
    liste_dossier =[]
    for i in range(len(liste_fichier)):
        #la fonction split separe en deux l'enxtension du nom du fichier
        # le [1] a la fin indique qu'on récupere l'extension
        # le [0] a la fin indique qu'on recupere le nom du fichier
        extension = os.path.splitext(liste_fichier[i])[1] #recupère l'extension du fichier traité
        nom_fichier = os.path.splitext(liste_fichier[i])[0] # recupere le nom du fichier

        # on traite le cas où il n'y a pas d'extension
        if extension == '':
            liste_dossier +=[nom_fichier]

    liste_dossier = sorted(liste_dossier)
    return liste_dossier



"""
Fonction permettant de recupérer le chemin jusqu'au fichier de sample
i.e [sample/date_et_heure/void_ratio1, etc , ...]
Cette fonction fonvtionne uniquement si l'on garde l'organisation des dossiers tel
qu'elle a été pensé, sinon ça ne fonctionnera plus

input : string
        la base du chemin (i.e : le nom du chemin mis à la variable "chemin" Dans
        inpu_data.py -->)
output : liste des chemin jusqu'à chaque fichier de donnée de sample pour l'essaie triax (list)
"""
def RecupPathToSample(chemin) :
    liste_dossier_date = RecupUniquementListeDossier(chemin)
    chemin+= '/'+liste_dossier_date[-1]+'/'
    liste_dossier_void_ratio = RecupUniquementListeDossier(chemin)
    liste_chemin_sample=[]
    for i in range(len(liste_dossier_void_ratio)) :
        liste_chemin_sample +=[chemin+liste_dossier_void_ratio[i]]
        liste_chemin_sample = sorted(liste_chemin_sample)
    return liste_chemin_sample



"""
Fonction permettant de recupérer dans un dictionnaire de l'ensemble des extensions
ainsi que la liste des noms de fichier associée

Input : liste de string contenant les chemins jusqu'au fichier des samples
Ouput : dictionnaire{ 'extension' : [liste des fchiers associes], etc ...}
"""
def RecupDictExtensionListeFichier(chemin_to_sample) :
    # On créé un dictionnaire qui associe a chque extension la liste des nom de
    #fichiers contenu dans le dossier
    dictionnaire_extension={}

    # ici on liste les fichier contenur dans le dossier psoitionné en premier
    # dans la liste liste_chemin_sample
    print("--------------------------------------------------------------------------------------------------------------------")
    print("""Le dossier de résultat traité est :""", chemin_to_sample,"""
    Si ce n'est pas celui que vous voulez traiter, vous avez plusieurs possibilités :
        1) Allez régler à la main les dossiers et/ou fichiers que vous voulez traiter dans CompressTriax_yade.py
        2) Supprimer tous les dossiers arrivant avant le votre dans l'ordre alphabetique, toutefois ça ressemble à une connerie
        """)

    liste_fichier = os.listdir(chemin_to_sample)

    for i in range(len(liste_fichier)):
        #la fonction split separe en deux l'enxtension du nom du fichier
        # le [1] a la fin indique qu'on récupere l'extension
        # le [0] a la fin indique qu'on recupere le nom du fichier
        extension = os.path.splitext(liste_fichier[i])[1] #recupère l'extension du fichier traité
        nom_fichier = os.path.splitext(liste_fichier[i])[0] # recupere le nom du fichier

        # on traite le cas où il n'y a pas d'extension
        if extension == '':
            extension = 'dossier'
        # on traite le cas des fichier yade.gz car c'est une "double" extension
        # vu qu'il y a deux points
        # c'est une manire de faire, on aurait pu faire differement
        # mais j'aime bien comme ça
        if extension =='.gz':
            extension = '.yade.gz'
            # du coup ici on recupere le vrai nom du fichier
            nom_fichier =os.path.splitext(os.path.splitext(liste_fichier[i])[0])[0]

        #la boucle ci-dessous indique que si l'extension existe deja dans le dictionnaire
        #nous ajoutons le fichier à la liste existante
        #sinon, nus créons une nouvelle cles de dictionnaire ainsi que la liste associée
        if extension in dictionnaire_extension :
            dictionnaire_extension[extension]+=[nom_fichier]#[os.path.splitext(liste_fichier[i])[0]]
        else:
            dictionnaire_extension[extension] =[nom_fichier]#[os.path.splitext(liste_fichier[i])[0]]


    return dictionnaire_extension




"""
Ici nous avons une fonction qui va nous permettre de choisir quel est le bon fichier pour appliquer notre essaie triaxial
Cette focntion privilégie l'utilisation d'un fichier '.yade.gz', mais si un fichier adéquat '.py' est trouvé, il sera utilisé
(si on ne trouve pas de '.yade.gz'  biensur)

input : dictionnaire et string (chemin jusq'au fichier de sample)
output : string , le nom du fichier a utiliser pour la simulation
"""
def SelectionFichieraTraiter(dictionnaire_extension,chemin_to_sample,option) :
    # contiendra le nom du fichier à traiter
    selected_file = ''
    # sert quand il y a plusieurs fichier possible à traiter
    liste_des_fichiers_possibles_a_traiter = []
    #permet un affichage plus tard, en vrai ça sert un peu à que dalle
    count =0

    if option == "essaie_triax" :
        # cette variable va servir a comparer le nom des fichiers pour savoir lequel séléctionner
        nom_a_comparer = 'Sample_State_'
        #nom_a_comparer = 'compactedState_'
        # sert quand il y a plusieurs fichier possible à traiter
        liste_des_fichiers_possibles_a_traiter = []
        # liste extension a tester dans notre cas particulier
        liste_extension_a_tester = ['.yade.gz' , '.py']
        # sert pour savoir combien d'extension preente de la lsite des extension a testé on etet teste
        LimitCount = 2
    if option == "post_traitement" :
        # cette variable va servir a comparer le nom des fichiers pour savoir lequel séléctionner
        nom_a_comparer = "Data_to_Plot_VoidRatios"
        #nom_a_comparer = 'compactedState_'
        # liste extension a tester dans notre cas particulier
        liste_extension_a_tester = ['.dat']
        # sert pour savoir combien d'extension preente de la lsite des extension a testé on etet teste
        LimitCount = 1



    for key in liste_extension_a_tester :

        # boucle au cas ou il y a plusieurs de fichier de résultats possible
        # on verifie si l'extension 'key' existe dans le dictionnaire ainsi que le nombre de fichier ayant cette exension
        #si il n'y a pas d'extension 'key', on va regarder les extension'.py
        if (key in dictionnaire_extension) and len(dictionnaire_extension[key])> 1 :
            # on parours la liste de fichier tant l'extenson 'key'
            for i in range(len(dictionnaire_extension[key])) :

                # pour chaque nom de fichier dans cette liste on la compare a notre chaine de charactere de reference
                if dictionnaire_extension[key][i][0:len(nom_a_comparer)] == nom_a_comparer :
                    #si la condition est de comparaison est vrai on ajoute le ds fichier à la liste des fichier possibles à traiter
                    liste_des_fichiers_possibles_a_traiter += [dictionnaire_extension[key][i]]
            if len(liste_des_fichiers_possibles_a_traiter)>1 :
                print("")
                print("""La liste des fichiers d'extension key contient plus deux fichiers commmençant par :""", nom_a_comparer,"""
La liste des fichiers est la suivante :""", liste_des_fichiers_possibles_a_traiter,"""
Le code va être stoppé, vous avez plusieurs possibilités pour régler ce probleme :
    1) Allez faire du ménage dans le dossier""",chemin_to_sample,"""car il ne devrait y a avoir qu'un seul fichier commençant par :""", nom_a_comparer,"""
    2) Modifier la fonction SelectionFichieraTraiter() dans le fichier CompressTriax_yade.py qui permet de séléctionner les fichiers à traiter""" )
                exit()
            # normalement le elif juste en dessous ne sert a rien car impossible
            elif len(liste_des_fichiers_possibles_a_traiter)== 0 :
                print("""Il y a plusieurs fichier portant l'extension""",key,"""
Mais il ne porte pas le nom qu'il devrait, nous allons vous montrer la liste de l'ensemble des fichier contenu dans ce dossier :""",chemin_to_sample,"""
On rappelle que le nom du fichier devrait commencer par :""",nom_a_comparer)
                print('{')
                for key in dictionnaire_extension :
                    print(len(dictionnaire_extension[key]),"fichiers ", key, ": \n", dictionnaire_extension[key], "\n")
                print('}')
                print("")
            else :
                print("A priori ",option," de ce sample a déjà été effectué, mais ayant trouvé un fichier aquéquat la simulation va être lancée")
                selected_file = liste_des_fichiers_possibles_a_traiter[0]+key
                print(selected_file)
                #permet de stopper la boucle for du tout début
                # car en effet quand on a un seul fichier on sait que c'est le bon
                break

        # nous sommes dans le cas où nous avons un seul fichier ayant l'extension 'key'
        # boucle if principale
        elif (key in dictionnaire_extension) and len(dictionnaire_extension[key])== 1 :

            # on verifie si c'est bien un fihcier qui n'a pas déjà subit la compression triaxial
            if dictionnaire_extension[key][0][0:len(nom_a_comparer)] == nom_a_comparer :
                selected_file += dictionnaire_extension[key][0]+key
                print("Le fichier utilisé pour ",option," du dossier :",chemin_to_sample," est : ", selected_file)
                print("")
                print("")
                #permet de stopper la boucle for du tout début
                break
            else :
                print("""Il y a un fichier portant l'extension""",key,"""
Mais il ne porte pas le nom qu'il devrait, nous allons vous montrer la liste de l'ensemble des fichier contenu dans ce dossier :""",chemin_to_sample,"""
On rappelle que le nom du fichier devrait commencer par :""",nom_a_comparer)
                print('{')
                for key in dictionnaire_extension :
                    print(len(dictionnaire_extension[key]),"fichiers ", key, ": \n", dictionnaire_extension[key], "\n")
                print('}')
                print("")
        else :
            print("Il n'y a pas de fichier",key,"pouvant servir pour",option," prévu")
            count +=1
            if count == LimitCount :
                print("""La liste de fichier contenu dans le dossier :""",chemin_to_sample,"""est la suivante :""")
                print('{')
                for key in dictionnaire_extension :
                    print(len(dictionnaire_extension[key]),"fichiers ", key, ": \n", dictionnaire_extension[key])
                print('}')

    return selected_file




"""
Cette fonction est utile pour lancer les essaie triaxiaux ainsi que le
post traitement
De nombreuses étapes utilsant les fonctions ci-dessus sont données
Il faut garder en mémoire que cette fonction permet de récuper la liste des
ficher à  traiter ainsi que leur chemin d'accès

input : string et string
        initial chemin : donné dans input_data --> permet d'aler chercher les fichiers résultats
        option : permet de savoir si on est dans le cass du post traitement ou de l'essaie triaxiale
ouput : Liste et liste
        liste_chemin_sample : liste des chemin jusqu'au fichiers de résultats
        Liste_des_fichiers_a_traiter : liste des noms des fichiers de resultats a traiter

"""
def MiseEnPlaceSimu(initial_chemin, option):
    # on recupere les chemin menant au fichier des samples
    # recupere automatiquement le fichier le plus recent
    liste_chemin_sample = RecupPathToSample(initial_chemin)

    """
    Dans le cadre où nous referions un post traitement, il y aura un dossier
    sample/date_et_heure/multi_resultat et pour éviter un affichage inutile qui arrivera plus tard
    on supprime de la liste les nom finissant par 'multi_resultat' et 'resultat'
    """
    for i in range(0, len(liste_chemin_sample)) :
        if liste_chemin_sample[i][liste_chemin_sample[i].rfind('/')+1:] == 'multi_resultat' or liste_chemin_sample[i][liste_chemin_sample[i].rfind('/')+1:] == 'resultat' :
            del liste_chemin_sample[i]


    # cas ou il n'y a pas fichier de resultats
    # i.e les chemisn sample/date_et_heure/void_ratio n'existent pas
    if len(liste_chemin_sample) == 0 :
        # va montrer la limite du chemin (ie sample/date_et_heure)
        limite_chemin = RecupUniquementListeDossier(initial_chemin)
        if len(limite_chemin) != 0 :
            print("""Le dossier :""", initial_chemin+'/'+limite_chemin[-1],""" ne contient aucun dossier resultats.
L'""",option,""" ne peut donc pas être réalisé.

Il faut donc d'abord créer des samples via la variable 'dictionnaire_simu {creation_sample}' dans input_data.py
Le code va donc être stoppé""")
            exit("")
        # cas ou la limite du chemin beh c'est sample
        else :
            print("""Le dossier :""", initial_chemin,""" ne contient aucun dossier resultats.
Il faut donc d'abord créer des samples via la variable 'dictionnaire_simu {creation_sample}' dans input_data.py
Le code va donc être stoppé""")
            exit("")

    Liste_des_fichiers_a_traiter=[]
    # car les chemin ne contiendront pas de rficheir de resultats
    liste_des_indices_a_supprimer=[]
    for i in range(0,len(liste_chemin_sample)):
        dictionnaire_extension = RecupDictExtensionListeFichier(liste_chemin_sample[i])
        selected_file = SelectionFichieraTraiter(dictionnaire_extension,liste_chemin_sample[i],option)
        if selected_file != '' :
            Liste_des_fichiers_a_traiter +=[selected_file]
        else :
            liste_des_indices_a_supprimer.append(i)

    # on supprime de liste_dmin_sample tous les odssier ne contenant pas de fichier de resultats 
    for i in range(0,len(liste_des_indices_a_supprimer)):
        del liste_chemin_sample[liste_des_indices_a_supprimer[i]]


    # si il ya des dossiers de résultats (avec les fichiers dedans)
    print('')
    if len(Liste_des_fichiers_a_traiter)== 0 :
        print("Aucun fichier de résultats n'a été trouvé, la simulation",option,"est donc terminée")

    else :
        print("Les fichiers qui seront traités sont donc les suivants :")
        for i in range(0,len(Liste_des_fichiers_a_traiter)) :
            print(liste_chemin_sample[i]+'/'+Liste_des_fichiers_a_traiter[i])

    return liste_chemin_sample, Liste_des_fichiers_a_traiter
