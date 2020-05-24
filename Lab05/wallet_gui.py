from tkinter import simpledialog, messagebox
import wallet_app as wallet
import tkinter as tk


window = tk.Tk()
wallet_info = tk.StringVar()


def update_wallet_info():
    wallet_info.set(value=wallet.get_wallet_info())


def add_currency_dialog():
    currency = simpledialog.askstring('Currency', 'Enter the currency', parent=window)
    amount = simpledialog.askfloat('Amount', 'Enter the amount', parent=window)
    if currency is not None and currency != '' and amount is not None:
        currency = currency.upper()
        if wallet.add_currency(currency, amount):
            update_wallet_info()
        else:
            messagebox.showerror('Error', f'{currency}-{wallet.base_currency} market isn\'t available!')


def remove_currency_dialog():
    currency = simpledialog.askstring('Currency', 'Enter the currency', parent=window)
    amount = simpledialog.askfloat('Amount', 'Enter the amount', parent=window)
    if currency is not None and currency != '' and amount is not None:
        currency = currency.upper()
        if wallet.remove_currency(currency, amount):
            update_wallet_info()
        else:
            messagebox.showerror('Error', f'You have no {currency} in your wallet!')


def update_currency_dialog():
    currency = simpledialog.askstring('Currency', 'Enter the currency', parent=window)
    amount = simpledialog.askfloat('Amount', 'Enter the amount', parent=window)
    if currency is not None and currency != '' and amount is not None:
        currency = currency.upper()
        if wallet.update_currency(currency, amount):
            update_wallet_info()
        else:
            messagebox.showerror('Error', f'You have no {currency} in your wallet!')


def set_base_currency_dialog():
    currency = simpledialog.askstring('Base currency', 'Enter the base currency', parent=window)
    if currency is not None and currency != '':
        wallet.set_base_currency(currency)


def create_main_window():
    window.title("WALLET")

    set_base_currency_dialog()

    lbl_base_currency = tk.Label(window, text=f'Base currency: {wallet.base_currency}')
    lbl_base_currency.grid(column=0)

    update_wallet_info()
    lbl_wallet_info = tk.Label(window, textvariable=wallet_info)
    lbl_wallet_info.grid(column=0)

    btn_add_currency = tk.Button(window, text='Add currency', command=add_currency_dialog)
    btn_add_currency.grid(column=0)

    btn_remove_currency = tk.Button(window, text='Remove currency', command=remove_currency_dialog)
    btn_remove_currency.grid(column=0)

    btn_remove_update = tk.Button(window, text='Update currency', command=update_currency_dialog)
    btn_remove_update.grid(column=0)

    btn_refresh = tk.Button(window, text='Refresh', command=update_wallet_info)
    btn_refresh.grid(column=0)


def run_gui():
    create_main_window()
    window.mainloop()


if __name__ == '__main__':
    run_gui()
    exit()
