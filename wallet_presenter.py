import wallet_viewer as viewer
import wallet_model as wallet


'''
TODO:
1. auto-save data
2. load data at startup
3. auto-refresh values
'''

def add_currency(currency, amount):
    if wallet.add_currency(currency, float(amount)):
        update_view_display()
    else:
        viewer.error_display("Currency doesn't exist in this exchange")

def set_currency(currency, amount):
    add_currency(currency, amount)

def remove_currency(currency):
    if wallet.remove_currency(currency):
        update_view_display()
    else:
        viewer.error_display("You don't have such currency")

def set_base_currency(currency):
    if wallet.set_base_currency(currency):
        #update_view_display()
        print()
    else:
        viewer.error_display("Currency doesn't exist in this exchange")
        viewer.get_base_currency_dialog()

def update_view_display():
    wallet_data = wallet.get_wallet_data()
    wallet_display_text = ""
    print(wallet_data['data'])
    for currency, info in wallet_data['data'].items():
        wallet_display_text += "{}: {:.4f}  |  {:.4f} {}\n".format(currency, info['amount'], info['value'], wallet_data['base_currency'])
    viewer.update_display(wallet_display_text)

def update_database():
    print()

def update_currencies_value():
    print()

def thread():
    #TODO
    update_database()
    update_currencies_value()

def main():
    viewer.create_main_window()

if __name__ == "__main__":
    main()
