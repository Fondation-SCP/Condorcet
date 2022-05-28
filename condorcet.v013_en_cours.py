import array

#Interface Humaine :
#1.Rentrer chaque vote
#-> Premier vote, identifie les pseudos
#-> Si un pseudo étranger est rentré, prévenir l'utilisateur qu'il y a une faute d'orthographe quelque part
#-> Permettre à l'utilisateur de vérifier ses saisies avant de soumettre

def recup_vote(chaine,liste_vote = [],next_equal = False):
    """Fonction récurrente qui établit la liste ordonnée des préférences pour un vote précis (vote non-conforme -> vote conforme)
    
        chaine est une chaîne de caractères qui correspond au vote. Elle est donc composée de caractères encodés en UFT-8.
            Les pseudos des candidats doivent être écrits sans espaces, sans <, sans =.
            Les pseudos des candidats doivent être composés de deux caractères au moins.
        liste_vote est la liste des votes obtenus jusqu'alors. Paramètre optionnel.
        next_equal indique si le prochain candidat est censé être à égalité avec le candidat précédent. Paramètre optionnel.
        
        La fonction doit démarrer avec next_equal = False, une liste_vote vide et la chaîne entière.
        
        STATUT FONCTION : TESTEE ET FONCTIONNELLE"""
    
    #cas où on arrête la récurrence
    taille = len(chaine)
    if(taille == 0):
        return("",liste_vote)
    
    i=0
    marqueur = chaine[i]
    liste = liste_vote

    if(taille == 1):
        if(marqueur != ' ' and marqueur != '>' and marqueur != '<' and marqueur != '='):
            liste[-1]=liste[-1]+marqueur
        if next_equal:
            liste[-1]=liste[-1]+"="
        return("",liste)

    new_next_equal = False
    #pour examiner caractère par caractère, on établit un marqueur ; ce marqueur ne doit pas être un symbole non retenu (espace, <, = ou fin de chaîne)
    if(marqueur == ' ' or marqueur == '>' or marqueur == '<' or marqueur == '='):
        while((marqueur == ' ' or marqueur == '>' or marqueur == '<' or marqueur == '=') and i < taille - 1):
            if marqueur == '=':
                new_next_equal = True
            i+=1
            marqueur = chaine[i]
    
        return recup_vote(chaine[i:],liste_vote,new_next_equal or next_equal)
    
    pseudo = ''
    #tant qu'on ne trouve pas un symbole non retenu, on choppe le pseudo (demande de ne pas mettre de symbole non retenu dans les pseudos)
    while(marqueur != ' ' and marqueur != '>' and marqueur != '<' and marqueur != '=' and i<taille-1):
        pseudo += marqueur
        i+=1
        marqueur = chaine[i]
    #on ajoute le pseudo à la Liste
    if next_equal and len(chaine[i:])>1:
        pseudo = pseudo + "="
        new_next_equal = False
    elif next_equal:
        new_next_equal = True
    liste = liste + [pseudo]

    #on retourne la nouvelle liste récupérée + la nouvelle chaîne raccourcie des données déjà obtenues
    return recup_vote(chaine[i:],liste,new_next_equal)

#Test recup_vote()
#_,l = recup_vote(" Jean> Pierre > Marc ")
#print("Ceci est le résultat : ",l)
#_,l, = recup_vote(" Jean> Pierre = Marc ")
#print("Ceci est le résultat : ",l)
#_,l = recup_vote(">>> Jean> Pierre = Marc      ")
#print("Ceci est le résultat : ",l)
#_,l = recup_vote("Pierre > Marc = Jean")
#print("Ceci est le résultat : ",l)
#_,l = recup_vote("Pierre> Marc = Jean")
#print("Ceci est le résultat : ",l)
#_,l = recup_vote("Jean = Marc = Pierre")
#print("Ceci est le résultat : ",l)
#_,l = recup_vote("Pierre > Marc < Jean")
#print("Ceci est le résultat : ",l)

