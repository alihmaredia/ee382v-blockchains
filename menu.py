from termcolor import colored


# Here we need to ask the user for their address.
def account():
    valid = False
    while not valid:
        address = input(colored('\nWhat is the address you would like to analyze? \n', 'blue'))
        if len(address) < 26:
            print('\n Sorry, that wasn\'t quite long enough.')
            valid = False
        else:
            valid = True
    return address


# Here we need to ask the user if they want to grab transactions.
def accountmenu(address):

    print(colored('\nWhat shall we proceed with next?', 'green'))
    options = {
        '1': 'Collect this Bitcoin address\'s transactions',
        '2': 'Go back',
        '3': 'Exit'
    }
    for key, value in options.items():
        print(f'({key}) {value}')
    selection = input(colored('\nPlease enter your choice (1-3):\n', 'blue'))

    if selection == '1':
        max_num_transactions = input(
             colored('\nWhat is the max number of transactions?\n', 'blue'))
        print(colored('Should just take a few moments...', 'yellow'))
        collect_transactions(address, max_num_transactions)

    elif selection == '2':
        from main import main
        main()

    elif selection == '3':
        quit()

    else:
        print('\n \nSorry, you entered an invalid option.')
        accountmenu(address)


# Collect the transactions
def collect_transactions(addr, max_num_transactions):
    from data import getTransactions
    from data import accounttransactions
    r = getTransactions(addr, max_num_transactions)
    accounttransactions(r, max_num_transactions, addr)
    return
