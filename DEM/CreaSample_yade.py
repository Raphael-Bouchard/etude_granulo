from yade import pack, plot
import os
import re
import sys
from datetime import datetime

"""
Ce code sert a générer plusieurs samples avec des void rato différents

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
    4) La creation des materiaux et des objets, via les parametres definis à l'étape précédente
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
Fonction permettant de gerer l'ensemble des données d'entrées
1) suppression des void ratio inf à 0.6
2) gestion du chemin
3) gestion du TargetVoidRatio
"""

def GestionInputDonnes(ListTargetVoidRatio,chemin) :

    """
    Ici on supprime de la liste des void ratios trop petit ne pas tourner infiniment
    """

    for i in range(len(ListTargetVoidRatio)-1) :
        if ListTargetVoidRatio[i]<0.6 :
            del ListTargetVoidRatio[i]
    ListTargetVoidRatio.sort(reverse=True)
    TargetVoidRatio =  ListTargetVoidRatio[0]

    # normalement ça a deja etait modifié donc ne sert a rien
    # mais on ne sait jmais
    if chemin[-1] == '/' :
        chemin = chemin[:len(chemin)-1]

    return TargetVoidRatio, ListTargetVoidRatio, chemin





"""
Cette fonction sert a récupérer
- les positions des particules situées aux extremums des pckages
- le nbre de particule
- les rayons min et max de particules
etc ...
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
    print("Le volume de notre boite est de ", (abs(Max_X)-abs(Min_X))*(abs(Max_Y)-abs(Min_Y))*(abs(Max_Z)-abs(Min_Z))," mètres cubes")
    print("")
    #print("The critical Time step is"  , PWaveTimeStep())
    return nb ,Min_r, Max_r, Min_X, Max_X, Min_Y, Max_Y, Min_Z, Max_Z




"""
Ici on créé deux dictionnaires : grains{} et walls{}
Et on va remplir ces deux dictionnaires avec les informations suivantes :
- grains : positions et rayons
- walls  : positions, axes et sens
Puis on écrit ces deux dictionnaires dnas un fichier .py
On s'en servira surtout pour l'étude granulométrique

