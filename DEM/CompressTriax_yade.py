
import os
import sys
import time
import numpy as np
from yade import pack


"""
 code lisant un fichier de donnée contenant le sample,
 que l'on compresse jusqu'a une valeur (noté ici sigma1). Quand cette valeur est
 atteinte on change alors la méthode de compression, pour ne plus bouger que
 le mur supérieur de l'axe z, jusqu'a atteindre un taux de de deformation prédéfini aussi

 Ce code est créé pour etre utilisé avec main.py
 Mais il peut etre lancé à la main pour cela voir la partie :
     ############################################
     ###   DEFINING VARIABLES AND MATERIALS   ###
     ############################################
     vers la ligne 250


  /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
  /!\ /!\ /!\ /!\ /!\ /!\   ORGANISATION DU CODE  /!\ /!\ /!\ /!\ /!\ /!\
  /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

 Ce code etant un code visant a gérer une simulation yade, son organisation est
 légerement différentes par rapport à un script standard


     1) en en tete les import
     2) les functions utiles au code
     3) les definitions des parametres physiques (materiaux) et geometrique (type de forme),
         ainsi que tous les parametres associés, utilisés lors de la simulation
         /!\ De plus, contient les explications pour lancer le code en utilisant le main. py ou à la mano
         /!\ De plus, l'appelle à certaines fonctions avant le debut de la simulation
         /!\ La partrie 4) de CeaSample_yade.py est ici contenue dans la fonction
             LectureFichiersDonnees()
     4) du coup y'en a pas vraiment (cf voir ligne juste au dessus)

     5) Parametrage de la compression (je dis ici compression parce que c'est le cas, mais dans le cadre d'une autre simu ca pourrait être autre chose)
     6) Parametrage de l'ensemble de la simu (gravité, type d'intrecation etc .....) --> variable O.engine() --> voir notice pour comprendre


     PS : chaque partie est séparée par une encadré du type :
                #########################################
                ###           NOM D'UNE PARTIE        ###
                #########################################
 """



############################################
###       DEFINITION DES FUNCTIONS       ###
############################################

"""
Lecture du dossier contenant les fichiers de de données et cration d'un dictionnaoire
qui a chaque extension associe la liste des fichier ayant cette meme extension
"""
def LectureFichiersDonnees(chemin, filename) :

    """
    Encore une fois on verifie le dernier element des noms des fichiers recupérers pour etre
    sûr qu'il n'y ait pas de probleme dans la gestion des fichiers
    """
    if chemin[-1] == '/' :
        chemin = chemin[:len(chemin)-1]

    """
    Ici on vérifie l'extension du fichier traité, pour savoir comment il doit etre importé
    Si c'est un '.yade.gz' on utilise la focniton interne de yade
    """
    if os.path.splitext(chemin+'/'+filename)[1] == '.gz' :
        # sert a donner le temps qu'il a fallut pour charger le fichier
        # ca serta rien mais c'est rigolo
        t0_LoadingData = time.time()
        # fontion interne de yade
        O.load(chemin+'/'+filename)
        tf_LoadingData = time.time() - t0_LoadingData
        print("Loading of",chemin+'/'+filename,"took (Python) : ", tf_LoadingData)
        # on range les ids des walls danss une liste speciale qui sera utile dans le parametrage de engine
        for i in range(6):
            wall_ids.append(O.bodies[i].id)


    """
    Si c'est un '.py' on utilise une fonction pour appeler les fichiers pythons (presque) comme dans main.py
    """
    if os.path.splitext(chemin+'/'+filename)[1] == '.py' :
        """
        A noter :
        exec() Parameters

        The exec() method takes three parameters:

            object - Either a string or a code object
            globals (optional) - a dictionary
            locals (optional) - a mapping object (commonly dictionary)

        PS : Il faut savoir que dans ce code et DEM/CreaSample_yade.py, on l'utilise comme telle
             Mais que dans CompressTriax_yade.py il est dans une boucle et on a du ajouter (1 fois)
             l'option globals() et je sias pas pourquoi
             A priori --> l'option local les transforme en variable locals
             A priori --> l'option global les transforme en variable globals
        """
        exec(open(chemin+'/'+filename).read(),globals())

        """
        On recré les matériaux ainsi que les objets à l'identiques
        """
        O.materials.append(FrictMat(young=young,poisson=poisson,frictionAngle=0,
                                    density=density,label='walls'))
        O.materials.append(FrictMat(young=young,poisson=poisson,
                                    frictionAngle=radians(frictAngle),
                                    density=density,label='spheres'))


        # NB : The walls were saved in the correct order to be correctly identified automatically in triax engine
        for i in range(6):
            O.bodies.append(utils.wall(walls['pos'][i],axis=walls['axis'][i],
                                       sense=walls['sense'][i],material='walls'))
            wall_ids.append(O.bodies[i].id)

        for i in range(len(grains['rad'])):
            pos=[grains['pos'][i][0],grains['pos'][i][1],grains['pos'][i][2]]
            O.bodies.append(utils.sphere(pos,grains['rad'][i],material='spheres'))

    #reset the friction angle
    setContactFriction(radians(frictAngle))


    return wall_ids



