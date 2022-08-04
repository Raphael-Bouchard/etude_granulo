from post_traitement_function import *

#####################################
#Fin des fonctions
#####################################


#chemin d'accès aux fichiers résultats
"""
Cette fonction permet de récuéperer toutes les informations utiles
au post traitement
"""
OptionTrace, OptionMultiTrace, chemin_multi_trace, Liste_chemin_sample, Liste_nom_fichiers, Liste_void_ratio = MiseEnPlacePostTraitement(sys.argv[1], sys.argv[2])


Liste_couleur_trace = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
Liste_forme_trace   =  ['-', '*', '^', 'x', '+', '.']


"""
Cette boucle vise a tracer tous les graphs individuels, ie dans chque void ratio
"""
for i in range(0,len(Liste_chemin_sample)) :

    if OptionTrace == False and OptionMultiTrace == False :
        exit("""Les options : 'OptionsTrace' et 'OptionMultiTrace'
Situées dans le fichier input_data.py sont toutes les deux à False
Il faut en mettre au moins une sur True pour qu'il y ait un post traitement

Le code est donc stoppé """)

    if not os.path.exists(Liste_chemin_sample[i]+'/resultat') :
        os.mkdir(Liste_chemin_sample[i]+'/resultat')
    if not os.path.exists(chemin_multi_trace+'/multi_resultat') :
        os.mkdir(chemin_multi_trace+'/multi_resultat')

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
    Récuperations de certaines données à trracer ans le fichier Data_to_plot traité
    Détail de la function dan sle fichier post_traitement_function.py
    """
    r_mean, grains, liste_rad_pondere, liste_pourcentage_rad_inf = AnalyseGranulometrique(Liste_chemin_sample[i])

    """
    Les fonctions ci-dessous servent à tracer différentes courbes
    Le choix de courbe individuel ou multiple est fait dans les fonctions
    """
    TraceDeviatoricStrain(line_epsilon_zz, line_deviatoric_strain, Liste_void_ratio[i], Liste_chemin_sample[i], chemin_multi_trace, Liste_couleur_trace , i, len(Liste_void_ratio), OptionTrace, OptionMultiTrace)
    TraceDeviatoricStress(line_epsilon_zz, line_deviatoric_stress, Liste_void_ratio[i], Liste_chemin_sample[i], chemin_multi_trace, Liste_couleur_trace , i, len(Liste_void_ratio), OptionTrace, OptionMultiTrace)
    TraceCourbeGranulometric( grains['rad'], liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , i, len(Liste_void_ratio), OptionTrace, OptionMultiTrace)
    TraceCourbeGranulometricPondere(liste_rad_pondere, liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , i, len(Liste_void_ratio), OptionTrace, OptionMultiTrace)
    TraceCourbeGranulometricEchelleLog(grains['rad'], liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , i, len(Liste_void_ratio), OptionTrace, OptionMultiTrace)
    TraceCourbeGranulometricPondereEchelleLog(liste_rad_pondere, liste_pourcentage_rad_inf,Liste_void_ratio[i], Liste_chemin_sample[i] ,chemin_multi_trace, Liste_couleur_trace , i, len(Liste_void_ratio), OptionTrace, OptionMultiTrace)

print("Tous les post-traitements ont été effectués")
