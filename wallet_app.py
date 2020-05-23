import tkinter
import sys
import os
import sqlite3
from tkinter import messagebox
import pathlib
import create_wallet
from tkinter import filedialog
import dataFromApi

wallet_file = ""
resources=[]
base_currency = None

def create_new_wallet(wind):
    global wallet_file
    wallet_name = filedialog.asksaveasfilename(parent=wind,
                                        initialdir=os.getcwd(),
                                        title="Create your wallet file:",
                                        filetypes= [('database', '.db')])
    wallet_file = wallet_name + ".db"
    create_wallet.create_database(wallet_file)
    wind.destroy()
    create_main_window()
    
    
def load_data(filename):
    connention = sqlite3.connect(filename)
    cursor = connention.cursor()
    cursor.execute("SELECT * FROM wallet")
    global resources
    resources = cursor.fetchall()
    print(resources)

def load_wallet(wind):
    global wallet_file
    wallet_name = filedialog.askopenfilename(parent=wind,
                                        initialdir=os.getcwd(),
                                        title="Open your wallet file file:",
                                        filetypes= [('database', '.db')])
    load_data(wallet_name)
    wallet_file = wallet_name
    wind.destroy()
    create_main_window()

def print_resources():
    labels_resources = []
    print_resources_window = tkinter.Tk()
    print_resources_window.title("Resources")
    resources
    print(resources)
    for resource in resources:
        labels_resources.append(tkinter.Label(print_resources_window, text=("Currency: %s Amount: %f" % (resource[0],resource[1]))))

    for label in labels_resources:
        label.pack(side="top")
    
    print_resources_window.mainloop()

def setBase(base, window):
    global base_currency
    if base == "USD" or base == "PLN":
        base_currency = base
        window.destroy()
    else:
        messagebox.showinfo("Set result","Wrong currency - Choose one from [USD,PLN]")

def calculateValue(currency,amount):
    if next(iter(dataFromApi.parsedData("https://bitbay.net/API/Public/{0}{1}/ticker.json".format(currency,base_currency)))) == 'code':
        if(dataFromApi.parsedData("https://api.bittrex.com/api/v1.1/public/getticker?market={}-{}".format(base_currency, currency)))['success'] == False: 
            if next(iter(dataFromApi.parsedData("https://api.binance.com/api/v3/ticker/bookTicker?symbol={}T{}".format(currency, base_currency)))) == 'code':
                print()
            else:
                return float(dataFromApi.parsedData("https://api.binance.com/api/v3/ticker/bookTicker?symbol={}T{}".format(currency, base_currency))['bidPrice'])*amount
        else:
            return float((dataFromApi.parsedData("https://api.bittrex.com/api/v1.1/public/getticker?market={}-{}".format(base_currency, currency)))['result']['Bid'])*amount
    else:
         return float(dataFromApi.parsedData("https://bitbay.net/API/Public/{0}{1}/ticker.json".format(currency,base_currency))['bid'])*amount
        

def checkExistance(currency):
    if next(iter(dataFromApi.parsedData("https://bitbay.net/API/Public/{}{}/ticker.json".format(currency, base_currency)))) == 'code':
        if(dataFromApi.parsedData("https://api.bittrex.com/api/v1.1/public/getticker?market={}-{}".format(base_currency, currency)))['success'] == False: 
            if next(iter(dataFromApi.parsedData("https://api.binance.com/api/v3/ticker/bookTicker?symbol={}T{}".format(currency, base_currency)))) == 'code':
                return True
            else:
                return False

def set_base_currency():
    set_base_currency_window = tkinter.Tk()
    set_base_currency_window.geometry("200x100")
    set_base_currency_window.title("Base currency")
    set_base = tkinter.Entry(set_base_currency_window)
    set_base_label = tkinter.Label(set_base_currency_window, text = "Set base currency [USD,PLN]")
    set_base.place(x=10,y=40)
    set_base_label.place(x=10,y=5)
    set_button = tkinter.Button(set_base_currency_window, text="Set", command=lambda: setBase(set_base.get(), set_base_currency_window))
    set_button.place( height=30, width=40,x=75,y=60)
    set_base_currency_window.mainloop()

def addResource(currency, amount, window):
    found = False
    if base_currency == None:
        messagebox.showinfo("Error","Set a base currency first")
        found = True
        window.destroy()
    elif checkExistance(currency):
        messagebox.showinfo("Error","This market doesn't exist")
        found = True
    else:
        for resource in resources:
            if currency == resource[0]:
                messagebox.showinfo("Error","This currency already in resources")
                found = True
    if found == False:
        resources.append((currency,float(amount)))
        connection = sqlite3.connect(wallet_file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO wallet VALUES (?,?)",
                       (currency, amount))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success","Resource added.")
    window.destroy()