"""
Cette fonction permet de récupérer de nombreuses informations sur l'état de la simulation
et de les affihcer à l'écran
"""
def infoInitialState():
    nb, Min_r, Max_r, Min_X, Max_X, Min_Y, Max_Y, Min_Z, Max_Z, Volume= infoPositions()
    Volume_initial = Volume

    Initial_Void_ratio = porosity()/(1-porosity())
    dimCell = [Max_X - Min_X, Max_Y - Min_Y, Max_Z-Min_Z]
    StressTensor = getStress()

    """
    Formule classique pour obtenir le deviatoric stress
    """
    deviatoric_stress = StressTensor - (1.0/3.0)*Matrix3.trace(StressTensor)*Matrix3.Identity
    q_dev_stress = 0
    for i in range(0,2) :
        for j in range(0,2) :
            q_dev_stress = deviatoric_stress[i][j]* deviatoric_stress[j][i]
    q_dev_stress = sqrt((3.0*2.0)*q_dev_stress)

    print("")
    print("************************")
    print("Volume initial    : ", Volume_initial)
    print("iteration         : ", O.iter)
    print("q_dev_stress      : ", q_dev_stress)
    print('unbalanced force  : ',unbalancedForce())
    print("porosity          : ", porosity())
    print("Void ratio        : ", Initial_Void_ratio)
    print("")

    return Volume_initial, dimCell, Initial_Void_ratio






"""
Fonction permettant de sauvegarder les données necessaires pour le post traitement
au niveau des samples

Si cette fonction est modifiée, il ya de fortes chances que le code permettant le post traiotement ne fonctionne plus correctemnt ou plus du tout.
Ils doivent donc etre modifiés conjointement
"""
def Save_Data_to_Plot(chemin):
    global to_plot, Initial_Void_ratio
    Initial_Void_ratio = str('%0.2f'%(Initial_Void_ratio)).replace(".","_")
    f = open(chemin+'/'+"Data_to_Plot_VoidRatios"+Initial_Void_ratio+".dat", "a")
    f.truncate(0) # supprime tout ce qu'il ya en dessous de la ligne 0
    for i in range(0,len(to_plot["time"])) :
        f.write((str(to_plot["time"][i])+"\t"+str(to_plot["iter"][i])+"\t"+str(to_plot["epsilon_zz"][i])+"\t"+str(to_plot["volumetric_strain"][i])+"\t"+str(to_plot["deviatoric_stress"][i])+"\n"))
    f.close()



"""
Cette fonction sert a récupérer
- les positions des particules situées aux extremums des packages
- le nbre de particule
- les rayons min et max de particules
etc ...
/!\ Fonction legemrent modifier par rapport au fichier CreaSample_yade.py --> return le volume en plus
"""
def infoPositions() :

    # compte le nbre de particule
    nb = 0
    for b in O.bodies:
        if isinstance(b.shape,Sphere):
            #  b.state.blockedDOFs = 'zXY'
            nb=nb+1


    Min_r = min([b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])
    Max_r = max([b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])


    Max_X = max([b.state.pos[0] + b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])
    Min_X = min([b.state.pos[0] - b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])

    Max_Y = max([b.state.pos[1] + b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])
    Min_Y = min([b.state.pos[1] - b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])

    Max_Z = max([b.state.pos[2] + b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])
    Min_Z = min([b.state.pos[2] - b.shape.radius for b in O.bodies if isinstance(b.shape, Sphere)])
    print("")
    print("The number of particles is ", nb)
    print("The smallest particle is "  , Min_r)
    print("The biggest particle is"    , Max_r)
    print("There is a factor", Max_r/Min_r, "between the max and the min radius")
    Volume = (abs(Max_X)-abs(Min_X))*(abs(Max_Y)-abs(Min_Y))*(abs(Max_Z)-abs(Min_Z))
    print("Le volume de notre boite est de ", (abs(Max_X)-abs(Min_X))*(abs(Max_Y)-abs(Min_Y))*(abs(Max_Z)-abs(Min_Z))," mètres cubes")
    #print("The critical Time step is"  , PWaveTimeStep())
    return nb ,Min_r, Max_r, Min_X, Max_X, Min_Y, Max_Y, Min_Z, Max_Z, Volume

