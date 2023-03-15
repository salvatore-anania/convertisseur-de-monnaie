from tkinter import *
import json
import math
from tkinter.messagebox import *
from tkinter.ttk import Combobox

def clear():
    amount.delete(0,END)
    devise_from_choice.set("")
    devise_to_choice.set("")
    converted.delete(0,END)

def update():
    devise_change=lire_devise()
    devise=["doll"]
    for i in devise_change.keys():
        dev=i[4:]
        devise.append(dev)
    from_currency["menu"].delete(0, "end")
    for item in devise:
        from_currency["menu"].add_command(
            label=item,
            command=lambda value=item: devise_from_choice.set(value)
        )
    to_currency["menu"].delete(0, "end")
    for item in devise:
        to_currency["menu"].add_command(
            label=item,
            command=lambda value=item: devise_to_choice.set(value)
        )


def converting():
    devise_change=lire_devise()
    devise=["doll"]
    for i in devise_change.keys():
        dev=i[4:]
        devise.append(dev)
    if devise_from_choice.get() != devise_to_choice.get() and amount.get():
        if devise_from_choice.get()=="doll":
            taux=devise_change[devise_from_choice.get()+devise_to_choice.get()]
            print(type(taux))
            result=round(float(amount.get())*taux,4)
            save({"From":devise_from_choice.get(),"To":devise_to_choice.get(),"Amount":amount.get(),"Resultat":result,"Taux":taux})
            converted.delete(0,END)
            converted.insert(0,result)
        elif devise_to_choice.get()=="doll":
            taux=1/devise_change[devise_to_choice.get()+devise_from_choice.get()]
            result=round(float(amount.get())*taux,4)
            save({"From":devise_from_choice.get(),"To":devise_to_choice.get(),"Amount":amount.get(),"Resultat":result,"Taux":taux})
            converted.delete(0,END)
            converted.insert(0,result)
        else:
            taux=1/devise_change["doll"+devise_from_choice.get()]*(devise_change["doll"+devise_to_choice.get()])
            result=round(float(amount.get())*taux,4)
            save({"From":devise_from_choice.get(),"To":devise_to_choice.get(),"Amount":amount.get(),"Resultat":result,"Taux":taux})
            converted.delete(0,END)
            converted.insert(0,result)
    else:
        showinfo("Impossible","Conversion impossible !")

def lire_devise():
    devise=["doll"]
    with open("devise.json", "r+") as affiche:
        test=json.load(affiche)
    return test

def add():
    if add_devise.get() and add_taux.get():
        ecrire=open("devise.json", "r+")
        donnes=json.load(ecrire)
        ok=True
        try :
            float(add_taux.get())
        except ValueError:
            ok=False
        else:    
            taux=float(add_taux.get())
            
        if ok:
            donnes["doll"+add_devise.get()] = taux
            ecrire.seek(0)
            ecrire.truncate(0)
            ecrire.write(json.dumps(donnes))
            ecrire.close()
            add_devise.delete(0,END)
            add_taux.delete(0,END)
            update()
            showinfo("Ajouter","Devise ajouté !")
        else:
            showinfo("Erreur","Veuillez entré un nombre !")
    else:
        showinfo("impossible","Entrez des valeurs !")

def save(operation):
    ecrire=open("historique.json", "r+")
    donnes=json.load(ecrire)
    donnes[len(donnes)] = operation
    ecrire.seek(0)
    ecrire.truncate(0)
    ecrire.write(json.dumps(donnes))
    ecrire.close()

fenetre = Tk()
fenetre.title("convertisseur de monnaie")
fenetre.configure(bg='grey')


devise_change=lire_devise()
devise=["doll"]
for i in devise_change.keys():
    dev=i[4:]
    devise.append(dev)
devise_to_choice = StringVar()
devise_from_choice = StringVar()

Label(fenetre, text="Pypower Project : Currency Converter",bg="maroon").pack(anchor="w",fill='x',pady=(0,30))

grid=Frame(fenetre,bg='grey')

amount_label=Label(grid, text="Amount :",bg='grey').grid(row=1, column=0 ,sticky = "w",pady=5)
amount = Entry(grid)
amount.grid(row=1, column=1,pady=5,padx=20,sticky = "e")


from_currency_label=Label(grid, text="From Currency :",bg='grey').grid(row=2, column=0 ,sticky = "w",pady=5)
from_currency = OptionMenu(grid,devise_from_choice,*devise)
from_currency.grid(row=2, column=1,pady=5,sticky = "e",padx=20)


to_currency_label=Label(grid, text="To Currency :",bg='grey').grid(row=3, column=0 ,sticky = "w",pady=5)
to_currency = OptionMenu(grid,devise_to_choice,*devise)
to_currency.grid(row=3, column=1,pady=5,sticky = "e",padx=20)

convert=Button(grid, text="Convert", bg="blue",command=converting).grid(row=5, column=0,sticky = "e",pady=10)

converted_label=Label(grid, text="Converted amount :",bg='grey').grid(row=6, column=0,sticky = "w",pady=5)
converted = Entry(grid)
converted.grid(row=6, column=1,pady=5,sticky = "e",padx=20)

convert=Button(grid, text="Clear All", bg="white",fg="red",command=clear).grid(row=7, column=0,sticky = "e",pady=10)

add_label=Label(grid, text="Devise à ajouter :",bg='grey').grid(row=8, column=0,sticky = "w",pady=5)
Label(grid, text="Taux du dollar vers la devise :",bg='grey').grid(row=9, column=0,sticky = "w",pady=5)
add_devise = Entry(grid)
add_taux = Entry(grid)
add_devise.grid(row=8, column=1,pady=5,sticky = "e",padx=20)
add_taux.grid(row=9, column=1,pady=5,sticky = "e",padx=20)

convert=Button(grid, text="Ajouter devise", bg="white",fg="red",command=add).grid(row=10, column=0,sticky = "e",pady=10)

grid.pack()
fenetre.mainloop()