import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.animation as manimation
import numpy as np
import os
import re
import sys




"""
Script contenant Toutes les fonctions qui seront utiles au post traitement
"""


parseLine = lambda a : a.split()


"""
Cette fonction recupere un fichier de donnée et transforme son contenu en une matrice
géante
input : string
        chemin d'accès au focheir de donnée

output : Liste de liste
        Liste[L1[], L2[], etc ... ] --> peut etre vu comme une matrice car chaque liste
        contient chque information de la matrice ainsi l'élement
        matrice[i][j] correspond à Li[j] --> element j de la liste i
                                         --> element j de la ieme colonne du fochier de resultat
"""
def info_list_parse(str_path_client_list):
    with open(str_path_client_list, "r") as file:
        matrice = []
        for line in file:
            if(len(parseLine(line))>1):
                matrice.append(parseLine(line))
        #for x in matrice:
        #    print(*x, sep=" ")
        return matrice

        #create vector with information selected



"""
Fonction permettant de selectionner les élements souhaitées dnas la matrice
et de les stockée comme on le souhaite

input : La matrice (i.e une liste de liste )

Ouput : ce qu'on veut garder ... actuellement j'ai 6 liste que j'utilise apres
        mais ça c'est voué à etre modifié en fonction des besoins
"""
def getLineFromcolumn(matrice):
    line_name = []
    line_time  = []
    line_iter  = []
    line_epsilon_zz = []
    line_deviatoric_strain = []
    line_deviatoric_stress =[]
    for i in range(0,len(matrice[0])):
        line_name.append(matrice[0][i])
    for i in range(1,len(matrice)):
        #index,
        #l'indice des index commence à 0, et les virgules comptent comme une colonne
        #les données sont donc contenues que aux indices pairs ,0, 2, 4 et 6
        line_time.append(float(matrice[i][0]))
        line_iter.append(float(matrice[i][1]))
        line_epsilon_zz.append(float(matrice[i][2]))
        line_deviatoric_strain.append(float(matrice[i][3]))
        line_deviatoric_stress.append(float(matrice[i][4]))
    return line_time , line_iter ,line_epsilon_zz ,line_deviatoric_strain, line_name, line_deviatoric_stress



"""
Permet de trsnaformer une ligne d'un fichier en string
Utile dans le cas de fichier .csv

input : string
        ligne et u seul string geant
output : string
        ligne avec des espace entre chque terme de la ligne
"""
def lineToStr(line):
    lineStr = " "
    for x in line:
        lineStr += x + " "
    lineStr+="\n"
    return lineStr


"""
Fonctin permettant de prendre en compte tous les arguments onné au post traitement pour
ensuite mene a bien touts ce que l'ont veut
"""
def MiseEnPlacePostTraitement(name, path_to_input) :
    Liste_chemin_sample =[]
    Liste_nom_fichiers  =[]
    Liste_void_ratio    =[]
    test=False

    """
    Ici on recupere les noms des fichiers concatainés, dans la variable name,
    et on les separes pour remplir la liste 'Liste_nom_fichiers'

    A la fin de cette boucle 'Liste_nom_fichiers' contient le chemin complet jusqu'au
    fichier
    i.e : [/absolute/path/to/file/filename1, /absolute/path/to/file/filename2 , /absolute/path/to/file/filename3, etc...]
    """
    while test == False :
        Liste_nom_fichiers += [name[0:name.find('%')]]
        if name.find('%')+1 == len(name) :
            test = True
        else :
            name = name[name.find('%')+1:]

    """
    Dans cette boucle on va séparer les noms des fichiers de leuur chemin
    Ainsi que créer une listee des void ratios qui vont être traités
    """
    for i in range(0,len(Liste_nom_fichiers)) :
        """
        On recupere le chemin
        """
        Liste_chemin_sample +=[Liste_nom_fichiers[i][:Liste_nom_fichiers[i].rfind('/')]]
        """
        On garde que le nom du fichier
        """
        Liste_nom_fichiers[i]= Liste_nom_fichiers[i][Liste_nom_fichiers[i].rfind('/')+1:]
        """
        Ici on rercupere le void ratio
        """
        Liste_void_ratio += [Liste_chemin_sample[i][Liste_chemin_sample[i].rfind('/')+1:].replace('_','.')]

    """
    Ici on recupere le chemin ou seront tracé les courbes communes
    i.e sample/date_et_heure
    """
    chemin_multi_trace = Liste_chemin_sample[0][0:Liste_chemin_sample[0].rfind('/')]

    """
    Ici on execute encore une fois input_data.py afin de récupérer les options de tracé
    """
    exec(open(path_to_input+'/input_data.py').read(),globals())
    return OptionTrace, OptionMultiTrace, chemin_multi_trace, Liste_chemin_sample, Liste_nom_fichiers, Liste_void_ratio



