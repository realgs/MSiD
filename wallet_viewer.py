from tkinter import simpledialog, messagebox
import wallet_presenter as presenter
import tkinter as tk


window = tk.Tk()
wallet_info = tk.StringVar(value="")

def add_currency_dialog():
    currency = simpledialog.askstring('Data', 'Enter the currency you want to add', parent=window)
    amount = simpledialog.askstring('Data', 'Enter currency amount', parent=window)
    presenter.add_currency(currency, amount)

def set_currency_dialog():
    currency = simpledialog.askstring('Data', 'Enter the currency you want to modify', parent=window)
    amount = simpledialog.askstring('Data', 'Enter new currency amount', parent=window)
    presenter.set_currency(currency, amount)

def remove_currency_dialog():
    currency = simpledialog.askstring('Data', 'Enter the currency u want to remove', parent=window)
    presenter.remove_currency(currency, amount)

def get_base_currency_dialog():
    currency = simpledialog.askstring('Data', 'Enter the base currency', parent=window)
    if currency is not None and currency != '':
        presenter.set_base_currency(currency)
        #base_currency.set(value=f'Base currency: {wallet.base_currency}')

def update_display(wallet_display_text):
    basic_info = "Currency: Amount | Value\n"
    wallet_info.set(basic_info + wallet_display_text)

def error_display(error_info):
    messagebox.askyesno("Error info", "")
    messagebox.showerror(title="Error", message=error_info)

def create_main_window():
    window.title("WALLET")

    get_base_currency_dialog()
    lb_wallet_info = tk.Label(window, textvariable=wallet_info)
    btn_add_currency = tk.Button(window, text='Add currency', command=add_currency_dialog)
    btn_set_currency = tk.Button(window, text='Modify currency', command=set_currency_dialog)
    btn_remove_currency = tk.Button(window, text='Remove currency', command=remove_currency_dialog)
    btn_add_currency.pack()
    btn_set_currency.pack()
    btn_remove_currency.pack()
    lb_wallet_info.pack()

    window.mainloop()

create_main_window()
