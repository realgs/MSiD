import csv
import tkinter
import tkinter.messagebox
import wallet
import api

my_wallet = []
empty_wallet = []
DEFAULT_CURRENCY = 'USD'
window = tkinter.Tk()


# to mój feature dla użytkownika, myślę, że przejrzyste gui może znacząco ułatwić używanie aplikacji :)
def gui():
    window.geometry("300x340")
    window.title("API application")
    menu_label = tkinter.Label(window, text="Menu", font=("Sans-serif", 13), anchor='e')
    menu_label.grid(row=0, column=0, padx=90, pady=5, sticky='n')
    menu_button_first = tkinter.Button(window, text="Show wallet", command=lambda: first_button())
    menu_button_first.grid(row=1, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_second = tkinter.Button(window, text="Add new currency", command=lambda: second_button())
    menu_button_second.grid(row=2, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_third = tkinter.Button(window, text="Remove currency", command=lambda: third_button())
    menu_button_third.grid(row=3, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_fourth = tkinter.Button(window, text="Edit currency amount", command=lambda: fourth_button())
    menu_button_fourth.grid(row=4, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_fifth = tkinter.Button(window, text="Add amount to currency", command=lambda: fifth_button())
    menu_button_fifth.grid(row=5, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_sixth = tkinter.Button(window, text="Convert wallet", command=lambda: sixth_button())
    menu_button_sixth.grid(row=6, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_seventh = tkinter.Button(window, text="Make empty wallet",
                                         command=lambda: wallet.save_wallet_to_file(empty_wallet))
    menu_button_seventh.grid(row=7, column=0, padx=90, pady=5, sticky='nwse')
    menu_button_eighth = tkinter.Button(window, text="Exit", command=window.quit)
    menu_button_eighth.grid(row=8, column=0, padx=90, pady=5, sticky='nwse')


def first_button():
    my_wallet = wallet.read_wallet_data()
    wallet_str = wallet.print_wallet(my_wallet)

    tkinter.messagebox.showinfo('Wallet', wallet_str)


def second_button():
    global my_wallet
    try:
        my_wallet = wallet.read_wallet_data()
    except:
        tkinter.messagebox.showinfo('Error!', 'Check your csv file.')

    second_window = tkinter.Toplevel()
    second_window.geometry("300x170")
    second_window.title("Adding new currency")
    window.protocol("WM_DELETE_WINDOW", window.quit())

    currency_label = tkinter.Label(second_window, text="Enter currency name:", font=("Sans-serif", 13), anchor='e')
    currency_field = tkinter.Entry(second_window)
    amount_label = tkinter.Label(second_window, text="Enter amount:", font=("Sans-serif", 13), anchor='e')
    amount_field = tkinter.Entry(second_window)
    add_currency_button = tkinter.Button(second_window, text="Add currency",
                                         command=lambda: second_button_helper(currency_field, amount_field, my_wallet))

    currency_label.grid(row=0, column=0, pady=(40, 0))
    currency_field.grid(row=0, column=1, pady=(40, 0))
    amount_label.grid(row=1, column=0)
    amount_field.grid(row=1, column=1)
    add_currency_button.grid(columnspan=2)

    second_window.mainloop()


def second_button_helper(currency_field, amount_field, my_wallet):
    currency = str(currency_field.get()).upper()
    amount = amount_field.get()
    try:
        if api.check_availability_in_api(DEFAULT_CURRENCY, currency):
            wallet.add_currency(currency, float(amount), my_wallet)
        else:
            tkinter.messagebox.showinfo('Error!', 'Currency is not available in API.')
            return
    except ValueError:
        tkinter.messagebox.showinfo('Error!', 'Wrong amount.')
        return
    tkinter.messagebox.showinfo('Info', 'Currency added.')


def third_button():
    global my_wallet
    try:
        my_wallet = wallet.read_wallet_data()
    except:
        tkinter.messagebox.showinfo('Error!', 'Check your csv file.')

    third_window = tkinter.Toplevel()
    third_window.geometry("300x170")
    third_window.title("Removing currency")
    window.protocol("WM_DELETE_WINDOW", window.quit())

    currency_label = tkinter.Label(third_window, text="Enter currency name:", font=("Sans-serif", 13), anchor='e')
    currency_field = tkinter.Entry(third_window)
    add_currency_button = tkinter.Button(third_window, text="Remove currency",
                                         command=lambda: third_button_helper(currency_field, my_wallet))

    currency_label.grid(row=0, column=0, pady=(40, 0))
    currency_field.grid(row=0, column=1, pady=(40, 0))
    add_currency_button.grid(columnspan=2)

    third_window.mainloop()


def third_button_helper(currency_field, my_wallet):
    currency = str(currency_field.get()).upper()
    if wallet.check_currency_in_wallet(currency, my_wallet):
        wallet.remove_currency(currency, my_wallet)
        tkinter.messagebox.showinfo('Info', 'Currency removed.')
    else:
        tkinter.messagebox.showinfo('Info', 'There is no such currency in your wallet.')


def fourth_button():
    global my_wallet
    try:
        my_wallet = wallet.read_wallet_data()
    except:
        tkinter.messagebox.showinfo('Error!', 'Check your csv file.')

    fourth_window = tkinter.Toplevel()
    fourth_window.geometry("300x170")
    fourth_window.title("Editing amount of currency")
    window.protocol("WM_DELETE_WINDOW", window.quit())

    currency_label = tkinter.Label(fourth_window, text="Enter currency name:", font=("Sans-serif", 13), anchor='e')
    currency_field = tkinter.Entry(fourth_window)
    amount_label = tkinter.Label(fourth_window, text="Enter amount:", font=("Sans-serif", 13), anchor='e')
    amount_field = tkinter.Entry(fourth_window)
    add_currency_button = tkinter.Button(fourth_window, text="Edit currency amount",
                                         command=lambda: fourth_button_helper(currency_field, amount_field, my_wallet))

    currency_label.grid(row=0, column=0, pady=(40, 0))
    currency_field.grid(row=0, column=1, pady=(40, 0))
    amount_label.grid(row=1, column=0)
    amount_field.grid(row=1, column=1)
    add_currency_button.grid(columnspan=2)

    fourth_window.mainloop()


def fourth_button_helper(currency_field, amount_field, my_wallet):
    currency = str(currency_field.get()).upper()
    amount = amount_field.get()
    if wallet.check_currency_in_wallet(currency, my_wallet):
        try:
            wallet.edit_currency_amount(currency, float(amount), my_wallet)
        except ValueError:
            tkinter.messagebox.showinfo('Error!', 'Wrong amount.')
        tkinter.messagebox.showinfo('Info', 'Currency amount edited.')
    else:
        tkinter.messagebox.showinfo('Info', 'There is no such currency in your wallet.')


def fifth_button():
    global my_wallet
    try:
        my_wallet = wallet.read_wallet_data()
    except:
        tkinter.messagebox.showinfo('Error!', 'Check your csv file.')

    fifth_window = tkinter.Toplevel()
    fifth_window.geometry("300x170")
    fifth_window.title("Adding amount to currency")
    window.protocol("WM_DELETE_WINDOW", window.quit())

    currency_label = tkinter.Label(fifth_window, text="Enter currency name:", font=("Sans-serif", 13), anchor='e')
    currency_field = tkinter.Entry(fifth_window)
    amount_label = tkinter.Label(fifth_window, text="Enter amount:", font=("Sans-serif", 13), anchor='e')
    amount_field = tkinter.Entry(fifth_window)
    add_currency_button = tkinter.Button(fifth_window, text="Add amount to currency",
                                         command=lambda: fifth_button_helper(currency_field, amount_field, my_wallet))

    currency_label.grid(row=0, column=0, pady=(40, 0))
    currency_field.grid(row=0, column=1, pady=(40, 0))
    amount_label.grid(row=1, column=0)
    amount_field.grid(row=1, column=1)
    add_currency_button.grid(columnspan=2)

    fifth_window.mainloop()


def fifth_button_helper(currency_field, amount_field, my_wallet):
    currency = str(currency_field.get()).upper()
    amount = amount_field.get()
    if wallet.check_currency_in_wallet(currency, my_wallet):
        try:
            wallet.add_currency_amount(currency, float(amount), my_wallet)
        except ValueError:
            tkinter.messagebox.showinfo('Error!', 'Wrong amount.')
        tkinter.messagebox.showinfo('Info', 'Currency amount edited.')
    else:
        tkinter.messagebox.showinfo('Info', 'There is no such currency in your wallet.')


def sixth_button():
    global my_wallet
    try:
        my_wallet = wallet.read_wallet_data()
    except:
        tkinter.messagebox.showinfo('Error!', 'Check your csv file.')

    sixth_window = tkinter.Toplevel()
    sixth_window.geometry("480x180")
    sixth_window.title("Converting wallet")
    window.protocol("WM_DELETE_WINDOW", window.quit())

    info_label = tkinter.Label(sixth_window, text="If you won't entry any currency it will be used default one - USD",
                               font=("Sans-serif", 13), anchor='e')
    currency_label = tkinter.Label(sixth_window, text="Enter currency name:", font=("Sans-serif", 13), anchor='e')
    currency_field = tkinter.Entry(sixth_window)
    add_currency_button = tkinter.Button(sixth_window, text="Convert wallet",
                                         command=lambda: sixth_button_helper(currency_field))

    info_label.grid(columnspan=2, pady=(40, 0))
    currency_label.grid(row=1, column=0)
    currency_field.grid(row=1, column=1)
    add_currency_button.grid(columnspan=2)

    sixth_window.mainloop()


def sixth_button_helper(currency_field):
    currency = str(currency_field.get()).upper()
    if currency == None:
        currency = DEFAULT_CURRENCY
    try:
        converted_wallet = wallet.convert_wallet(my_wallet, currency)
    except:
        tkinter.messagebox.showinfo('Error!', 'Something went wrong. It is possible that the wallet'
                                              ' cannot be converted to the currency of your choice')
        return
    tkinter.messagebox.showinfo('Wallet', converted_wallet)


def run():
    csv.register_dialect('semicolons', delimiter=';')
    gui()
    window.mainloop()


if __name__ == "__main__":
    run()