"""
Fonction permettant le calcul de nbreuxx parametre et leur affichage dans le terminal
de plus on ajoites les elements dans les listes pour le post traitement ici
"""
def InfoSimu() :
    """
    Fonction servant a vérifier l'évolution des éléments de calculs ed notre simulation
    On y change aussi certains parametres de calculs en fonction de ce que l'on shouaite faire.
    """
    # Les lignes commentées ci-desosus provuennent d'n code de antoine,
    # je dois lui demander à quoi ça correspond
    # Ne pas toucher au cas ou
    """
    Critere de tresca
    """
    # print(" verification variable antoine ")
    # q=triax.stress(triax.wall_back_id)[2]-triax.stress(triax.wall_left_id)[0]
    # p=(triax.stress(triax.wall_left_id)[0]+\
    #        triax.stress(triax.wall_bottom_id)[1]+\
    #        triax.stress(triax.wall_back_id)[2])/3
    # eta=q/p
    # print(" q   = ", q)
    # print(" p   = ", p)
    # print(" eta = ", eta )




    unb=unbalancedForce()

    """
    renvoie un scalaire, qui est la contrainte moyenne
    """
    meanStress=triax.meanStress

    """
    triax.stress
    ceci est un pointeur, on doit lui donner une coposante [i] pour avoir sa valeur. Renvoie un
    renvoie le vecteur contrainte tau associé à la normale sortante de notre mur
    tau = sigma.n
    c'est pour ça que c'est un vecteur de trois coomposantes
    De plus, cela correspond aux contraintes sur les faces et non pas uax contraintes interne
    c'est pourquoi les résultats obtenus avec getStress() diffèrent légérement
    """
    stress = triax.stress

    """
    strain = triax.strain
    Renvoie le vecteur taux de deformation de la simulation triaxial
    renvoie un vecteur car nous sommes en triaxial et il ne peut donc pas y avoir de deformation non normale aux murs
    """
    strain = triax.strain

    """
    getStress()
    Fonction renvoyant le tenseur des contraintes selon la formule de Love-webber
    du cube de simulation
    """
    StressTensor = getStress()


    """
    Formule classique pour obtenir le deviatoric stress : von mises
    """
    deviatoric_stress = StressTensor - (1.0/3.0)*Matrix3.trace(StressTensor)*Matrix3.Identity
    q_dev_stress = 0
    for i in range(0,2) :
        for j in range(0,2) :
            q_dev_stress = deviatoric_stress[i][j]* deviatoric_stress[j][i]
    q_dev_stress = sqrt((3.0*2.0)*q_dev_stress)

    void_ratio =  porosity()/(1-porosity())
    print("************************")
    print("iteration         : ", O.iter)
    print("strainRate        : ", triax.strainRate)
    print("q_dev_stress      : ", q_dev_stress)
    print('unbalanced force  : ',unb)
    print('mean stress       : ',meanStress)
    print("strain  zz        : ", strain[2])
    print("Volumetric strain : ", triax.volumetricStrain)
    print("porosity          : ", porosity())
    print("Void ratio        : ", void_ratio)
    print("")


    to_plot["time"].append(O.time)
    to_plot["epsilon_zz"].append(triax.strain[2])
    to_plot["volumetric_strain"].append(triax.volumetricStrain)
    to_plot["iter"].append(O.iter)
    to_plot["deviatoric_stress"].append(q_dev_stress)


