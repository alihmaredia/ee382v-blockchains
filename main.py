from termcolor import colored


def main():
    print(colored('\nPlease select an option from the list below:', 'green'))
    print(colored('(1) Analyze a Bitcoin address'))
    print('(2) Exit\n')

    choice = int(input((colored('Enter your option: \n', 'blue'))))

    if choice == 1:
        from menu import account
        addr = account()
        from data import BTCaccount
        BTCaccount(addr)
        from menu import accountmenu
        accountmenu(addr)

    elif choice == 2:
        quit()

    else:
        print(colored('\nSorry, you entered an invalid option.\n', 'red'))
        main()

if __name__ == "__main__":
    main()
