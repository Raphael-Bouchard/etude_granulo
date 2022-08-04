#On def la porosité comme : P =  (V -Vshpere)/V
#Alors que le void ratio est def (a priori) comme e = P /(1-P) = (V-Vsphere)/Vsphere
#On utilise le void ratio comme parametre de creation de sample
#PS : dans la liste ListTargetVoidRatio, les void ratio doivent tjs etres mis par ordre décroissant

################################################
### Propriété du matériaux utilisé du sample ###
################################################
# module d'youn du materiau
young              = 356e6
poisson            = 0.42
#permet de gerer les contrainte sinteners de notre materiau
frictAngle         = 30
density            = 3000

##############################################
### Propriétés geometrique de notre essaie ###
##############################################
# nombre de particule souhaité
num_spheres           = 10000

# liste des obtectifs des void ratios
# une boucle dans le programme supprimera de la liste tous les void ratio inferrieu à 0.6
ListTargetVoidRatio   = [1.0,0.7,0.8,0.9,0.4,0.6,0.5]

# va permettre de definir le volume de notre bioite
dimCell = [ 5*10**-3,  5*10**-3,  5*10**-3]



# chemin où seront ecrit les résultats de la creation des samples
chemin = 'sample'

"""
Variable permettant de svaoir si l'on veut créer un nouveau fichier de résulat
On  la passe False dans plusieurs situation :
1) on veut pas recréer de sample mais seulement faire l'essaie triaxial ou le post-traitement
2) on veut remplacer les samples de la dernière simulation
"""
creation_chemin = False

#Parametre de la simulation triaxial
#######################################################################################
### /!\ Ne pas toucher au hasard : lire NOTICE DE YADE TriaxialStressController /!\ ###
#######################################################################################
sigma0 = -20*10**3
damp = 0.8


# permet d'inqieur si l'on veut que les simulation s'enchaine ou nan
#####################################################################################
### /!\ il est quand meme conseiller de lancer les simu une par une au cas ou /!\ ###
#####################################################################################
dictionnaire_simu={
# permet de crer les sample avec les informations données ci-avant
'creation_sample' : False,
# permet de savoir si l'on veut procéder à l'essaie trriaxial une fois que l'ensemble des sample aura ete créé
# faire attention à ca, si on met un void ratio impossible à atteindre dans la liste,
# le code de creation de sample tournera à l'infini
'essaie_triaxial' : True,

# encore une fois permet de savoir si l'onva lancer le post_traitement en automatique par la suite
'post_traitement' : False
}