"""
Ici on créé deux dictionnaires : grains{} et walls{}
Et on va remplir ces deux dictionnaires avec les informations suivantes :
- grains : positions et rayons
- walls  : positions, axes et sens
Puis on écrit ces deux dictionnaires dnas un fichier .py
On s'en servira surtout pour l'étude granulométrique

De plus on utilise aussi la sauvegarde interne
"""
def saveSampleCompressedPy(chemin,meanStress,debut_nom_fichier):

    """
    On formate certaines informations pour les incorporer dans le nom des fichiers
    --> passage en string --> conservation que des premiers chiffres --> emplace les '.' par des '_'
    """
    meanStress = str('%0.2f'%(int(abs(meanStress)/1000))).replace('.','_')

    """
    Utilisation de la fonction interne de sauvegarde
    """
    O.save(chemin+'/'+debut_nom_fichier+meanStress+'kPa.yade.gz')

    """
    Creation et remplissage des dictionnaires qui seront ecris dans le fichier '.py'
    """
    grains={'pos':[],'rad':[]}
    walls={'pos':[],'axis':[],'sense':[]}

    for b in O.bodies:
        if isinstance(b.shape,Wall):
            walls['axis']+=[b.shape.axis]
            walls['sense']+=[b.shape.sense]
            walls['pos']+=[b.state.pos[b.shape.axis]]
        else :
            pos=(b.state.pos[0],b.state.pos[1],b.state.pos[2])
            grains['pos']+=[pos]
            grains['rad']+=[b.shape.radius]

    """
    Ecriture dans le fichier '.py'
    """
    with open(chemin+'/'+debut_nom_fichier+meanStress+'kPa.py','w') as f:
        f.write('# Position and radius of the grains in the initial configuration.\n')
        f.write('grains='+repr(grains)+'\n')
        f.write('walls='+repr(walls)+'\n')
        f.write("print('Dictionnaries grains and walls loaded.')\n")

    """
    Message d'information sur la simulation qui seront imprim ecran
    """
    print("")
    print ("\n ###    compressed state saved      ###")
    print("Le nom du fichier est : ",debut_nom_fichier+meanStress+"kPa.yade.gz'")
    print(" et se situe dans le dossier :", chemin)
    nb ,Min_r, Max_r, Min_X, Max_X, Min_Y, Max_Y, Min_Z, Max_Z, Volume =infoPositions()
    """
    ici on imprime ecran de nombreses informations  permettant de comparer avec le compactage que nous verrons apres
    """

    print("************************")
    print("iteration        : ", O.iter)
    print('unbalanced force : ',unbalancedForce())
    print('mean stress      : ',meanStress)
    print("porosity         : ", porosity())
    print("Void ratio       : ", porosity()/(1-porosity()))
    print("")


"""
Fonction contenant les parametres d'analyse de la simulation et de son évolution
"""

def checkConvergence(chemin):
    """
    Fonction servant a vérifier l'évolution des éléments de calculs ed notre simulation
    On y change aussi certains parametres de calculs en fonction de ce que l'on shouaite faire.
    """

    test = abs((triax.meanStress-sigma1)/sigma1)<0.01 or abs(triax.meanStress)>=abs(sigma1)
    # vérifie le compatcatge jusqua la valeur souhaité
    if triax.stressMask ==7 and test ==True :

        # si nous avons atteint le compactage souhaité on modifie les parametre de TrixStressControler
        #pour compresser uniquement selon l'axe z
        print("")
        print("nous avons un sample compressé a 100 kPa, on va commencer la compression selon l'axe z")
        saveSampleCompressedPy(chemin,triax.meanStress,'Compressed_State_')
        print('')
        triax.stressMask = 3
        # triax.strainRate = (0,0,-0.01)
        triax.goal1 = sigma1
        triax.goal2 = sigma1
        triax.goal3 = strainSpeed
        #triax.strainRate = Vector3(0,0,-0.01)

        # ici on verifie si on a atteint l'objectif de comprssion selon l'axe des z
    elif triax.stressMask == 3 and abs(triax.strain[2])>=Strain_Z_Goal :

        print("La simulation pour le fichier",chemin+'/'+filename,"est terminée")
        print("")
        Save_Data_to_Plot(chemin)
        saveSampleCompressedPy(chemin,triax.meanStress,'Finale_deformation_')
        O.pause()





############################################
###   DEFINING VARIABLES AND MATERIALS   ###
############################################
strainSpeed=-100
sigma1=-100*10**3
Input_StressMask = 7
young=356e6
poisson=0.42
frictAngle=30
density=3000
damp=0.8
wall_ids=[]
Strain_Z_Goal = 0.2