#NOTE : (ENCOURS) une ALTERNATIVE à recup_vote plus efficace serait de corriger d'abord les erreurs d'écriture ; puis d'utiliser un array avec la division par > et = pour diviser
#Ensuite, le premier vote entré pourrait servir de référentiel pour les prochains pseudos, corrigeant les erreurs.
#TO DO :
#   - 1. fonction de correction de l'écriture (Done, correction_ecriture())
#        - 1.1 fonction qui détermine s'il reste ou non des symboles significatifs à la fin (Done, symbole_significatif())
#   - 2. fonction qui établit la liste des références à partir du premier vote (Done, references(), besoin d'être testée un peu +)
#   - 3. fonction qui divise en liste les participants de chaque vote (Done, votes_conformes2())
#       - 3.1 fonction qui cherche si l'élément se trouve dans une liste d'une liste (Done, in_exhaustif)
#   - 4. fonction qui compare aux références le nom d'un participant et qui permet de trouver la variante la plus proche typographiquement parlant 
#       (compter les erreurs de frappe avec des proximités de lettres)
#       (demander à l'utilisateur de confirmer le changement o/n)
#       # (Done,comp_aux_refs())
#   - 5. CORRECTION BUNDLE
#       - 5.1 vérifie dans un tableau si la chaîne a été modifiée ou non
#       - 5.2 vérifie s'il y a une irrégularité au niveau des participants
#   - . assembler tout ça
#       # (_, en cours, calcul_defaite2() à créer)
#   - .. INTERACTION BUNDLE
#       - ..1 demande le nom du votant puis l'entrée de la chaîne

def symbole_significatif(chaine):
    """Détermine s'il reste au moins un symbole significatif, càd autres que >, ' ', < et =
    
    STATUT : TESTEE ET FONCTIONNELLE"""
    res = False
    for element in chaine:
        if element not in [">"," ","<","="]:
            res = True
            break
    return res

#Tests symbole_significatif
#l = ">     = !"
#print(symbole_significatif(l))
#l="      "
#print(symbole_significatif(l))

def correction_ecriture(origine):
    """Fonction réccurrente qui corrige l'écriture des strs pour faciliter leur division. Cette fonction prend en compte les erreurs suivantes :
    
        Espaces en trop (recup_vote)
        Signes ">" et "=" en trop (recup_vote)
        Signes "<" à la place de "> (recup_vote)

        Il faut que les pseudos n'aient pas de signe =, > ou < en leur sein ; que l'ordre ne soit pas totalement inversé.

        STATUT FONCTION : Rajouter corr_maj pour que ça marche
    """
    #print(origine) #déboguage
    #pour ne pas modifier la chaîne originale
    taille = len(origine)
    chaine = ""
    i=0
    corr_maj = False
    #le second critère sert à arrêter le programme lorsqu'une boucle infinie de rajout se crée, à des fins de test
    while (i < taille and len(chaine)<=len(origine)):
        marqueur = origine[i]
        #print("Marqueur examiné : '",marqueur,"' en ",i,"-ème position") #déboguage
        if marqueur == "<":
            if not symbole_significatif(origine[i:]):
                i=taille
            else:
                chaine += ">"
                while(i < taille - 1 and (origine[i] == ' ' or origine[i] == '>' or origine[i] == '<' or origine[i] == '=')):
                    i+=1
        elif marqueur == ">" or marqueur == "=":
            if chaine == "":
                i+=1
            elif not symbole_significatif(origine[i:]):
                i=taille
            else:
                chaine += marqueur
                while(i < taille - 1 and (origine[i] == ' ' or origine[i] == '>' or origine[i] == '<' or origine[i] == '=')):
                    i+=1
        elif marqueur == " ":
            i+=1
        else:
            chaine+=marqueur
            i+=1
        #print("Résultat so far : ",chaine) #déboguage
    if(len(chaine)>len(origine)):
        print("Boucle infinie de rajout arrêtée de force")
        #si nécessaire, cas où le test casse la fonction, permet une meilleur visibilité seulement en déboguage

    return chaine,corr_maj

#Test correction_ecriture()
#l,_ = correction_ecriture(" Jean> Pierre > Marc ")
#print("Ceci est le résultat : ",l) #valide
l2_main,_ = correction_ecriture(" Jean> Pierre = Marc ")
print(l2_main,_)
#print("Ceci est le résultat : ",l2_main) #valide
#l,_ = correction_ecriture(">>> Jean> Pierre = Marc      ")
#print("Ceci est le résultat :",l) #valide
#l,_ = correction_ecriture("Pierre > Marc = Jean")
#print("Ceci est le résultat : ",l) #valide
#l,_ = correction_ecriture("Pierre> Marc = Jean")
#print("Ceci est le résultat : ",l) #valide
#l,_ = correction_ecriture("Jean = Marc = Pierre")
#print("Ceci est le résultat : ",l) #valide
l1_main,_ = correction_ecriture("Pierre > Marc < Jean")
print(l1_main,_)
#print("Ceci est le résultat : ",l1_main)#valide
#l,_ = correction_ecriture("Pierre > Marc < Jean <")
#print("Ceci est le résultat : ",l)#valide
#l,_ = correction_ecriture("Pierre > Marc < Jean <=")
#print("Ceci est le résultat : ",l) #valide
#l,_ = correction_ecriture("Pierre > Marc < Jean =")
#print("Ceci est le résultat : ",l) #valide
l,_ = correction_ecriture("Pierre >= Marc < Jean")
print(_)