De plus on utilise aussi la sauvegarde interne
"""
def saveSamplePy(chemin,meanStress, void_ratio,TargetVoidRatio):

    """
    On formate certaines informations pour les incorporer dans le nom des fichiers
    --> passage en string --> conservation que des premiers chiffres --> emplace les '.' par des '_'
    """
    void_ratio = str('%0.2f'%(void_ratio)).replace('.','_')
    meanStress = str('%0.2f'%(int(abs(meanStress)/1000))).replace('.','_')
    """
    Dans le dossier sample/date_et_heure, on va céer des dossier portant le nom du
    void ratio associé ( exple 0.6 , 0.7 etc ...)
    si le dossier existe deja on ne le créé pas
    """
    chemin += "/"+str(TargetVoidRatio).replace('.','_')
    if os.path.exists(chemin) == False:
        os.mkdir(chemin)

    """
    Utilisation de la fonction interne de sauvegarde
    """
    O.save(chemin+'/Sample_State_'+meanStress+'kPa_voidRatio_'+void_ratio+'.yade.gz')

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
    with open(chemin+'/Sample_State_'+meanStress+'kPa_voidRatio_'+void_ratio+'.py','w') as f:
        f.write('# Position and radius of the grains in the initial configuration.\n')
        f.write('grains='+repr(grains)+'\n')
        f.write('walls='+repr(walls)+'\n')
        f.write("print('Dictionnaries grains and walls loaded.')\n")

    """
    Message d'information sur la simulation qui seront imprim ecran
    """
    print("")
    print ("\n ###    sample state saved      ###")
    print("Le nom du fichier est :'Sample_State_"+meanStress+"kPa_voidRatio_"+void_ratio+".yade.gz'")
    print(" et se situe dans le dossier :", chemin)
    nb, Min_r, Max_r, Min_X, Max_X, Min_Y, Max_Y, Min_Z, Max_Z =infoPositions()
    """
    ici on imprime ecran de nombreses informations  permettant de comparer avec le compactage que nous verrons apres
    """

    print("************************")
    print("iteration        : ", O.iter)
    print('unbalanced force : ',unb)
    print('mean stress      : ',meanStress)
    print("porosity         : ", porosity())
    print("Void ratio       : ", void_ratio)
    print("")







"""
Permet de verifier de nombreux parametres lors de la création du sample
Permet aussi de changer les conditiosn de compressiosn si on le souahite etc..
fonction appele automatiquement au cours de la compression
"""

def checkConvergence(TargetVoidRatio, chemin):

    """
    Calcul de certains parametre
    """
    unb=unbalancedForce()
    meanStress=triax.meanStress
    void_ratio =  porosity()/(1-porosity())

    print('unbalanced force : ',unb,' mean stress : ',meanStress, "porosity : ", porosity(), "Void ratio : ", void_ratio)
    #if triax.stressMask==7:
    """
    A quoi sert exactement  le parametre stabilityThreshold??
    Il est comparé aux "unbalanced force" qui mesure en gros le degre de stabilité de notre stucture.
    Plus il sera statique, plus ce nbre tendra vers 0 même si il ne vaut jamais 0.
    une valeur de 1e-2 est une bonne valeur de stabilité, néanmoins cela dépend de chaque cas d'étude.
    """
    #test=unb<stabilityThreshold and abs((meanStress-sigma0)/sigma0)<0.01

    """
    L'objectif étant d'obtenir un certain void ratio, les lignes ci-dessous permet
    d'avoir l'obtectif de void ratio en condition prioritaire sur le taux de compression
    """
    test = abs((meanStress-sigma0)/sigma0)<0.01 or abs(meanStress)>=abs(sigma0)
    if void_ratio<=TargetVoidRatio :
        test = True

    """
    La diminution de l'angle de friction facilite le rearrangement des particles
    permettant ainsi d'obtenir des voids ratio plus aisément
    """
    if test==True and void_ratio>TargetVoidRatio:
        print("on diminue l'angle de friction")
        for b in O.bodies :
            if isinstance(b.shape,Sphere):
                b.material.frictionAngle *= 0.98



        """
        Si on est inf ou egale au void ratio cible, on sauvegarde le sample
        et on passe au void ratio suivant
        """
    elif test==True and void_ratio<=TargetVoidRatio:

        """
        Sauvegarde le sample en deux formats différents
        1) O.save --> fonction interne de yade au format '.yade.gz'
        2) fichier '.py' contenat des dictionnaires --> utiles pour post traitement
            et/ou remplacer les '.yade.gz' si corrompu
        """
        saveSamplePy(chemin,meanStress,void_ratio,TargetVoidRatio)

        """
        On passe au void ratio suivant
        """
        if TargetVoidRatio == ListTargetVoidRatio[-1] :
            O.pause()
        else :
            for i in range(0,len(ListTargetVoidRatio)) :
                if TargetVoidRatio == ListTargetVoidRatio[i] :
                    TargetVoidRatio = ListTargetVoidRatio[i+1]
                    print("Le nouveau void ratio est", TargetVoidRatio)
                    break








############################################
###   DEFINING VARIABLES AND MATERIALS   ###
############################################

"""
Parametre pour si l'on veut lancer la simu a la main et non avec main.py
"""

# parametre phsyique
young              = 356e6
poisson            = 0.42
frictAngle         = 30
density            = 3000
# parametre nuage de point
num_spheres        = 10000
Rmean              = 45*10**(-6)
DispersionRadiusCoeff = 0.82

dimCell = [ 5*10**-3,  5*10**-3,  5*10**-3]


#parametre de compression
sigma0 = -20*10**3
Input_InternalCompaction = True
Input_StressMask = 7
strainSpeed = 0
damp = 0.8
# liste des obtectifs des void ratios
# une boucle dans le programme supprimera de la liste tous les void ratio inferrieu à 0.6
ListTargetVoidRatio   = [1.5,1.0,0.7,0.8,0.9,0.4,0.6,0.5]

"""
Si vous lancer le script sans main.py :
    1) Commenter les deux lignes ci-dessous :
        exec(open('input_data.py').read())
        chemin = sys.argv[1]

    2) Decommenter la troisieme ligne :
        chemin ="sample_mano"

Faire exactement l'inverse pour le lancer depuis le main.py
NB : Si vous lancer le script sans le main.py, la gestion des fichiers de resultats
sera différentes --> voir fonction checkConvergence()
Il faura donc lancer les scripts suivant à la main aussi !
"""
exec(open('input_data.py').read())
chemin = sys.argv[1]
# chemin ="sample_mano/"
TargetVoidRatio, ListTargetVoidRatio, chemin = GestionInputDonnes(ListTargetVoidRatio,chemin)






##########################################################
### CREATION DES MATERIAUX DES WALLS ET DES PARTICULES ###
##########################################################

# Create 6 bounding walls in order : left, right, bottom, top, back, front
O.materials.append(FrictMat(young=young,poisson=poisson,frictionAngle=0,
                            density=density,label='walls'))



"""
on rappelle que quand on créé un body, il a forcement le type du materiau défini
 juste avant, sinon c'est des valeurs par defauts.
