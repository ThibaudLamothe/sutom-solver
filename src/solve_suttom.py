

def load_text(path):
    """ Charge un fichier texte
    """
    with open(path, 'r') as f:
        return f.read()


def filter_corpus(words_path, first_letter, word_size):
    """ Retourne la liste des mots du corpus correspondant à la taille et à la première lettre
        - Charge le corpus de mots à partir du fichier texte spécifié
    """
    # Load
    words = load_text(words_path).split("\n")
    words = [word.lower().replace("é", "e").replace("è", "e").replace("à", "a").replace("â", "a").replace("ô", "o") for word in words]
    print("Total mots  :", len(words))

    # First letter
    first_list = [i for i in words if i.startswith(first_letter)]
    print(f"Avec {first_letter}      :", len(first_list))

    # Size
    size_list = [i for i in first_list if len(i)==word_size]
    print(f"{word_size} lettres   :", len(size_list))
    
    return size_list


def filter_rules(words_list, lettre_in_not_at = {}, lettre_nb = {}, lettre_at = {}, not_in = []):
    """ Filtre un ensemble de mot, basé sur des règles de construction
        - lettre_in_not_at : {lettre: [positions]}
        - lettre_nb : {lettre: nb}
        - lettre_at : {lettre: position}
        - not_in : [lettres]
    """
    # On parcourt la liste de mots
    # => Tout ceux qui matchent les règles sont conservés
    keep_word = []
    for word in words_list:
        
        # Par défaut on conserve le mot
        ko = False
        
        # Sauf si il matche une des règles
        for lettre, nbs in lettre_in_not_at.items():
            if not isinstance(nbs, list):
                nbs = [nbs]
            for nb in nbs:
                if lettre not in word:
                    ko=True
                elif word[nb]==lettre:
                    ko=True
        for lettre in not_in:
            if lettre in word:
                ko = True        
        for lettre, nb in lettre_nb.items():
            if len([i for i in word if i ==lettre])!=nb:
                ko = True
        for lettre, nb in lettre_at.items():
            if word[nb] != lettre:
                ko=True
        if not ko:
            keep_word.append(word)
            pass
    return keep_word


def filter_macro(words_list, rules):
    return filter_rules(
        words_list, 
        lettre_in_not_at=rules["lettre_in_not_at"],
        lettre_nb=rules["lettre_nb"],
        lettre_at=rules["lettre_at"],
        not_in=rules["not_in"]
    )




if __name__  == "__main__":
    
    #######################################
    # CONFIG
    #######################################
    
    words_path = "../data/mots.txt"
    first_letter = "p"
    word_size = 6
    
    #######################################
    # RULES
    #######################################
    
    # Default value
    lettre_in_not_at = {}
    not_in = []
    lettre_nb = {}
    lettre_at = {}
    
    not_in = ["e", "t", "s"]
    lettre_in_not_at = {"i":2}
    lettre_at = {"n":3}
    # lettre_nb = {"e":1}


    #######################################
    # EXECUTION
    #######################################

    words_list = filter_corpus(words_path, first_letter, word_size)
    short_list = filter_rules(words_list, lettre_in_not_at, lettre_nb, lettre_at, not_in)
    
    if len(short_list) < 25:
        for i in short_list:
            print("-", i)

