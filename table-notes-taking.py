from tkinter import *

# 1ere fenetre de tkinter
root=Tk()
root_x = 300
root_y = 0
root.geometry("1100x100+%s+%s" % (root_x , root_y))# width x height + x + y : possibilité de ne saisir que x et y
root.title('Notes+')
root.configure(background="#B8C7C5")
root.attributes('-topmost', True)
root.lift(None)

# Création d'image :
# width = 100
# height = 100
# image = PhotoImage(file="move_symbol4.png")
# canvas = Canvas(root, width=width, height=height, bg='#B8C7C5', bd=0, highlightthickness=0)
# canvas.create_image(width/2, height/2, image=image)
# canvas.pack(side=RIGHT,ipadx=52)


menubar = Menu(root)
root.config(menu=menubar)
root.overrideredirect(1)

menufichier = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Fichier", menu=menufichier)
menubar.add_cascade(label="Réduire", command=lambda : reduire_fermer())

menufichier.add_command(label="Save as SNG", command=lambda : creersauvegardefenetres('SNG'))
menufichier.add_command(label="Save as CG", command=lambda : creersauvegardefenetres('CG'))
menufichier.add_command(label="Save as MTT", command=lambda : creersauvegardefenetres('MTT'))
menufichier.add_separator()
menufichier.add_command(label="Quit", command=lambda : root.destroy() )

root.bind("<FocusIn>", lambda event: focus_root())
root.f = 0

def reduire_fermer():
    root.f = 0
    root.overrideredirect(0)
    root.iconify()
    for child in root.winfo_children():
        if isinstance(child,Toplevel):
            child.withdraw()

def focus_root():
    root.f += 1
    if root.f > 1 :
        root.overrideredirect(1)
        for child in root.winfo_children():
            if isinstance(child,Toplevel):
                child.update()
                child.deiconify()


def creerFenetre (position_x, position_y, couleur, texte ): # difference entre attributs et methodes : methode = nom() / attribut .nom
    new_window = Toplevel(root, bg= couleur)
    new_window.attributes('-topmost', True)
    rx = root.winfo_x() # recuperer la postion X
    ry = root.winfo_y()
    new_window.geometry("45x45+%s+%s" % (position_x + rx - root_x, position_y + ry - root_y)) # on ajoute la nouvelle position et on retranche l'ancienne position (root_y)
    new_window.overrideredirect(1)
    new_window.flag= True
    label = Label(new_window ,text=texte, bg= couleur)
    label.write_flag= False
    label.place(relx=1.0, rely=1.0, x=-22, y=-25,anchor=CENTER)
    new_window.bind('<Delete>' , lambda event : new_window.destroy())
    new_window.bind("<ButtonPress-1>", lambda event : drag(new_window,event)) # event= evenement de press-1
    new_window.bind("<ButtonRelease-1>", lambda event : drop(new_window, label, event))
    new_window.bind("<B1-Motion>", lambda event : enMouvement(new_window,event))
    new_window.bind("<Button-3>", lambda event : new_window.popup_menu.tk_popup(event.x_root, event.y_root))
    new_window.bind("<Key>", lambda event : key(label,event)) # lambda : permet d'utiliser une fonction avec plusieurs parametres et permet de retarder l'execution
    new_window.bind("<Double-Button-1>", lambda event : doubleclic(label))
    new_window.bind('<FocusOut>', lambda event:  focus_out(label,couleur))
    numero = Label(new_window,text="",bg = couleur ,font = "Verdana 7 bold ")
    numero.pack(anchor='ne')
    new_window.popup_menu = Menu(new_window, tearoff=0)
    new_window.popup_menu.add_command(label="1ere", command=lambda : Label_coin(numero, "1")) # mumero= emplacement de l'argument dans la fenetre
    new_window.popup_menu.add_command(label="2eme", command=lambda : Label_coin(numero, "2"))
    new_window.popup_menu.add_command(label="3eme", command=lambda : Label_coin(numero, "3"))
    new_window.popup_menu.add_command(label="4eme", command=lambda : Label_coin(numero, "4"))
    new_window.popup_menu.add_command(label="5eme", command=lambda : Label_coin(numero, "5"))
    new_window.popup_menu.add_command(label="kill", command=lambda : new_window.destroy())

def Label_coin(numero, text):
    numero.config(text=text)


def focus_out(label,couleur) :
  label.write_flag= False
  label.config(bg=couleur)

