from tkinter import *
from tkinter import ttk

def inter(words=["ceci", "est", "un", "test"]):
    """ Crée une interface avec un bouton par mot de la liste fournie
        Retourne le mot surlequel on a cliqué
        Si pas de choix, ou fenêtre fermée : retourn `__automatix__`
    """
    # Création de la fenêtre et centrage
    root = Tk()
    root.eval('tk::PlaceWindow . center')
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    # Ajout du label
    ttk.Label(frm, text="Mots restants! En choisir un ?").grid(column=0, row=0)
    
    # Instanciation de la fonction de callback des boutons
    global rep
    rep = "__automatix__"
    def ma_f(m):
        global rep
        rep = m
        root.withdraw()
    
    # Ajout des boutons (1 par mot)
    for nb, word in enumerate(words):
        ttk.Button(frm, text=word, command=lambda m=word: [ma_f(m), root.withdraw(), root.destroy()]).grid(column=0, row=nb+1)
    
    # Ajout du bouton final => pas de choix par l'utilisateur
    ttk.Button(frm, text="Choix automatique", command=lambda m="__automatix__": [ma_f(m), root.withdraw(), root.quit()]).grid(column=0, row=nb+3)
    
    # Affichage de la fenêtre
    root.mainloop() 
    return rep

if __name__=="__main__":
    rep = inter()
    print(rep)