"""
Fonction permttant de tracer automatiquement le deviatoric strain en fonction de epsilon ZZ

toutes les fonctions permettant de tracer les courbes prennent le mêm type d'argument
dans le même ordre :
input :     Liste   : abs --> abscisses du graph
            Liste   : ordo --> ordonnées du graph
            Liste   : void ratio --> Liste des void ratio --> sert pour les légendes
            string  : chemin --> chemin jusqu'au lieu de lecture des données (i.e chemin jusqu'aut dossier resultat)
            string  : chemin_multi_trace --> chemin menat au dossier multi_resultat
            Liste   : Liste_couleur_trace --> liste contenat 8 couelurs différentes, utile pour le multi trace car sur chque coubre de multi trace, la même couleur representera le me sample
            integer : count --> compte tour
            integer : n --> nbre de tour a effctuer --> sert en colaboratio avec count pour savoir quand sauvegarder les figures multi_trace
            bool    : optionTrace --> sert a savoir si l'on trace les courbve individuelles
            bool    : optionMultiTrace --> sert a savoir si l'on veut tracer le courbes multiTrace

output :    fig : les figures auvegardées si il y en a


/!\ Lire bien les commentaires de cette fonction, car elles marchent toutes de la même manière, je n'ai donc pas réécris les commentaires. /!\
"""
def TraceDeviatoricStrain(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n, optionTrace, optionMultiTrace) :

    """
    La première figure est celle tracé dans le dossier sample/date_et_heure/void_ratio/resultat
    et ne contient que une courbe, celle du void ratio traité

    Tandis que la seconde est celle ou sont tracé toutes les courbes pour une meme granulométire PONDÉRÉE
    /!\ le mot pondéré est important car c'est la seule variable commune, les granulométrie n'étant pas exactement les mes dans notre cas actuel
    et se situe dans le dossier sample/date_et_heure/multi_resultat
    """

    """
    Ici on érifie que l'utiliateur souhaite tarcé les courbes individuelles
    De plus il est interessant de noter le numero de la figure dans plt.figure( numfig , etc...)
    On veut que grace à la variable count la figure change de numero a chque itération de la bucle de tracé
    --> pemet d'avoir une seule courbe par graph
    """
    if optionTrace == True :
        plt.figure(0+count,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label = '$\epsilon_\\nu$ pour un void ratio de '+void_ratio)
        plt.grid(True)
        plt.xlabel("$\epsilon_{zz}$", fontsize = 18)
        plt.ylabel("$\epsilon_\\nu$", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.xlim(0,max(abs)*1.1)
        plt.title('Evolution of the deviatric strain as a function of the z-strain', fontsize =18)
        plt.savefig(chemin+'/resultat/'+'dev_strain.png')
        plt.close(0+count)

    """
    Résultat affiché dans sample/date_et_heure/multi_resultat

    Iic le numéro de la figure reste le meme entre chque boucle, cela permet de tracer plusieurs fois sur une meme figure

    On aurait peut etre pu utiliser les fonctions :

        1) pyplot.close() : ferme la figure et libère toutes les ressources liées à cette figure (à faire après sauvegarde de l'image dans un fichier, pas avant !)
        2) pyplot.clf() : efface la figure courante.
        3) pyplot.cla() : efface le graphe courant.

    Mais j'y ai pensé après et là ça marche donc bon a voir pour plus tard


    NB : j'ai ajouté les plt.close() au final car ca evite l'affichqge de warning
    """
    if optionMultiTrace == True :
        plt.figure(10,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label = '$\epsilon_\\nu$ pour un void ratio de '+void_ratio)
        plt.xlabel("$\epsilon_{zz}$", fontsize = 18)
        plt.ylabel("$\epsilon_\\nu$", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.xlim(0,max(abs)*1.1)
        plt.title('Evolution of the deviatric strain as a function of the z-strain', fontsize =18)
        plt.grid(True)
        if count == n-1 :
            plt.savefig(chemin_multi_trace+'/multi_resultat/'+'multi_dev_strain.png')
            plt.close(10)


"""
Fonction permttant de tracer automatiquement le deviatoric stress en fonction de epsilon ZZ
"""
def TraceDeviatoricStress(abs, ordo, void_ratio,chemin, chemin_multi_trace, Liste_couleur_trace, count, n, optionTrace, optionMultiTrace) :

    """
    La première figure est celle tracé dans le dossier sample/date_et_heure/void_ratio/resultat
    et ne contient que une courbe, celle du void ratio traité

    Tandis que la seconde est celle ou sont tracé toutes les courbes pour une meme granulométire PONDÉRÉE
    /!\ le mot pondéré est important car c'est la seule variable commune, les granulométrie n'étant pas exactement les mes dans notre cas actuel
    et se situe dans le dossier sample/date_et_heure/multi_resultat
    """
    if optionTrace == True :
        plt.figure(20+count,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='q pour un void ratio de '+ void_ratio)
        plt.grid(True)
        plt.xlabel("$\epsilon_{zz}$", fontsize = 18)
        plt.ylabel("q (kPa)", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.xlim(0,max(abs)*1.1)
        plt.title('Evolution of the deviatric stress as a function of the z-strain', fontsize =18)
        plt.savefig(chemin+'/resultat/'+'dev_stress.png')
        plt.close(20+count)

    """
    Résultat affiché dans sample/date_et_heure/multi_resultat
    """
    if optionMultiTrace == True :
        plt.figure(30,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='q pour un void ratio de '+ void_ratio)
        plt.grid(True)
        plt.xlabel("$\epsilon_{zz}$", fontsize = 18)
        plt.ylabel("q (kPa)", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.xlim(0,max(abs)*1.1)
        plt.title('Evolution of the deviatric stress as a function of the z-strain', fontsize =18)
        if count == n-1 :
            plt.savefig(chemin_multi_trace+'/multi_resultat/'+'multi_dev_stress.png')
            plt.close(30)



"""
Cette focntion permet simplement de recuperer la liste des rayons des particules
triées, une autre ponérée par l rayon minimim, du coup le rayon minimum
etc... va servir pour le tracer de l'ensemble des courbes granulométiques possibles

input : string : chemin --> chemin menant au fichier de resultat à lire (i;e sample/date_et_heure/void_ratio)

output :
"""
def AnalyseGranulometrique(chemin) :
    """
    Ici on selectione le ficheir sauvegardé au moment de la sauvegarde du sample
    """
    liste_fichier = os.listdir(chemin)
    nom_a_comparer = 'Sample_State_'
    extension_a_comparer = '.py'
    for i in range(0,len(liste_fichier)) :
        if liste_fichier[i][0:len(nom_a_comparer)] == nom_a_comparer and os.path.splitext(liste_fichier[i])[1] == extension_a_comparer :
            exec(open(chemin+'/'+liste_fichier[i]).read(),globals())


    """
    On a pris soins d'ouvrir le fichier python et maintenat on va faire quelques calculs sur les rayons des grains pour le stracer
    """
    grains['rad'].sort()
    liste_ordon =[]
    liste_abs   =[]
    sum_rayon = 0
    r_mean=0

    for i in range(0,len(grains['rad'])) :
        liste_ordon.append(i*100/len(grains['rad']))
        sum_rayon +=grains['rad'][i]
    r_mean = sum_rayon/len(grains['rad'])

    for i in range(0,len(grains['rad'])) :
        liste_abs.append(grains['rad'][i]/r_mean)

    return r_mean, grains, liste_abs, liste_ordon

def TraceCourbeGranulometric(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n, optionTrace, optionMultiTrace) :

    if optionTrace == True :
        plt.figure(40+count,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+ void_ratio)
        plt.grid(True)
        plt.xlabel("r(m)", fontsize = 18)
        plt.ylabel("%", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.ylim(0,100)
        plt.title('Courbe granulometrique', fontsize =18)
        plt.savefig(chemin+'/resultat/'+'granulo.png')
        plt.close(40+count)

    if optionMultiTrace == True :
        plt.figure(50,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+ void_ratio)
        plt.grid(True)
        plt.xlabel("r(m)", fontsize = 18)
        plt.ylabel("%", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.ylim(0,100)
        plt.title('Courbe granulometrique', fontsize =18)
        if count == n-1 :
            plt.savefig(chemin_multi_trace+'/multi_resultat/'+'multi_granulo.png')
            plt.close(50)

def TraceCourbeGranulometricPondere(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n, optionTrace, optionMultiTrace) :
    if optionTrace == True :
        plt.figure(60+count,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+void_ratio)
        plt.grid(True)
        plt.xlabel("$\dfrac{r}{r_{mean}}$", fontsize = 18)
        plt.ylabel("%", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.ylim(0,100)
        plt.title('Courbe granulometrique pondérée par $r_{mean}$', fontsize =18)
        plt.savefig(chemin+'/resultat/'+'granulo_pondere_r_mean.png')
        plt.close(60+count)

    if optionMultiTrace == True :
        plt.figure(70,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+void_ratio)
        plt.grid(True)
        plt.xlabel("$\dfrac{r}{r_{mean}}$", fontsize = 18)
        plt.ylabel("%", fontsize = 18)
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.ylim(0,100)
        plt.title('Courbe granulometrique pondérée par $r_{mean}$', fontsize =18)
        if count == n-1 :
            plt.savefig(chemin_multi_trace+'/multi_resultat/'+'multi_granulo_pondere_r_mean.png')
            plt.close(70)

def TraceCourbeGranulometricEchelleLog(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n, optionTrace, optionMultiTrace) :

    if optionTrace == True :
        plt.figure(80+count,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+ void_ratio)
        plt.grid(True,which="both")
        plt.xlabel("r(m)", fontsize = 18)
        plt.ylabel("%", fontsize = 18)
        plt.xscale("log")
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.xlim(min(abs)/10,max(abs)*10)
        plt.ylim(0,100)
        plt.title('Courbe granulometrique', fontsize =18)
        plt.savefig(chemin+'/resultat/'+'granulo_echelle_log.png')
        plt.close(80+count)

    if optionMultiTrace == True :
        plt.figure(90,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+ void_ratio)
        plt.grid(True,which="both")
        plt.xlabel("r(m)", fontsize = 18)
        plt.ylabel("%", fontsize = 18)
        plt.xscale("log")
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.legend(prop={'size':14})
        plt.xlim(min(abs)/10,max(abs)*10)
        plt.ylim(0,100)
        plt.title('Courbe granulometrique', fontsize =18)
        if count == n-1 :
            plt.savefig(chemin_multi_trace+'/multi_resultat/'+'multi_granulo_echelle_log.png')
            plt.close(90)

def TraceCourbeGranulometricPondereEchelleLog(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n, optionTrace, optionMultiTrace) :
    if optionTrace == True :
        plt.figure(100+count,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+void_ratio)
        plt.grid(True,which="both")
        plt.xlabel("$\dfrac{r}{r_{mean}}$", fontsize = 18)
        plt.xscale('log')
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.ylabel("%", fontsize = 18)
        plt.legend(prop={'size':14})
        plt.xlim(min(abs)/10,max(abs)*10)
        plt.ylim(0,100)
        plt.title('Courbe granulometrique pondérée par $r_{mean}$', fontsize =18)
        plt.savefig(chemin+'/resultat/'+'granulo_pondere_r_mean_echelle_log.png')
        plt.close(100+count)

    if optionMultiTrace == True :
        plt.figure(110,figsize=(14, 8), dpi=80)
        plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+void_ratio)
        plt.grid(True,which="both")
        plt.xlabel("$\dfrac{r}{r_{mean}}$", fontsize = 18)
        plt.xscale('log')
        plt.gca().xaxis.set_tick_params(labelsize = 12)
        plt.gca().yaxis.set_tick_params(labelsize = 12)
        plt.ylabel("%", fontsize = 18)
        plt.legend(prop={'size':14})
        plt.xlim(min(abs)/10,max(abs)*10)
        plt.ylim(0,100)
        plt.title('Courbe granulometrique pondérée par $r_{mean}$', fontsize =18)
        if count == n-1 :
            plt.savefig(chemin_multi_trace+'/multi_resultat/'+'multi_granulo_pondere_r_mean_echelle_log.png')
            plt.close(110)