def doubleclic(label):
    label.write_flag= True
    label.config(bg='white')

def drag (window, event): #  windows permet de passer le parametre new_window à toutes les fonctions
    window.prevX= window.winfo_x() # winfo_x() pour recuperer la position en x / 
    window.prevY= window.winfo_y() # Ces 2 lignes : creation de la nouvelle fenetre
    window.x= event.x
    window.y= event.y
def enMouvement (window, event):
    try:
        deltax = event.x - window.x # window x = point de depart / event.x = point actuel de la souris
        deltay = event.y - window.y
        x = window.winfo_x() + deltax
        y = window.winfo_y() + deltay
        window.geometry("+%s+%s" % (x, y))
    except :
        pass

def drop (window, label, event):
    if window.flag and (window.prevX != window.winfo_x() or window.prevY != window.winfo_y()) : # sous entendu window.flag == True
        rx = root.winfo_x() # recuperer la postion X
        ry = root.winfo_y()
        creerFenetre(window.prevX-rx+root_x, window.prevY-ry+root_y, window.cget("bg"), label.cget("text"))
        window.flag = False

    window.x= None # effacer les valeurs prises par x
    window.y= None

def rootDrop (window, event):
    window.x= None
    window.y= None

def rootDrag (window, event): #  windows permet de passer le parametre new_window à toutes les fonctions
    window.prevX= window.winfo_x() # winfo_x() pour recuperer la position en x /
    window.prevY= window.winfo_y() # Ses 2 lignes : creation de la nouvelle fenetre
    window.x= event.x
    window.y= event.y

def rootEnMouvement (window, event):
    try:
        deltax = event.x - window.x # window x = point de depart / event.x = point actuel de la souris
        deltay = event.y - window.y
        x = window.winfo_x() + deltax
        y = window.winfo_y() + deltay
        window.geometry("+%s+%s" % (x, y))
        for child in window.winfo_children() :
            if isinstance(child, Toplevel) :
                cx = child.winfo_x()
                cy = child.winfo_y()
                child.geometry("+%s+%s" % (cx+deltax, cy+deltay))
    except :
        pass


# gestionnaire de la zone cliquable : ajout et supression de texte + RAJOUTER UNE LIGNE POUR SAUVEGARDER LE CONTENU
def key(label,event):
    if label.write_flag == True :
        t = label.cget("text")
        print ("pressed", event.char)#-> commande pour voir ce qui est tapé -> ligne pour debbuger

        if event.keysym  == 'Return':
            label.config(text=t+'\n')
        elif event.keysym  == 'BackSpace':
            label.config(text=t[:-1])     # [...] permet de recupere une partie des caracteres ici [0:-1] donc on recupere tout sauf le dernier caractere / [1:3] on recuperere du 2eme au 4eme non inclus / [2:-2] on recupere du 3eme caractere jusqu a l avant avant dernier inclus
        else:
            label.config(text=t+event.char)

def couleur(window, label, couleur):
    label.config(bg=couleur)
    window.config(bg=couleur)


#bouton CG qui sauvegarde et qui detruit toutes fenetres avec regeneration d'une de chaque apres à l'emplacement prévu
CG = Button(root, text='CG', bg = 'red', command=lambda: chargersauvegarde('CG'))
CG.place(x=1055, y=0, width=45, height=45)


#bouton SNG qui sauvegarde et qui detruit toutes fenetres avec regeneration d'une de chaque apres à l'emplacement prévu
SNG = Button(root, text='SNG', bg = '#91BACF', command=lambda: chargersauvegarde('SNG'))
SNG.place(x=1005, y=0, width=45, height=45)

#bouton MTT qui sauvegarde et qui detruit toutes fenetres avec regeneration d'une de chaque apres à l'emplacement prévu
MTT = Button(root, text='MTT', bg = '#FEE347', command=lambda: chargersauvegarde('MTT'))
MTT.place(x=1005, y=50, width=45, height=45)



# bouton pour remettre toutes les fenetres on top des autres programmes :
ontop_bouton = Button(root, width=6, height=2, text='On\nTop', bg = '#CCC6AD', command=lambda : ontop())
ontop_bouton.place(x=1055, y=50, width=45, height=45)

def ontop():
    for child in root.winfo_children() :
        if isinstance(child, Toplevel) : # cela verifie la class de la fenetre s'applique qu'aux toplevel
            child.attributes('-topmost', 1)