def add_resource():

    add_resource_window = tkinter.Tk()
    add_resource_window.geometry("150x200")
    add_resource_window.title("Add resource")
    resource_currency = tkinter.Entry(add_resource_window)
    resource_currency_label = tkinter.Label(add_resource_window, text = "Currency")
    resource_currency.place(x=10,y=40)
    resource_currency_label.place(x=10,y=5)
    resource_amount = tkinter.Entry(add_resource_window)
    resource_amount_label = tkinter.Label(add_resource_window, text = "Amount")
    resource_amount.place(x=10,y=90)
    resource_amount_label.place(x=10,y=65)
    add_button = tkinter.Button(add_resource_window, text="Add", command=lambda: addResource(resource_currency.get(), resource_amount.get(), add_resource_window))
    add_button.place( height=30, width=40,x=65,y=120)
    add_resource_window.mainloop()

def deleteResource(currency,window):
    found = False
    for resource in resources:
        if currency == resource[0]:
            resources.remove((currency,resource[1]))
            connection = sqlite3.connect(wallet_file)
            cursor = connection.cursor()
            cursor.execute('DELETE FROM wallet WHERE currency=?',(currency,))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success","Deleted successfully.")
            found = True
            window.destroy()
    if found == False:
        messagebox.showinfo("Error","No such currency. Impossible to delete")
        window.destroy()
    


def delete_resource():
    delete_resource_window = tkinter.Tk()
    delete_resource_window.geometry("150x100")
    delete_resource_window.title("Delete resource")
    resource_currency = tkinter.Entry(delete_resource_window)
    resource_currency_label = tkinter.Label(delete_resource_window, text = "Currency")
    resource_currency.place(x=10,y=40)
    resource_currency_label.place(x=10,y=5)
    delete_button = tkinter.Button(delete_resource_window, text="Delete", command=lambda: deleteResource(resource_currency.get(), delete_resource_window))
    delete_button.place( height=30, width=40,x=65,y=70)
    delete_resource_window.mainloop()

def modifyResource(currency, amount, window):
   for resource in resources:
        if currency == resource[0]:
            connection = sqlite3.connect(wallet_file)
            cursor = connection.cursor()
            cursor.execute('UPDATE wallet SET amount = ? WHERE currency = ?', (amount,currency,))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success","Updated successfully.")
            window.destroy()

def modify_resource():
    modify_resource_window = tkinter.Tk()
    modify_resource_window.geometry("150x200")
    modify_resource_window.title("Modify resource")
    resource_currency = tkinter.Entry(modify_resource_window)
    resource_currency_label = tkinter.Label(modify_resource_window, text = "Currency")
    resource_currency.place(x=10,y=40)
    resource_currency_label.place(x=10,y=5)
    resource_amount = tkinter.Entry(modify_resource_window)
    resource_amount_label = tkinter.Label(modify_resource_window, text = "Amount")
    resource_amount.place(x=10,y=90)
    resource_amount_label.place(x=10,y=65)
    modify_button = tkinter.Button(modify_resource_window, text="Modify", command=lambda: modifyResource(resource_currency.get(), resource_amount.get(), modify_resource_window))
    modify_button.place( height=30, width=40,x=65,y=130)
    modify_resource_window.mainloop()

def print_value():
    if base_currency == None:
        messagebox.showinfo("Error", "Set base currency first")
    else:
        print_value_window = tkinter.Tk()
        print_value_window.geometry("150x60")
        print_value_window.title("Wallet value")
        value = 0
        for resource in resources:
            value += float(calculateValue(resource[0],resource[1]))
        value_label =  tkinter.Label(print_value_window, text = ("Value of wallet: %d %s" % (value,base_currency)))
        value_label.place(x=40,y=20)
        print_value_window.mainloop()

def create_main_window():
    window = tkinter.Tk()
    window.title("Virtual Wallet")
    window.geometry("250x260")
    see_resources_button = tkinter.Button(window, text="See resources", command=lambda: print_resources())
    see_resources_button.place( height=30, width=120,x=65,y=20)
    set_base_currency_button = tkinter.Button(window, text="Set base currency", command=lambda: set_base_currency())
    set_base_currency_button.place( height=30, width=120,x=65,y=60)
    add_resource_button = tkinter.Button(window, text="Add resource", command=lambda: add_resource())
    add_resource_button.place( height=30, width=120,x=65,y=100)
    delete_resource_button = tkinter.Button(window, text="Delete resource", command=lambda: delete_resource())
    delete_resource_button.place( height=30, width=120,x=65,y=140)
    modify_resource_button = tkinter.Button(window, text="Modify resource", command=lambda: modify_resource())
    modify_resource_button.place( height=30, width=120,x=65,y=180)
    show_wallet_value_button = tkinter.Button(window, text="Show wallet value", command=lambda: print_value())
    show_wallet_value_button.place( height=30, width=120,x=65,y=220)

    
    window.mainloop()

def create_start_window():
    window = tkinter.Tk()
    window.title("Virtual Wallet")
    window.geometry("250x100")
    create_wallet_button = tkinter.Button(window, text="Create new wallet", command=lambda: create_new_wallet(window))
    create_wallet_button.place( height=30, width=120,x=65,y=20)
    load_wallet_button = tkinter.Button(window, text="Load wallet", command=lambda: load_wallet(window))
    load_wallet_button.place( height=30, width=120,x=65,y=60)
    
    window.mainloop()


if __name__ == "__main__":
    create_start_window()
    #checkExistance("CCC")
    #base_currency = "BTC"
    #print(calculateValue("BTC",0.1))
    