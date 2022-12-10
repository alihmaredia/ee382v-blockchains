import requests
import json
import datetime
import pandas as pd
from termcolor import colored


def BTCaccount(address):
    if len(address) < 26:
        print('\n Sorry, that wasn\'t quite long enough.')
        from menu import account
        account()
    else:
        print(colored('Should just take a few moments...\n', 'yellow'))
        data = get_data(address)
        printaccountdata(address, data)
        return address

def printaccountdata(address, r):
    total_received = (r.get('total_received')) / 100000000
    total_sent = (r.get('total_sent')) / 100000000
    final_balance = (r.get('final_balance')) / 100000000
    number_of_transactions = r.get('n_tx')
    sanction_status = ofac(address)

    coin = 'btc'
    currency = 'usd'
    from coingecko import price
    convert = price(coin.lower(), currency.lower())

    print(f'Address: {address}')
    print(f'Total Received: {total_received:.8f} {coin.upper()} ${total_received * convert:,.2f} {currency.upper()}')
    print(f'Total Sent: {total_sent:.8f} {coin.upper()} ${total_sent * convert:,.2f} {currency.upper()}')
    print(f'Current Balance: {final_balance:.8f} {coin.upper()} ${final_balance * convert:,.2f} {currency.upper()}')
    print(f'Total Transactions: {number_of_transactions}')

    if sanction_status[0]:
        print(colored('This address in on the list of OFAC sanctioned Bitcoin addresses!', 'red'))
        printinfo = input(colored('Do you want to find the sanctioned entity? (Y/N):\n', 'blue'))
        if printinfo.upper() == "Y" or printinfo.upper() == "YES":
            print(sanction_status[1])

    return r


def accounttransactions(r, txs, addr):

    addr_list = []
    transaction_list = r['txs']
    keyerror = False
    error_list = []
    i = 0 
    dataframe_list = []
    empty_data_frame = pd.DataFrame({'A': [' '], 'B': [' '], 'C': [' '], 'D': [' ']})
    
    for transaction_data in transaction_list:

        hashid = transaction_data['hash']
        tx_time = datetime.datetime.fromtimestamp(transaction_data['time'])
        result = (transaction_data['result']) / 100000000

        df = pd.DataFrame(
        [
            ['Transaction:', 'Transaction Hash ID:', 'Time of Transaction:',
             'Amount traded by this address:'], [(i + 1), hashid, tx_time, result]
        ],
        columns=list('ABCD'), index=['1', '2']
        )

        dataframe_list.append(df)

        dataframe_list[i] = pd.concat((dataframe_list[i], empty_data_frame), ignore_index=True)

        input_list = transaction_data['inputs']

        index = pd.DataFrame({'A': ['Input:'], 'B': ['Address:'], 'C': ['Value:'], 'D': ['Spent:']})
        dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

        for input_data in input_list:
            input_data_list = input_data['prev_out']

            input_index = (input_data['index'] + 1)
            input_address = input_data_list['addr']
            input_value = -(input_data_list['value']) / 100000000
            input_spent = input_data_list['spent']

            if input_address != addr:
                addr_list.append(input_address)

            index = pd.DataFrame({'A': [input_index], 'B': [input_address], 'C': [input_value], 'D': [input_spent]})
            dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

        dataframe_list[i] = pd.concat((dataframe_list[i], empty_data_frame), ignore_index=True)
        index = pd.DataFrame({'A': ['Output:'], 'B': ['Address:'], 'C': ['Value:'], 'D': ['Spent:']})
        dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

        output_list = transaction_data['out']
        output_index = 0

        for output_data in output_list:
            output_index += 1

            try:
                output_address = output_data['addr']
            except KeyError:
                output_address = 'error'
                keyerror = True
                error_list.append('Transaction: {} Output: {}'.format(i, output_index))

            output_value = output_data['value'] / 100000000
            output_spent = output_data['spent']

            if keyerror:
                pass
            elif output_address != addr:
                addr_list.append(output_address)

            index = pd.DataFrame({'A': [output_index], 'B': [output_address], 'C': [output_value], 'D': [output_spent]})
            dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

        i += 1

    if keyerror:
        print('\nError occurred, could not find address for: ')
        print(error_list)

    linkedaddrs = addrcount(addr_list)
    print('\n', (len(linkedaddrs.index)), 'Potentially linked addresses found.')

    export = input(colored('\nPlease confirm if you want the transaction data exported. (Y/N):\n', 'blue'))

    if export.upper() == "Y" or export.upper() == "YES":
        i = 0

        with pd.ExcelWriter(addr + ".xlsx") as writer:
            i = 0
            if len(linkedaddrs.index) > 0:
                linkedaddrs.to_excel(writer, sheet_name='Linked Addresses', index=True)

            for i, tx in enumerate(dataframe_list, start=1):
                tx.to_excel(writer, sheet_name=("Transaction %d" % i), index=False)

        print(
            '\The export can be found in the current directory.\n \nIt is named:\n' +
            addr + '.xlsx')
    
    return addr_list


def get_data(address):
    url = f'https://blockchain.info/rawaddr/{address}'
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def getTransactions(address, numTransactions):
    url = f'https://blockchain.info/rawaddr/{address}?limit={numTransactions}'
    response = requests.get(url).json()
    return response


def addrcount(addresses):
    address_count = {}
    for address in addresses:
        if address in address_count:
            address_count[address] += 1
        else:
            address_count[address] = 1
    address_count_df = pd.DataFrame.from_dict(address_count, orient='index', columns=['Count'])
    address_count_df.sort_values(by=['Count'], ascending=False, inplace=True)
    return address_count_df


def ofac(addr):
    url = 'https://cryptofac.org/api/?q=' + addr
    response = requests.get(url).json()
    if response[0]['match']:
        return [response[0]['match'], response[0]['entity']]
    else:
        return [response[0]['match']]

