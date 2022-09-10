import time
import requests
import pandas as pd

def conv_letters(word):
    """ Conversion du mot en clavier qwerty (pour usage dans selenium)
        - prend un mot bien écrit et renvoie sa traduction clavier
    """
    word = word.lower()
    conv = {
        "a":"q", "q":"a",
        "z":"w", "w":"z",
        ",":"m", "m":",",
    }
    new_word = ""
    for letter in word:
        if letter in conv.keys():
            letter = conv[letter]
        new_word += letter
    return new_word


def get_most_common_word(words_list):
    """ A partir d'une liste de mot, détermine le mot le plus commmun.
        - Celui qui a le plus de proximité avec tous les autres
        - 
    """
    # Si un seul mot, on le renvoie
    if len(words_list)==1:
        return words_list[0]

    # On regarde la distribution des lettres
    words_size = len(words_list[0])    
    df =pd.DataFrame(words_list, columns=["mots"])
    letters = ''.join(words_list)
    len(letters)
    let = [i for i in letters]
    tmp = pd.Series(let).value_counts()
    #tmp.sort_index().plot.bar(figsize=(20 ,5))

    # On crée un dataframe avec une colonne = une lettre
    # (True si elle est dans le mot False sinon)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in alphabet:
        df[letter]=df["mots"].apply(lambda x: letter in x)
    
    # On trie par lettre les plus communes
    dff = df[tmp.index.tolist()].cumsum(axis=1)

    # Et on regarde à la taille du mot celui qui ressort avec le plus de "lettres fréquentes" 
    # Gérer le cas ou le nombre de lettre restant avec l'ensemebles des mots est inférieur à la taille du mot
    # CASSETTE / CAUSETTE le 10/09/2022
    filter_col = min(words_size-1, tmp.shape[0]-1)
    dff = dff.sort_values(by=tmp.index[filter_col], ascending=False)
    
    # On récupère le mot
    df_best = pd.merge(dff, df[["mots"]], left_index=True, right_index=True)[["mots"]].head(10)
    meilleur_mot = df_best.iloc[0, 0]

    return meilleur_mot



def filter_larousse(words_list):
    """ Regarde si le mot existe telquel dans le Larousse
        - Part du principe que si un verbe conjugué est appelé dans l'URL,
          la page est rertouée vers la forme infinitive
        - On élimine donc ceux qui changent
        - Petits défauts sur les homonymes malgré tout donc pas 100% fiable.
        - Et assez long...
    """
    good_words = []
    bad_words = []
    for nb, word in enumerate(words_list):
        print("*"*50)
        print(nb, word)
        word = word.lower()
        url = f"https://www.larousse.fr/dictionnaires/francais/{word}/"
        rep = requests.get(url)
        url_rep = rep.url.replace("%C3%A9", "e").replace("%C3%A2", "a")
        mots_url = url_rep.split("/")
        mots_url = [i for i in mots_url if len(i)>0]
        mot_url = mots_url[-2]
        print(url)
        print(url_rep)
        #correct = word in url_rep
        # si le mot est inclu => KO.
        # si le mot n'est pas trouvé => KO.
        # si trouvé, un nombre est rajouté à l'URL.)
        # si le mot est un nom propre => OK (c'est le seul cas particulier géré)

        correct = word==mot_url
        print(word, url_rep.split("/")[-2], correct)
        time.sleep(1)
        if correct:
            print("Good")
            good_words.append(word)
        else:
            print("Bad")
            bad_words.append(word)
    return bad_words, good_words


def get_initial_word(words_list):
    """ Renvoie un mot pour le premier appel selon la stratégie définie
        (Utile si on veut gérer différemment le premier appel)
    """
    word = words_list[0]
    word = get_most_common_word(words_list)
    return word, conv_letters(word)


def get_new_word(words_list):
    """ Renvoie un mot pour selon la stratégie définie
    """
    word = words_list[0]
    word = get_most_common_word(words_list)
    return word, conv_letters(word)