#Test pour les espaces
#if " " in l:
#    print("Espace oublié !")


def in_exhaustif(quete,liste):
    """Fonction réccurrente qui cherche un élément dans une liste en prenant compte que la liste peut aussi contenir des sous-listes.
    
    STATUT : TESTEE ET FONCTIONNELLE"""
    res = False
    for element in liste:
        if type(element)==list:
            res = in_exhaustif(quete,element)
            if res == True:
                break
        elif type(element)==type(quete):
            if quete == element:
                res = True
                break
    return res

#Test de in_exhaustif
#l_exhaustif = [1,2]
#print(in_exhaustif(1,l_exhaustif)) #valide
#l_exhaustif = [1,2]
#print(in_exhaustif(3,l_exhaustif)) #valide
#l_exhaustif=[[],[3,2]]
#print(in_exhaustif(2,l_exhaustif)) #valide

def votes_conformes2(liste):
    """Fonction qui établit une liste de votes conformes à partir d'une liste de strings correctement écrites
    
    STATUT : Manque une fonction in_exhaustif() qui cherche si un élément se trouve dans une liste OU les sous-listes de ses listes
    
    Crédit : Mafiew pour le concept et le code qui crée vote_array"""

    res = []
    for vote in liste:
        #print("La chaîne de vote examinée est :",vote)
        vote_array = [participant.split('=') for participant in vote.split('>')]
        #print("Nouvel ensemble : ",vote_array)
        res.append(vote_array)
        #print("Nouveau résultat so far : ",res)
    return res

#Test de votes_conformes2()
#l_conf2 = votes_conformes2(["Pierre>Marc>Jean","Pierre=Jean>Marc"])
#print(l_conf2) #valide
#l_conf2 = votes_conformes2(["Pierre=Marc=Jean"])
#print(l_conf2) #valide
#l_conf2 = votes_conformes2(["Pierre>Marc>Jean"])
#print(l_conf2) #valide
l_conf_main = votes_conformes2([l1_main,l2_main])
#print(l_conf_main) #valide

def references(liste_votes_conformes):
    """Fonction qui établit une liste de référence à partie de la liste des votes conformes.
    Le résultat retourné servira à vérifier si l'orthographe des participants est valide ou non.
    
    STATUT : TESTEE ET FONCTIONNELLE"""
    liste_ref = []
    if len(liste_votes_conformes)==0:
        print("La liste en paramètre de la fonction references() est vide.")
        return liste_ref
    ref_array = liste_votes_conformes[0]
    if type(ref_array[0])!=list:
        print("Le format de la liste en paramètre de la fonction references() n'est pas adéquat.")
        return liste_ref
    for i in range(len(ref_array)):
        #print(i)
        mini_liste = ref_array[i]
        #print("Mini-liste = ",mini_liste)
        for participant in mini_liste:
            #print("Participant = ",participant)
            liste_ref.append(participant)
    return liste_ref

#Test de references()
ref_main = references(l_conf_main)
#print(ref_main) #valide
#ref = references([]) #valide
#ref = references(l_conf2)
#print(ref) #valide
#ref = references(["Pierre"]) #valide

