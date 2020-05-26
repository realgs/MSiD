import config
import wallet
def main():
    end = False
    while not end:
        print("input 0 - set basic currency")
        print("input 1 - make new wallet")
        print("input 2 - update currency or add new")
        print("input 3 - get all money in inputted currency")
        print("input 4 - delete quantity of chosen currency")
        print("input 5 - exit")
        try:
            action_choice = int(input("your input: "))
            if (action_choice == 0):
                wallet.setBasicCurrency()
            elif (action_choice == 1):
                wallet.make_new_wallet()
            elif(action_choice == 2):
                wallet.updateCurrencyByAdding()
            elif(action_choice == 3):
                print("all money: " + str(wallet.getAllMoneyInChosenCurrency()) + " " + config.basic_currency)
            elif(action_choice == 4):
                wallet.deleteCurrecyQuantity()
            elif(action_choice == 5):
                end = True
        except ValueError:
            print("input a NUMBER!!!")
main()