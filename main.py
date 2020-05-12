import dataOperations


def start():
    print("Functions :\n"
          "\t1 - Display currencies\n"
          "\t2 - Check value\n"
          "\t3 - Add currency\n"
          "\t4 - Delete currency\n"
          "\t5 - Change existing currencies\n"
          "\t6 - List apis\n"
          "\t7 - Change apis(this will reset your wallet)")
    user_input = input("Input: ")
    if user_input == "1":
        dataOperations.display_currencies()
    elif user_input == "2":
        if not dataOperations.display_value():
            print("Error while requesting order books")
    elif user_input == "3":
        inp = input("Input type and quantity with whitespace: ")
        inp = inp.split(' ')
        if dataOperations.add_currency(inp[0], float(inp[1])):
            print("Successfully added")
        else:
            print("Currency type is not tradable")
    elif user_input == "4":
        inp = input("Input type: ")
        dataOperations.del_currency(inp)
    elif user_input == "5":
        currency_type = input('Input type: ')
        if dataOperations.check_currency(currency_type):
            inp = input('Input new quantity: ')
            dataOperations.modify_currency(currency_type, float(inp))
        else:
            print('Currency not found')
    elif user_input == "6":
        dataOperations.display_exchanges()
    elif user_input == "7":
        apis = input("Input apis with whitespaces between:")
        apis = apis.split(' ')
        dataOperations.change_apis(apis)
    else:
        exit(0)


if __name__ == '__main__':
    print("Hello there: ")
    while True:
        start()