def comp_aux_ref(participant,ref):
    """Fonction qu'on n'appelle que si particant not in ref. Elle comparera alors le terme problématique aux références
    pour trouver la meilleure alternative.
    
    Prend en compte les erreurs de compréhension les plus communes rapportées lors du vote Condorcet
    sur le nouveau logo de la branche francophone, càd :
    - Majuscule/minuscule lettres
    - 0 ou O
    - l (L minuscule) ou I (i majuscule) ou 1 (chiffre)
    - tiret underscore ou tirer du 6 ou cadratin (toutes déclinaisons)
    - e accent grave et e accent aigu
    - m et n
    
    On ne peut pas corriger automatiquement les fautes liées à la motricité, car les claviers azerty et qwerty donneraient des résultats
    différents. On ne peut donc agir que sur les erreurs de compréhension de l'utilisateur.
    
    STATUT : TESTEE ET FONCTIONNELLE"""
    best_match = '',0
    taille_p = len(participant)
    for element in ref:
        i=0
        sum_similar = 0
        if len(element)>taille_p:
            plus_long = element
            plus_court = participant
        else:
            plus_long = participant
            plus_court = element
        for char in plus_court:
            if i >= len(plus_long):
                break
            char_examine = plus_long[i]
            if char.upper() == char_examine.upper():
                sum_similar+=1
            else:
                #Confusion O et 0
                conf_O0 = ['O','0']
                #Confusion entre l (L minuscule), I (i majuscule) et 1 (chiffre)
                conf_il1 = ['I','1','l']
                #Confusion entre les tirets :
                conf_tirets = ['-','_','—','–']
                #confusion accents du e
                conf_accents_e = ['è','é']
                #confusion M et n
                conf_mn = ['m','n']
                conf_MN = ['M','N']
                if char.upper() in conf_O0 and char_examine.upper() in conf_O0 :
                    print("Erreur 0 O")
                    sum_similar+=1
                elif char in conf_il1 and char_examine in conf_il1:
                    print("Erreur 1 I l")
                    sum_similar+=1
                elif char in conf_tirets and char_examine in conf_tirets:
                    print("Erreur tiret")
                    sum_similar+=1
                elif char in conf_accents_e and char_examine in conf_accents_e:
                    print("Erreur accent e")
                    sum_similar+=1
                elif (char in conf_mn and char_examine in conf_mn) or (char in conf_MN and char_examine in conf_MN):
                    print("Erreur MN")
                    sum_similar+=1
            i+=1
        _,best_score = best_match
        if best_score < sum_similar:
            best_match = element,sum_similar
    res,_ = best_match
    return(res)

#Test de comp_aux_ref()
#correction_Pirre_en_Pierre = comp_aux_ref('Pirre',ref_main)
#print(correction_Pirre_en_Pierre) #valide
#correction_Narc_en_Marc = comp_aux_ref('Narc',ref_main)
#print(correction_Narc_en_Marc) #valide
#correction_tiret = comp_aux_ref('Jean_Hugues',['Jean-Hugue','Jean-Hugues','Paul_Myrtille'])
#print(correction_tiret) #valide
#correction_accents_e = comp_aux_ref('Sélèné1',['Apollon','Mars','Séléné1'])
#print(correction_accents_e) #valide
#correction_O0 = comp_aux_ref('PIerr0T',['PIERROT','Pierre','JACQUES','POULPE'])
#print(correction_O0) #valide
                

            

#Test de comp_aux_ref()
#Quid des pseudos extrêmement similaires ? à tester
    


#FIN DU TRAVAIL ENCOURS

def votes_conformes(votes_bruts):
    """Fonction qui transforme une liste de votes non conformes en liste de votes conformes
    
     STATUT FONCTION : TESTEE ET FONCTIONNELLE"""
    votes = []
    for element in votes_bruts:
        _,l = recup_vote(element)
        votes = votes + [l]
    return votes

#Test votes_conformes()
#votes_bruts = ["Jean = Marc = Pierre","Pierre > Marc = Jean","Jean > Marc > Pierre"]
#votes_finaux = votes_conformes(votes_bruts)
#print(votes_finaux)

def enlever_equal(chaine):
    """Petite fonction qui sert simplement à enlever le symbole égal d'une chaîne de caractère (pseudo).
    
    STATUT FONCTION : TESTEE ET FONCTIONNELLE"""

    res = [char for char in chaine if char != "="]
    return ''.join(res)

#Test enlever_equal
#test_equal=enlever_equal("Marc=")
#print(test_equal)

def quete_clefs_par_valeur(dico, valeur):
    """Fonction intermédiaire qui sert à chercher dans un dico une (ou plusieurs) clef(s) selon sa (leur) valeur associée.

    STATUT FONCTiON : TESTEE ET FONCTIONNELLE"""

    res = []
    for element in dico.keys():
        if dico[element] == valeur:
            res+=[element]
    return res

