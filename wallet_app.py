import tkinter
import sys
import os
import sqlite3
from tkinter import messagebox
import pathlib
import create_wallet
from tkinter import filedialog

wallet_file = ""
resources=[]
base_currency = None

def create_new_wallet(wind):
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
    resources = cursor.fetchall()
    print(resources)

def load_wallet(wind):
    wallet_name = filedialog.askopenfilename(parent=wind,
                                        initialdir=os.getcwd(),
                                        title="Open your wallet file file:",
                                        filetypes= [('database', '.db')])
    load_data(wallet_name)
    wallet_file = wallet_name
    wind.destroy()
    create_main_window()

def print_resources():
    labels_resource = []
    print_resources_window = tkinter.Tk()

    for resource in resources:
        labels_resources.append(tkinter.Label(print_log_window, text=("Currency: %s Amount: %d" % (resource[0],resource[1]))))

    for label in labels_resources:
        label.pack(side="top")
    
    print_resources_window.mainloop()

def create_main_window():
    window = tkinter.Tk()
    window.title("Virtual Wallet")
    window.geometry("250x260")
    see_resources_button = tkinter.Button(window, text="See resources", command=lambda: print_resources())
    see_resources_button.place( height=30, width=120,x=65,y=20)
    set_base_currency_button = tkinter.Button(window, text="Set base currency", command=lambda: print("Set base currency"))
    set_base_currency_button.place( height=30, width=120,x=65,y=60)
    add_resource_button = tkinter.Button(window, text="Add resource", command=lambda: print("Add resource"))
    add_resource_button.place( height=30, width=120,x=65,y=100)
    delete_resource_button = tkinter.Button(window, text="Delete resource", command=lambda: print("Delete resource"))
    delete_resource_button.place( height=30, width=120,x=65,y=140)
    modify_resource_button = tkinter.Button(window, text="Modify resource", command=lambda: print("Modify resource"))
    modify_resource_button.place( height=30, width=120,x=65,y=180)
    show_wallet_value_button = tkinter.Button(window, text="Show wallet value", command=lambda: print("Show wallet value"))
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
    