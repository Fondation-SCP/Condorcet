# Condorcet

Valables pour la version 11.

#EXPLICATIONS
print("EXPLICATIONS")

#Ces explications présentent le fonctionnement principal de l'algorithme de calcul afin d'aider à le comprendre.
#Une fois l'interface et les fonctions d'interaction humaine terminées, toutes ces étapes seront facilitées et accompagnées. Il n'y aura qu'à rentrer les votes.

#On doit tout d'abord entrer manuellement les votes et uniformiser les pseudos/options. Je vais réfléchir à une façon d'automatiser ça.

vote1 = "Jean > Marc = Pierre > Jacques = Crystal"
vote2 = "Pierre > Marc = Crystal > Jean = Jacques"
vote3 = "Jean > Marc = Pierre = Jacques > Crystal"

#Parfois, quelques erreurs peuvent se glisser et être réparées automatiquement par mon programme.
vote4 = "Crystal > Marc > Pierre > Jacques > Jean"
vote5 = "      Marc > Pierre > Jacques > Jean == Crystal"

#on réunit ces votes bruts en une liste
votes_bruts=[vote1,vote2,vote3,vote4,vote5]
#Variable votes_bruts vérifiée humainement, fonctionne

#on passe la liste et les votes dans un programme d'uniformisation qui va retirer les espaces en trop éventuels et autres petites erreurs basiques
votes = votes_conformes(votes_bruts)
#Variable votes vérifiée humainement, fonctionne

#Exemple sans erreur : Le vote "Jean > Pierre > Marc" devient [Jean ; Pierre ; Marc].
#Dans le cas des égalités, un signe "=" est ajouté à la fin du candidat pour indiquer que dans ce vote, le candidat est mis à égalité avec le candidat précédent
#Exemple avec égalité : Le vote "Jean > Pierre = Marc" devient [Jean ; Pierre ; Marc=].
#Les erreurs corrigées par mon programme sont les suivantes :
    #Espaces en trop
    #Signes ">" et "=" en trop
    #Signes "<" à la place de ">"
#Les erreurs que ne corrige pas mon programme et qui le faussent sont les suivantes :
    #Erreur dans l'orthographe des pseudos
    #Un signe >, =, < qui se trouverait au milieu d'un pseudo
    #Si un pseudo est séparé par des espaces
    #Si l'ordre des comparaisons est complètement inversé
#Ces erreurs doivent donc être surveillées lorsque la main humaine saisit la chaîne de caractère.
#Exemple avec erreurs corrigées : Le vote "Jean >> Pierre       == Marc =====" devient [Jean ; Pierre ; Marc=] VALIDE
#Exemple avec erreurs non-corrigées : Le vote "Jean >Pi>erre > MArc" devient [Jean ; Pi ; erre ; MArc] INVALIDE, casse le programme
#Autre exemple avec une erreur non-corrigée : Le vote "Jean < Pierre < Marc" devient [Jean ; Pierre ; Marc] INVALIDE, le programme fonctionne mais renvoie un résultat erroné
    #Or le vote donnait Marc en premier et Jean en dernier (< au lieu de >), on aurait dû obtenir [Marc ; Pierre ; Jean]
#Il faudrait donc que j'ajoute une fonctionnalité pour permettre à l'utilisateur de vérifier les votes qu'il a entrés dans le programme et de les modifier avant soumission.

#Vient ensuite la partie des calculs. On va associer à chaque candidat un certain nombre de défaites en considérant tous les votes donnés.
dico = calcul_défaites(votes)
#Variable dico vérifiée humainement, valide

#1 défaite = il y a une personne au-dessus de lui dans le vote. L'égalité avec quelqu'un d'autre n'est donc pas une défaite.
#Donc dans le vote "Jean > Pierre > Marc", Marc essuie deux défaites car Pierre et Jean sont au-dessus de lui.
#Dans le vote "Jean > Pierre = Marc", il n'en essuie qu'une car il est à égalité avec Pierre et en-dessous de Jean.
#On fait la somme de tous les votes. Dans ce petit exemple, Marc a donc 3 défaites. Jean en a 0 et Pierre en a 2.

#revenons à l'exemple principal avec 5 votes différents.
#On demande au programme de nous donner le gagnant.
print("Gagnant unique de l'exemple")
print(gagnants(dico))
#>>> [['Marc']], vérifié humainement
#En effet, Marc n'a subi que 4 défaites, il est donc le grand vainqueur.

#Lors des élections staffs, il y a souvent plus d'un gagnant car on veut pourvoir un certain nombre de place.
#Il suffit de rajouter un paramètre sous la forme d'un nombre entier, afin de demander le nombre de gagnants que l'on veut.
#Par exemple, on veut deux junior staffs.
print("Plusieurs gagnants de l'exemple")
print(gagnants(dico,2))
#>>> [['Marc'],['Pierre']], vérifié humainement
#En effet, Pierre n'avait que cinq défaites et talonnait donc Marc. Si on prend deux juniors staffs, ce seront ces deux là.

#Par défaut, il n'y a qu'un gagnant renvoyé par la fonction gagnants(). C'est souvent le cas, par exemple pour choisir des options :
vote1 = "Ping-pong > Piscine = Equitation"
vote2 = "Piscine > Equitation > Ping-pong"

print("Activité gagnante de l'exemple")
print(gagnants(calcul_défaites(votes_conformes([vote1,vote2]))))
#>>> [['Piscine']], vérifié humainement
# Allez, tous à la piscine !!!

#Il y a maintenant un cas à considérer : les égalités.
#On modifie l'exemple précédent :
vote1 = "Ping-pong > Piscine = Equitation"
vote2 = "Piscine = Equitation > Ping-pong"

#Cette fois-ci, on veut faire deux activités différentes :
print("Plusieurs activités gagnantes de l'exemple")
print(gagnants(calcul_défaites(votes_conformes([vote1,vote2])),2))
#>>> [['Piscine','Equitation'],['Ping-pong']], vérifié humainement
#On voit que la Piscine et l'Equitation remportent autant d'adhésion l'une que l'autre !
# On peut alors exploiter ce résultat pour choisir les deux activités. Ce choix sera automatisé lorsque cela sera possible, dans un futur proche.