#Test quete_clefs_par_valeur
#dico_test = {'a':0,'b':2,'c':45}
#print(quete_clefs_par_valeur(dico_test,0))
#print(quete_clefs_par_valeur(dico_test,45))
#print(quete_clefs_par_valeur(dico_test,46))



def sorted_dico_value(dico):
    """Fonction intermédiaire qui sert à classer les éléments d'un dictionnaire selon les valeurs qu'il contient (et non les clés).
    -> améliore la lisibilité humaine, pas le programme en soi
    
    STATUT FONCTiON : TESTE ET FONCTIONNELLE
    
    NOTE D'AMELIORATION : Pourrait peut-être améliorer la complexité de la fonction gagnants(), à étudier"""

    values = [dico[element] for element in dico]
    values = sorted(values)
    res = {}
    for value in values:
        clefs_correspondantes = quete_clefs_par_valeur(dico,value)
        for clef in clefs_correspondantes:
            res.update({clef:value})
    return(res)

#Test de sorted_dico_value:
#dico_test = {'a':43,'b':42,'c':45}
#print(sorted_dico_value(dico_test))
#dico_test2 = {'a':43,'b':42,'c':45,'d':43}
#print(sorted_dico_value(dico_test2))

def calcul_défaites(votes):
    """Fonction qui détermine à partir des votes le dictionnaire des défaites
    votes est une liste de listes de chaînes de caractère prenant chacune la forme :"Candidat 1 , Candidat 2 , Candidat 3..."
        Si un pseudo de Candidat se finit par "=", c'est qu'il faut compter une égalité avec le candidat précédent.
    seuil est un entier représentant le nombre de candidats que l'on veut retenir (par exemple les trois premiers)
    
    STATUT FONCTION : TESTEE ET FONCTIONNELLE JUSQUE NOUVEL ORDRE"""

    if(len(votes)==0):
        return("Pas de gagnant disponible.")
    
    #on détermine le nombre de candidats
    nb_candidats = len(votes[0])

    #on détermine la liste des candidats

    liste_candidats = [enlever_equal(element) for element in votes[0]]

    #création du dictionnaire de défaites
    dico_defaite = {}
    for element in liste_candidats:
        dico_defaite[element] = 0

    #on va regarder le nombre de défaites subies par chaque candidat quand on le compare aux autres dans chaque vote
    #puis on ajoute au dico des défaites

    for vote in votes:
        #print(vote)
        for i in range(nb_candidats-1):
            indice = nb_candidats-i-1
            candidat = vote[-indice]
            #print(candidat)
            if(enlever_equal(candidat) not in liste_candidats):
                print(candidat)
                print("Erreur : les pseudos entrés ont des variations d'orthographe qui empêchent le programme de fonctionner. Veuillez les resaisir.")
                return (None)
                #!!!Dans le futur, peut-être une fonctionnalité qui ne demanderait à ne resaisir que le vote qui pose problème ? + calcul automatique du pseudo le plus proche avec confirmation humaine nécessaire
            nb_egaux = 0
            #on vérifie s'il y a des égalités avec le candidat actuellement examiné
            if "=" in candidat:
                nb_egaux +=1
                while(indice + nb_egaux < len(vote) and "=" in vote[-indice-nb_egaux]):
                    #Note : si les fonctions précédentes sont bien faites et les données entrées correctes,
                    #il ne peut pas y avoir de "=" dans le premier élément de la liste vote et donc aucun dépassement de mémoire.
                    nb_egaux +=1
            #print("nb_egaux = ",nb_egaux)
            dico_defaite[enlever_equal(candidat)] += nb_candidats - indice - nb_egaux
            #print("indice = ",indice)
            #print("nb_candidats = ",nb_candidats)
            #print(nb_candidats - indice - nb_egaux)

    return sorted_dico_value(dico_defaite)

#Test de calcul_defaites():
#votes_bruts = ["Pierre > Marc=Jean","Marc >    Jean >> Pierre","Pierre = Jean = Marc", "   Marc > Jean > Pierre"]
#votes = votes_conformes(votes_bruts)
#dico = calcul_défaites(votes)
#print(dico)

#votes_bruts = ["Jean > Marc = Pierre","Marc = Jean > Pierre","Pierre = Jean = Marc", "Marc > Jean > Pierre"]
#votes = votes_conformes(votes_bruts)
#dico = calcul_défaites(votes)
#print(dico)