def creersauvegardefenetres(type_jeu):
    fichier = open("sauvegarde_%s.txt" % (type_jeu), "w+") # write

    for child in root.winfo_children() :
        print(child)
        if isinstance(child, Toplevel) :
            label= child.winfo_children()[0]
            relative_x = child.winfo_x() - root.winfo_x() + root_x
            relative_y = child.winfo_y() - root.winfo_y() + root_y
            fichier.write(str(relative_x) + ','+ str(relative_y) +','+ str(child.cget('bg'))+',' + str(label.cget('text')).replace('\n', '\\n').replace('\r','\\n')+ "\n")

    fichier.close()

def chargersauvegarde(type_jeu):
    for child in root.winfo_children() :
        if isinstance(child, Toplevel) : #verifier que l'enfant est bien une fentre top level
            child.destroy()
    fichier = open("sauvegarde_%s.txt" % (type_jeu), "r+") # read
    contenu = fichier.read()
    lignes = contenu.split("\n")
    for ligne in lignes :
        parametres= ligne.split(',')
        creerFenetre(int(parametres[0]), int(parametres[1]), parametres[2], parametres[3].replace('\\n', '\n'))


# 1 resolution d ecran reduire augmenter la fenetre

#  2 les notes doivent etre solidaires de la fenetre root principale.


# creer de nouvelles fenetres une a une 0 100 / 100 100 :
creerFenetre(310, 25, '#D400FF', "") #violet fluo   310 25 sont des arguments
creerFenetre(310, 70, '#D400FF', "") #violet fluo
creerFenetre(355, 25, '#D400FF', "") #violet fluo
creerFenetre(355, 70, '#D400FF', "") #violet fluo
creerFenetre(400, 25, '#EFA0FF', "") #violet pale
creerFenetre(400, 70, '#EFA0FF', "") #violet pale

creerFenetre(450, 25, '#318CE7', "") #bleu france
creerFenetre(450, 70, '#318CE7', "") #bleu france
creerFenetre(495, 25, '#318CE7', "") #bleu france
creerFenetre(495, 70, '#318CE7', "") #bleu france
creerFenetre(540, 25, '#91BACF', "") #bleu pastel
creerFenetre(540, 70, '#91BACF', "") #bleu pastel

creerFenetre(590, 25, '#7FDD4C', "") #vert absinthe
creerFenetre(590, 70, '#7FDD4C', "") #vert absinthe
creerFenetre(635, 25, '#7FDD4C', "") #vert absinthe
creerFenetre(635, 70, '#7FDD4C', "") #vert absinthe
creerFenetre(680, 25, '#C2F732', "") # vert chartreuse
creerFenetre(680, 70, '#C2F732', "") # vert chartreuse

creerFenetre(730, 25, 'yellow', "") # jaune
creerFenetre(730, 70, 'yellow', "") # jaune
creerFenetre(775, 25, 'yellow', "") # jaune
creerFenetre(775, 70, 'yellow', "") # jaune
creerFenetre(820, 25, '#FEE347', "") # jaune paille
creerFenetre(820, 70, '#FEE347', "") # jaune paille

creerFenetre(870, 25, '#FF8830', "") # orange
creerFenetre(870, 70, '#FF8830', "") # orange
creerFenetre(915, 25, '#FF8830', "") # orange
creerFenetre(915, 70, '#FF8830', "") # orange
creerFenetre(960, 25, 'orange', "") # orange pastel
creerFenetre(960, 70, 'orange', "") # orange pastel

creerFenetre(1010, 25, 'red', "") # rouge
creerFenetre(1010, 70, 'red', "") # rouge
creerFenetre(1055, 25, 'red', "") # rouge
creerFenetre(1055, 70, 'red', "") # rouge
creerFenetre(1100, 25, '#9F7001', "") # marron
creerFenetre(1100, 70, '#9F7001', "") # marron
creerFenetre(1145, 25, '#CCC6AD', "") #gris
creerFenetre(1145, 70, '#CCC6AD', "") #gris

root.bind("<ButtonPress-1>", lambda event : rootDrag(root,event)) # event= evenement de press-1
root.bind("<ButtonRelease-1>", lambda event : rootDrop(root, event))
root.bind("<B1-Motion>", lambda event : rootEnMouvement(root,event))
root.geometry()
root.mainloop()
