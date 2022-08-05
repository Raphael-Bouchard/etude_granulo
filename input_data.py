
############################
### Choix du simulateur ###
##########################
# grace a ce dictionnaire on va chosiir quelles simulations lancées
dictionnaire_simu={
# permet de crÉer les sample avec les informations données ci-avant
'creation_sample' : True,
# permet de savoir si l'on veut procéder à l'essaie trriaxial une fois que l'ensemble des sample aura ete créé
# faire attention à ca, si on met un void ratio impossible à atteindre dans la liste,
# le code de creation de sample tournera à l'infini
'essaie_triaxial' : True,
# encore une fois permet de savoir si l'onva lancer le post_traitement en automatique par la suite
'post_traitement' : True
}
"""
'creation_chemin', ci-dessous, est une Variable permettant de savoir si l'on veut
 créer un nouveau fichier de résulat
On  la passe False dans plusieurs situation :
1) on veut pas recréer de sample mais seulement faire l'essaie triaxial ou le post-traitement
2) on veut remplacer les samples de la dernière simulation (UNIQUEMENT LA DERNIERE)

PS : même si 'creation_chemin' = True, si 'creation_sample' = False
nous ne créerons pas de nouveau dossier car ça sert a rien
"""
creation_chemin = True
# chemin où seront ecrit les résultats de la creation des samples
chemin          = 'sample'
"""
Les options ci-dessous servent à gérer le sgraphs que l'on souhiate obtenir
Dans un soucis de limiter les donner, il vaut mieux mettre a True uniquement
OptionMultiTrace
"""
#Cette option permet de savoir si l'on veut les courbes individuelles
# i.e c'est à dire pour chque void ratio, les courbes associés
OptionTrace = True
# ici on choisit si l'on veut tracé les courbes sur un même graph
# pour les courbes issu de la mêmem simulation
OptionMultiTrace = True

#sert a savoir si l'on veut que les simu yade soient lancées par soient via la fentre
# permet de voir l'evolution du sample, mais quand on ets sur de la simulation
# on peut le laisser sur false
# True on voit les fentres
OptionFentreYade = False

################################################
### Propriété du matériaux utilisé du sample ###
################################################
# module d'young du materiau
young              = 356e6
poisson            = 0.42
density            = 3000
#permet de gerer les contrainte sinteners de notre materiau
frictAngle         = 30


########################################################
### Propriétés du nuage de particule de notre essaie ###
########################################################
# nombre de particule souhaité
num_spheres           = 10000
Rmean                 = 45*10**(-6)
#checker la notice de yade pour bien comprendre commenil marche celui ci
DispersionRadiusCoeff = 0.82
# va permettre de definir le volume de notre boite
dimCell               = [ 5*10**-3,  5*10**-3,  5*10**-3]


#######################################################################################
###        Parametre de la simulation triaxial pour la creation du sample           ###
### /!\ Ne pas toucher au hasard : lire NOTICE DE YADE TriaxialStressController /!\ ###
#######################################################################################
# etat de contrainte souhaite dans les trois direction (sigma0 CreatSample_yade.py et sigma1 CompressTriax_yade.py)
sigma0                    = -20*10**3
# permet de gérer si on fait grossir les particules ou bouger les murs
# a priori doit rester sur True
Input_InternalCompaction  = True
#Permet de gerer les stressMask --> TriaxialStressController() fonctionne en colab avec
# sigma0, strainSpeed et internal compaction
Input_StressMask          = 7


#######################################################################################
###        Parametre de la simulation triaxial pour le test triaxial                ###
### /!\ Ne pas toucher au hasard : lire NOTICE DE YADE TriaxialStressController /!\ ###
### Le stresmask est le même dans le dévut de chaque simulation donc c'est ok pr l'instant
#######################################################################################
sigma1              = -100*10**3
# vitesse de deplacement des murs dans certains cas : ici s'utilise dans CompressTriax_yade.py
strainSpeed         = -10
# objectif de compression triaxial
Strain_Z_Goal       = 0.2

# liste des obtectifs des void ratios
# une boucle dans le programme supprimera de la liste tous les void ratio inferrieu à 0.6
# si cette boucle devient chiante et qu'il faut l'enelver cela ce passe dans ver;py à la
# fonction GestionInputDonnes()
ListTargetVoidRatio   = [0.8,0.7,0.62]