def gagnants(dico,seuil = 1):
    """cette fonction retourne les gagnants du vote par condorcet.
        dico est le dictionnaire des défaites
        seuil est un paramètre optionnel qui indique le nombre de gagnants (par catégorie de classement) demandés.
            Par défaut, ne renvoie que le(s) gagnant(s) placé(s) premier(s).
        
        La fonction retourne une liste de listes, classée par ordre de victoire.
        Les candidats contenus dans une meme sous-liste sont à égalité.
        
        STATUT FONCTION : TESTEE ET FONCTIONNELLE MAIS MANQUE DE JEUX DE TEST
        
        NOTE D'AMELIORATION : 1. Ne rend pas automatiquement les gagnants en cas d'égalité. Plutôt, rend les "seuil" premières catégories de
                                gagnant sur le podium. Il faut calculer si les égalités permettent de remplir tout pile les gagnants ou non.
                              2. Vérifier si la complexité ne pourrait pas être améliorée par l'usage systématique du dictionnaire ordonné."""
    valeur_gagnante = min(dico[element] for element in dico)
    v_g_precedent = []
    gagnants = []
    for i in range(seuil):
        #print(_)
        gagnants+=[[element for element in dico if dico[element]==valeur_gagnante]]
        #print(gagnants)
        v_g_precedent += [valeur_gagnante]
        if i != seuil-1:
            valeur_gagnante = min(dico[element] for element in dico if dico[element] not in v_g_precedent)
    return gagnants

#Test de gagnants():
#dico = {'Jean': 2, 'Marc': 1, 'Pierre': 3}
#print(gagnants(dico,3))

#Ici les pignoufs
#EXPLICATIONS
#   print("EXPLICATIONS")

#Ces explications présentent le fonctionnement principal de l'algorithme de calcul afin d'aider à le comprendre.
#Une fois l'interface et les fonctions d'interaction humaine terminées, toutes ces étapes seront facilitées et accompagnées. Il n'y aura qu'à rentrer les votes.

#On doit tout d'abord entrer manuellement les votes et uniformiser les pseudos/options. Je vais réfléchir à une façon d'automatiser ça.

#   vote1 = "Jean > Marc = Pierre > Jacques = Crystal"
#   vote2 = "Pierre > Marc = Crystal > Jean = Jacques"
#   vote3 = "Jean > Marc = Pierre = Jacques > Crystal"

#Parfois, quelques erreurs peuvent se glisser et être réparées automatiquement par mon programme.
#   vote4 = "Crystal > Marc > Pierre > Jacques > Jean"
#   vote5 = "      Marc > Pierre > Jacques > Jean == Crystal"

#on réunit ces votes bruts en une liste
#   votes_bruts=[vote1,vote2,vote3,vote4,vote5]
#Variable votes_bruts vérifiée humainement, fonctionne

#on passe la liste et les votes dans un programme d'uniformisation qui va retirer les espaces en trop éventuels et autres petites erreurs basiques
#   votes = votes_conformes(votes_bruts)
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
#   dico = calcul_défaites(votes)
#Variable dico vérifiée humainement, valide

#1 défaite = il y a une personne au-dessus de lui dans le vote. L'égalité avec quelqu'un d'autre n'est donc pas une défaite.
#Donc dans le vote "Jean > Pierre > Marc", Marc essuie deux défaites car Pierre et Jean sont au-dessus de lui.
#Dans le vote "Jean > Pierre = Marc", il n'en essuie qu'une car il est à égalité avec Pierre et en-dessous de Jean.
#On fait la somme de tous les votes. Dans ce petit exemple, Marc a donc 3 défaites. Jean en a 0 et Pierre en a 2.

#revenons à l'exemple principal avec 5 votes différents.
#On demande au programme de nous donner le gagnant.
#   print("Gagnant unique de l'exemple")
#   print(gagnants(dico))
#>>> [['Marc']], vérifié humainement
#En effet, Marc n'a subi que 4 défaites, il est donc le grand vainqueur.

#Lors des élections staffs, il y a souvent plus d'un gagnant car on veut pourvoir un certain nombre de place.
#Il suffit de rajouter un paramètre sous la forme d'un nombre entier, afin de demander le nombre de gagnants que l'on veut.
#Par exemple, on veut deux junior staffs.
#   print("Plusieurs gagnants de l'exemple")
#   print(gagnants(dico,2))
#>>> [['Marc'],['Pierre']], vérifié humainement
#En effet, Pierre n'avait que cinq défaites et talonnait donc Marc. Si on prend deux juniors staffs, ce seront ces deux là.

