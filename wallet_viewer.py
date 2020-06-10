from tkinter import simpledialog, messagebox
import wallet_presenter as presenter
import tkinter as tk


window = tk.Tk()
wallet_info = tk.StringVar(value="")

def simple_dialog(msg, function):
    output = []
    for request in msg:
        output.append(simpledialog.askstring('Data', request, parent=window))
        if output[-1] == None:
            return False
    function(*output)
    return True

def add_currency_dialog():
    simple_dialog(['Enter the currency you want to add', 'Enter currency amount'], presenter.add_currency)

def set_currency_dialog():
    simple_dialog(['Enter the currency you want to modify', 'Enter new currency amount'], presenter.set_currency)

def change_currency_amount_dialog():
    simple_dialog(['Enter the currency you want to modify', 'Enter currency modification amount'], presenter.change_currency_amount)

def remove_currency_dialog():
    simple_dialog(['Enter the currency u want to remove'], presenter.remove_currency)

def get_base_currency_dialog():
    currency = simpledialog.askstring('Data', 'Enter the base currency', parent=window)
    if currency is not None and currency != '':
        presenter.add_currency(currency)

def update_display(wallet_display_text):
    basic_info = "Currency: Amount | Value\n"
    wallet_info.set(basic_info + wallet_display_text)

def error_display(error_info):
    messagebox.showerror(title="Error", message=error_info)

def create_main_window():
    window.title("Crypto wallet")
    window.geometry("250x300")

    lb_wallet_info = tk.Label(window, textvariable=wallet_info)
    btn_add_currency = tk.Button(window, text='Add currency', command=add_currency_dialog)
    btn_set_currency = tk.Button(window, text='Set currency amount', command=set_currency_dialog)
    btn_change_currency_amount =tk.Button(window, text='Change currency amount', command=change_currency_amount_dialog)
    btn_remove_currency = tk.Button(window, text='Remove currency', command=remove_currency_dialog)
    btn_add_currency.pack()
    #btn_set_currency.pack()
    btn_change_currency_amount.pack()
    btn_remove_currency.pack()
    lb_wallet_info.pack()

    window.mainloop()
