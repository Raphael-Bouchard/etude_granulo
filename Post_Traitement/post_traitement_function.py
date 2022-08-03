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
output : Liste[L1[], L2[], etc ... ] --> peut etre vu comme une matrice car chaque liste
        contient chque information de la matrice ainsi l'élement
        matrice[i][j] correspond à Lj[i] --> element i de la liste j
                                         --> element i de la jeme colonne du fochier de resultat
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
def MiseEnPlacePostTraitement(name) :
    Liste_chemin_sample =[]
    Liste_nom_fichiers  =[]
    Liste_void_ratio    =[]
    test=False

    while test == False :
        Liste_nom_fichiers += [name[0:name.find('%')]]
        if name.find('%')+1 == len(name) :
            test = True
        else :
            name = name[name.find('%')+1:]



    for i in range(0,len(Liste_nom_fichiers)) :
        Liste_chemin_sample +=[Liste_nom_fichiers[i][:Liste_nom_fichiers[i].rfind('/')]]
        Liste_nom_fichiers[i]= Liste_nom_fichiers[i][Liste_nom_fichiers[i].rfind('/')+1:]
        Liste_void_ratio += [Liste_chemin_sample[i][Liste_chemin_sample[i].rfind('/')+1:].replace('_','.')]
    return Liste_chemin_sample, Liste_nom_fichiers, Liste_void_ratio



"""
Fonction permttant de tracer automatiquement le deviatoric strain en fonction de epsilon ZZ
"""
def TraceDeviatoricStrain(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n) :

    """
    La première figure est celle tracé dans le dossier sampel/date_et_heure/void_ratio/post_traitement

    Tandis que la seconde est celle ou sont tracé toutes les courbes pour une meme granulométire PONDÉRÉE
    /!\ le mot pondéré est important car c'est la seule variable commune, les granulométrie n'étant pas exactement les mes dans notre cas actuel
    """
    plt.figure(0+count,figsize=(14, 8), dpi=80)
    plt.plot(abs[:],ordo[:],color='g',label = '$\epsilon_\\nu$ pour un void ratio de '+void_ratio)
    plt.grid(True)
    plt.xlabel("$\epsilon_{zz}$", fontsize = 18)
    plt.ylabel("$\epsilon_\\nu$", fontsize = 18)
    plt.gca().xaxis.set_tick_params(labelsize = 12)
    plt.gca().yaxis.set_tick_params(labelsize = 12)
    plt.legend(prop={'size':14})
    plt.xlim(0,max(abs)*1.1)
    plt.title('Evolution of the deviatric strain as a function of the z-strain', fontsize =18)
    plt.savefig(chemin+'/post_traitement/'+'dev_strain.png')

    """
    Résultat affiché dans sample/date_et_heure/multi_post_traitement
    """
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
        plt.savefig(chemin_multi_trace+'/multi_post_traitement/'+'multi_dev_strain.png')


"""
Fonction permttant de tracer automatiquement le deviatoric stress en fonction de epsilon ZZ
"""
def TraceDeviatoricStress(abs, ordo, void_ratio,chemin, chemin_multi_trace, Liste_couleur_trace, count, n) :


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
    plt.savefig(chemin+'/post_traitement/'+'dev_stress.png')

    """
    Résultat affiché dans sample/date_et_heure/multi_post_traitement
    """
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
        plt.savefig(chemin_multi_trace+'/multi_post_traitement/'+'multi_dev_stress.png')



"""
Cette focntion permet simplement de recuperer la liste des rayons des particules
triées, une autre ponérée par l rayon minimim, du coup le rayon minimum
etc... va servir pour le tracer de l'ensemble des courbes granulométiques possibles
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
    r_mean    = sum_rayon/len(grains['rad'])

    for i in range(0,len(grains['rad'])) :
        liste_abs.append(grains['rad'][i]/r_mean)

    return r_mean, grains, liste_abs, liste_ordon

def TraceCourbeGranulometric(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n) :

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
    plt.savefig(chemin+'/post_traitement/'+'granulo.png')

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
        plt.savefig(chemin_multi_trace+'/multi_post_traitement/'+'multi_granulo.png')

def TraceCourbeGranulometricPondere(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n) :

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
    plt.savefig(chemin+'/post_traitement/'+'granulo_pondere_r_mean.png')


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
        plt.savefig(chemin_multi_trace+'/multi_post_traitement/'+'multi_granulo_pondere_r_mean.png')

def TraceCourbeGranulometricEchelleLog(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n) :

    plt.figure(80+count,figsize=(14, 8), dpi=80)
    plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+ void_ratio)
    plt.grid(True)
    plt.xlabel("r(m)", fontsize = 18)
    plt.ylabel("%", fontsize = 18)
    plt.xscale("log")
    plt.gca().xaxis.set_tick_params(labelsize = 12)
    plt.gca().yaxis.set_tick_params(labelsize = 12)
    plt.legend(prop={'size':14})
    plt.xlim(min(abs)/10,max(abs)*10)
    plt.ylim(0,100)
    plt.title('Courbe granulometrique', fontsize =18)
    plt.savefig(chemin+'/post_traitement/'+'granulo_echelle_log.png')


    plt.figure(90,figsize=(14, 8), dpi=80)
    plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+ void_ratio)
    plt.grid(True)
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
        plt.savefig(chemin_multi_trace+'/multi_post_traitement/'+'multi_granulo_echelle_log.png')

def TraceCourbeGranulometricPondereEchelleLog(abs, ordo, void_ratio, chemin, chemin_multi_trace, Liste_couleur_trace, count, n) :

    plt.figure(100+count,figsize=(14, 8), dpi=80)
    plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+void_ratio)
    plt.grid(True)
    plt.xlabel("$\dfrac{r}{r_{mean}}$", fontsize = 18)
    plt.xscale('log')
    plt.gca().xaxis.set_tick_params(labelsize = 12)
    plt.gca().yaxis.set_tick_params(labelsize = 12)
    plt.ylabel("%", fontsize = 18)
    plt.legend(prop={'size':14})
    plt.xlim(min(abs)/10,max(abs)*10)
    plt.ylim(0,100)
    plt.title('Courbe granulometrique pondérée par $r_{mean}$', fontsize =18)
    plt.savefig(chemin+'/post_traitement/'+'granulo_pondere_r_mean_echelle_log.png')

    plt.figure(100+count,figsize=(14, 8), dpi=80)
    plt.plot(abs[:],ordo[:],color=Liste_couleur_trace[count],label ='void ratio de '+void_ratio)
    plt.grid(True)
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
        plt.savefig(chemin_multi_trace+'/multi_post_traitement/'+'multi_granulo_pondere_r_mean_echelle_log.png')