#Par défaut, il n'y a qu'un gagnant renvoyé par la fonction gagnants(). C'est souvent le cas, par exemple pour choisir des options :
#   vote1 = "Ping-pong > Piscine = Equitation"
#   vote2 = "Piscine > Equitation > Ping-pong"

#   print("Activité gagnante de l'exemple")
#   print(gagnants(calcul_défaites(votes_conformes([vote1,vote2]))))
#>>> [['Piscine']], vérifié humainement
# Allez, tous à la piscine !!!

#Il y a maintenant un cas à considérer : les égalités.
#On modifie l'exemple précédent :
#   vote1 = "Ping-pong > Piscine = Equitation"
#   vote2 = "Piscine = Equitation > Ping-pong"

#Cette fois-ci, on veut faire deux activités différentes :
#   print("Plusieurs activités gagnantes de l'exemple (avec égalité)")
#   print(gagnants(calcul_défaites(votes_conformes([vote1,vote2])),2))
#>>> [['Piscine','Equitation'],['Ping-pong']], vérifié humainement
#On voit que la Piscine et l'Equitation remportent autant d'adhésion l'une que l'autre !
# On peut alors exploiter ce résultat pour choisir les deux activités. Ce choix sera automatisé lorsque cela sera possible, dans un futur proche.

#TEST de gagnants() avec les résultats des élections staffs précédentes
#   print("Résultats des élections staffs précédentes")

#On doit tout d'abord entrer manuellement les votes et uniformiser les pseudos. Je vais réfléchir à une façon d'automatiser ça.
#   v1 = "Flauros > Olbaum > Skoda > Alwaid > Gabitoon = Herolles > D-2108 > Mazdouk > Aloices > Henry"
#   v2 = "Skoda = Olbaum = Alwaid > Flauros = Herolles = Henry = Aloices = D-2108 = Mazdouk = Gabitoon"
#   v3 = "Skoda > Alwaid > Olbaum > Mazdouk = Henry = Herolles > Flauros > Aloices > Gabitoon = D-2108"
#   v4 = "Skoda = Alwaid = Olbaum = Flauros > Gabitoon = Herolles = Mazdouk = Aloices > Henry > D-2108"
#   v5 = "Flauros > Alwaid > Skoda > Olbaum > Mazdouk > Gabitoon = Henry > Herolles = D-2108 = Aloices"
#   v6 = "Skoda = Alwaid = Olbaum > Gabitoon = Mazdouk  = Aloices = Henry = Flauros = Herolles = D-2108"
#   v7 = "Henry = Alwaid > Herolles > Olbaum > Aloices = Skoda > Mazdouk > Flauros > D-2108 > Gabitoon"
#   v8 = "Flauros > Herolles > Skoda > Alwaid > Mazdouk > Olbaum > Aloices > D-2108 > Henry > Gabitoon "
#   v9 = "Alwaid > Flauros > Herolles = Skoda > Mazdouk > Olbaum > Henry > Gabitoon > Aloices > D-2108"
#   v10 = "Alwaid = Herolles > Henry = Skoda = Flauros > Olbaum = Mazdouk = Gabitoon = Aloices > D-2108"
#   v11 = "Olbaum > Skoda = Flauros > Aloices = D-2108 > Herolles = Alwaid > Mazdouk > Henry > Gabitoon"
#   v12 = "Alwaid = Gabitoon = Henry > Aloices = D-2108 = Herolles = Flauros = Mazdouk = Olbaum = Skoda"
#   v13 = "Flauros = Skoda > Herolles = Olbaum = Alwaid = D-2108 > Henry = Gabitoon = Aloices = Mazdouk"
#   v14 = "Alwaid > Olbaum > Gabitoon > Flauros = Skoda > Henry > Herolles > Mazdouk > D-2108 = Aloices"
#   v15 = " Alwaid > Herolles = Skoda > D-2108 > Flauros > Mazdouk > Olbaum > Henry > Gabitoon = Aloices"

#   votes_bruts = [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15]

#   votes = votes_conformes(votes_bruts)

#   dico = calcul_défaites(votes)
#   print("Calcul des défaites :")
#   print(dico)

#   print("Gagnant(s) absolu(s) :")
#   print(gagnants(dico))

#   print("3 premiers gagnants ayant un nombre de défaites différent")
#print(gagnants(dico,3))