"""
wall_ids=[]
wall_ids+=[O.bodies.append(utils.wall(0,axis=0,sense=1))] # left wall
wall_ids+=[O.bodies.append(utils.wall(dimCell[0],axis=0,sense=-1))] # right wall
wall_ids+=[O.bodies.append(utils.wall(0,axis=1,sense=1))] # bottom wall
wall_ids+=[O.bodies.append(utils.wall(dimCell[1],axis=1,sense=-1))] # top wall
wall_ids+=[O.bodies.append(utils.wall(0,axis=2,sense=1))] # back wall
wall_ids+=[O.bodies.append(utils.wall(dimCell[2],axis=2,sense=-1))] # front wall

# Create the sphere assembly
O.materials.append(FrictMat(young=young,poisson=poisson,
                            frictionAngle=radians(frictAngle),
                            density=density,label='spheres'))
sp=pack.SpherePack()
"""
La ligne ci dessous permet la création de particule avec un facteur 10
entre le rayon min et le max
"""
sp.makeCloud((0,0,0),dimCell,Rmean,DispersionRadiusCoeff,num_spheres,False,seed=0)
"""
La ligne ci dessous donne d'autres parametres à notre nuage de points
"""
sp.toSimulation()


# donne des infos de volume positions etc ...
nb, Min_r, Max_r, Min_X, Max_X, Min_Y, Max_Y, Min_Z, Max_Z =infoPositions()





#########################################
### Parametrisation de la compression ###
#########################################
"""
# Option doneHook n'existe pas en triaxlStresscontoler
# a quoi sert les goal alors??? car ils sont sensé travailler en colaboration
# en vrai on peut aussi supprimer les goals dans ce genre de simulation, car ce qui compte
--> update, le goal permet de definir dans quelle direction on compresse --> voir la fonction checkconvregence() pour bien comprendre
c'est le " stressmask"
De plus malgré ce qui est ecrit dans la notice, le paramaètre "strainRate", n'existe pas en TriaxialStressController
Cela renvoie une erreur

--> antoine a du utiliser un autre moyenn de géréer la compression (TrixialCompressionEngine ou
ThreeDTriaxialEngine)
"""
triax= TriaxialStressController(label='triax',
                height0=dimCell[1],width0=dimCell[0],depth0=dimCell[2],
                wall_left_id=wall_ids[0],wall_right_id=wall_ids[1],
                wall_bottom_id=wall_ids[2],wall_top_id=wall_ids[3],
                wall_back_id=wall_ids[4],wall_front_id=wall_ids[5],
                # Isotropic initial compression
                stressMask=Input_StressMask,
                goal1=sigma0,
                goal2=sigma0,
                goal3=sigma0,
                #le parametre dessous mis en true indique une augmentaion du rayon des particules, tandis
                # que si il est false, on bouge les murs
                internalCompaction=Input_InternalCompaction,
                # Comment if internalCompaction=True
                #max_vel=1,stressDamping=0.25,strainDamping=0.8
                # Uncomment if internalCompaction=True
                maxMultiplier=1.1,
                finalMaxMultiplier=1.001
                )


# definition du pas de temps
O.dt=0.95*utils.PWaveTimeStep()



#########################################
###              ENGINES              ###
#########################################

O.engines=[
        ForceResetter(),
        InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Wall_Aabb()]),
        InteractionLoop(
                 [Ig2_Sphere_Sphere_ScGeom(),Ig2_Wall_Sphere_ScGeom()],
                 [Ip2_FrictMat_FrictMat_FrictPhys()],
                 [Law2_ScGeom_FrictPhys_CundallStrack()]
        ),
#        GlobalStiffnessTimeStepper(active=1,timeStepUpdateInterval=100,
#                                   timestepSafetyCoefficient=0.8),
        triax,
        NewtonIntegrator(damping=damp,label='newton'),
        #PyRunner(command='test()', iterPeriod = 50),
        PyRunner(command='checkConvergence(TargetVoidRatio, chemin)',iterPeriod=2500,label='checker', dead=False)
        ]

"""
Le premier argument de O.run() est tres grand
mais il permet juste d'avoir un exit() en dessous
"""
if OptionFentreYade == True :
    O.run(200000000,True)
exit("Tous les samples ont été créé")
