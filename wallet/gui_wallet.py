import tkinter as tk

import config
import wallet

def create_main_window():
    window = tk.Tk()
    button_basic_curr = tk.Button(window, text="SET BASIC CURRENCY",
                              command=lambda: wallet.setBasicCurrency(), height=2, width=25)
    button_basic_curr.grid(row=1, column=0)

    button_new_wall = tk.Button(window, text="MAKE NEW WALLET",
                              command=lambda: wallet.make_new_wallet(), height=2, width=25)
    button_new_wall.grid(row=2, column=0)

    button_add = tk.Button(window, text="UPDATE CURRECY/ADD NEW",
                              command=lambda: wallet.updateCurrencyByAdding(), height=2, width=25)
    button_add.grid(row=3, column=0)
    button_all_money = tk.Button(window, text="GET ALL MONEY",
                              command=lambda: print("all money: " + str(wallet.getAllMoneyInChosenCurrency()) + " " + config.basic_currency), height=2, width=25)
    button_all_money.grid(row=1, column=1)
    button_del = tk.Button(window, text="DELETE QUANTITY",
                              command=lambda: wallet.deleteCurrecyQuantity(), height=2, width=25)
    button_del.grid(row=2, column=1)
    button_exit = tk.Button(window, text="EXIT",
                              command=window.quit, height=2, width=25)
    button_exit.grid(row=3, column=1)
    tk.mainloop()


create_main_window()