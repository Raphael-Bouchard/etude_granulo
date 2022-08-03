from post_traitement_function import *

#####################################
#Fin des fonctions
#####################################


#chemin d'accès aux fichiers résultats
"""
On récupère les arguments supplémentaires donnés au moment du lancment du
post traitement dans main.py
"""

Liste_chemin_sample, Liste_nom_fichiers, Liste_void_ratio =MiseEnPlacePostTraitement(sys.argv[1])
chemin_multi_trace = Liste_chemin_sample[0][0:Liste_chemin_sample[0].rfind('/')]
Liste_couleur_trace = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
Liste_forme_trace   =  ['-', '*', '^', 'x', '+', '.']
count = 0
"""
Cette boucle vise a tracer tous les graphs individuels, ie dans chque void ratio
"""
for i in range(0,len(Liste_chemin_sample)) :


    if not os.path.exists(Liste_chemin_sample[i]+'/post_traitement') :
        os.mkdir(Liste_chemin_sample[i]+'/post_traitement')
    if not os.path.exists(chemin_multi_trace+'/multi_post_traitement') :
        os.mkdir(chemin_multi_trace+'/multi_post_traitement')

    """
    info_list_parse() se situe dans le fichier post_traitement_function.py
    Il permet de lire l'ensemble d'un fichier textet et d'acrire sont contenu dans une grande matrice
    priori a ne pas modifier
    """
    matrice=info_list_parse(Liste_chemin_sample[i]+'/'+Liste_nom_fichiers[i])



    """
    getLineFromcolumn() se situe dans post_traitement_function.py
    Fonctionne en colaboration avec info_list_parse, car il lit les informations écrite
    dans la grosse matrice

    --> a modifier en focntion de ce qu'on souhaite recuperer dans le fichier de résultat
    Ici on recupere tout et on s'nemerde pas
    """
    line_time , line_iter ,line_epsilon_zz ,line_deviatoric_strain, line_name, line_deviatoric_stress = getLineFromcolumn(matrice)
    """
    Là on retravaille la forme de données pour avoir un beau graph
    et que ça soit plus silmple pour comparer avec les résultats de Antoine
    """
    for j in range (0, len(line_epsilon_zz)):
        line_epsilon_zz[j] *= -1
        line_deviatoric_stress[j] *=1./1000.



    """
    Bon ici on trace les graphs
    Je dois les ameliorer
    """

    TraceDeviatoricStrain(line_epsilon_zz, line_deviatoric_strain, Liste_void_ratio[i], Liste_chemin_sample[i], chemin_multi_trace, Liste_couleur_trace , count, len(Liste_void_ratio))

    TraceDeviatoricStress(line_epsilon_zz, line_deviatoric_stress, Liste_void_ratio[i], Liste_chemin_sample[i], chemin_multi_trace, Liste_couleur_trace , count, len(Liste_void_ratio))

    r_mean, grains, liste_rad_pondere, liste_pourcentage_rad_inf = AnalyseGranulometrique(Liste_chemin_sample[i])
    TraceCourbeGranulometric( grains['rad'], liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , count, len(Liste_void_ratio))
    TraceCourbeGranulometricPondere(liste_rad_pondere, liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , count, len(Liste_void_ratio))
    TraceCourbeGranulometricEchelleLog(grains['rad'], liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , count, len(Liste_void_ratio))
    TraceCourbeGranulometricPondereEchelleLog(liste_rad_pondere, liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , count, len(Liste_void_ratio))
    count +=1