"""
Si vous lancer le script sans le main.py :
    1) Commenter les deux lignes ci-dessous :
        exec(open('input_data.py').read())
        chemin   = sys.argv[1]
        filename = sys.argv[2]

    2) Decommenter la troisieme ligne (et mettez les informations necessaires) :
        chemin   = ""
        filename = ""

Faire exactement l'inverse pour le lancer depuis le main.py
NB : Si vous lancer le script sans le main.py, la gestion des fichiers de resultats
sera différentes --> voir fonction checkConvergence()
Il faura donc lancer les scripts suivant (essaie triaxial et post traitement)
 à la main aussi ! ou alors bien gérer les fichiers de résultats
"""
exec(open('input_data.py').read())
chemin = sys.argv[1]
filename = sys.argv[2]
# chemin = 'sample/2022-07-27_17_53/0_7'
# filename = 'compactedState_10.00kPa_voidRatio_0.70.py'


"""
Ici on recuperes la liste des id des wall, cela va servir dans la definition
de l'essaie triaxial
PLus les deux fonctiosn permettre d'imprim ecran certaines informations
"""
wall_ids = LectureFichiersDonnees(chemin, filename)
Volume_initial, dimCell, Initial_Void_ratio = infoInitialState()



"""
Va servir pour le post traitement
"""
to_plot = {"time" : ["time(s)"], "iter" : ["iter"], "epsilon_zz" : ["epsilon_zz"], "volumetric_strain" : ["volumetric_strain"], "deviatoric_stress" : ["deviatoric_stress"]}



#########################################
### Parametrisation de la compression ###
#########################################

triax= TriaxialStressController(label='triax',
                height0=dimCell[1],width0=dimCell[0],depth0=dimCell[2],
                wall_left_id=wall_ids[0],wall_right_id=wall_ids[1],
                wall_bottom_id=wall_ids[2],wall_top_id=wall_ids[3],
                wall_back_id=wall_ids[4],wall_front_id=wall_ids[5],
                # Isotropic initial compression
                stressMask=Input_StressMask,
                goal1=sigma1,
                goal2=sigma1,
                goal3=sigma1,
                #le parametre dessous mis en true indique une augmentaion du rayon des particules, tandis
                # que si il est false, on bouge les murs
                internalCompaction=False,
                # Comment if internalCompaction=True
                #strainRate = (0,0,-0.01),
                #max_vel=1,
				stressDamping=0.25,
				strainDamping=0.8,
                # Uncomment if internalCompaction=True
                # maxMultiplier=1.01,
                # finalMaxMultiplier=1.001
                )


# definition du pas de temps
O.dt=0.95*utils.PWaveTimeStep()



#########################################
###              ENGINES              ###
#########################################

O.engines=[
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Wall_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(),        # collision geometry
		Ig2_Wall_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_FrictPhys()], # collision "physics"
		[Law2_ScGeom_FrictPhys_CundallStrack()]   # contact law -- apply forces
	),
	triax,
    PyRunner(command='InfoSimu()', iterPeriod = 1000, label = 'InfoSimu'),
	PyRunner(command='checkConvergence(chemin)', iterPeriod = 1000, label = 'checkConvergence'),
	#VTKRecorder(iterPeriod=int(sys.argv[1]),recorders=['spheres', 'facets'],fileName='/mnt/DATA/nyounes/0g/DEM-LBM/TEST_LOTSPARTICLES/computation/YADE-'),
	#VTKRecorder(iterPeriod=2000,recorders=['spheres', 'boxes'],fileName='Results_YADE/YADE-'),
	# PyRunner(command='Check_Displacement()',iterPeriod=1, label = 'checker'),
	# PyRunner(command='Save_Stresses()',iterPeriod= 1000, label = 'Save_Stresses'),#int(sys.argv[1]), label = 'Save_Stresses'),
	# PyRunner(command='Check_Positions()',iterPeriod = 1000, label = 'Positions'),#int(sys.argv[1]), label = 'Positions'),
	# Apply gravity force to particles. damping: numerical dissipation of energy.
	NewtonIntegrator(gravity=(0.0,0.0,9.81),damping=0.2)
		  ]


"""
Le premier argument de O.run() est tres grand
mais il permet juste d'avoir un exit() en dessous
"""
O.run(200000000,True)
exit()
