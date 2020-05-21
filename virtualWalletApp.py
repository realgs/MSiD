import wallet

baseCur = input("Wybierz podstawową walute : PLN, USD lub BTC ")
baseCur = baseCur.upper()
if baseCur not in ['PLN','USD','BTC']:
    print("Currency not supported")
    exit()

wallet = wallet.Wallet(baseCur)

def handleAdding():
    currency = input("Podaj zasób ")
    amount = input("Podaj ilość ")
    wallet.addToWallet(currency,float(amount))

def handleRemoving():
    currency = input("Podaj zasób ")
    amount = input("Podaj ilość ")
    wallet.removeFromWallet(currency,float(amount))

def handleShowing():
    wallet.showWallet()

while True:
    print()
    print("Opcje portfela:")
    print("1. by dodać zasób do portfela")
    print("2. by odjąć zasób z portfela")
    print("3. by podsumować portfel")
    print("4. by wyjść")
    choose = input("... ")
    print()
    if choose == "1":
        handleAdding()
    elif choose == "2":
        handleRemoving()
    elif choose == "3":
        handleShowing()
    elif choose == "4":
        break