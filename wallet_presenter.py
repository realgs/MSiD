import threading
import time
import wallet_viewer as viewer
import wallet_model as wallet

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

def change_currency_amount(currency, amount):
    if wallet.change_currency_amount(currency, float(amount)):
        update_view_display()
    else:
        viewer.error_display("You don't have such currency")

def set_base_currency(currency):
    if wallet.set_base_currency(currency):
        print()
    else:
        viewer.error_display("Currency doesn't exist in this exchange")
        viewer.get_base_currency_dialog()

def update_data():
    wallet.update_database()


def update_view_display():
    wallet_data = wallet.get_wallet_data()
    wallet_display_text = ""
    sum = 0
    for currency, info in wallet_data['data'].items():
        wallet_display_text += "{}: {:.4f}  |  {:.4f} {}\n".format(currency, info['amount'], info['value'], wallet_data['base_currency'])
        sum += info['value']
    wallet_display_text += "\n\nIn total: {:.4f} {}".format(sum, wallet_data['base_currency'])
    viewer.update_display(wallet_display_text)

def run(wallet_data):
    while True:
        time.sleep(5)
        wallet.update_database(wallet_data)
        wallet.update_currencies_values(wallet_data)
        update_view_display()

def main():
    if wallet.load_database() == True:
        wallet.update_currencies_values()
        update_view_display()
    else:
        viewer.get_base_currency_dialog()
    threading.Thread(target=run, args=(wallet.get_wallet_data(),)).start()
    viewer.create_main_window()

if __name__ == "__main__":
    main()
