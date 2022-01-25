import imp
import json
from web3 import Web3
from dotenv import load_dotenv, find_dotenv
from os import environ
from utils import erc20_ABI, int_to_unit
import requests

load_dotenv(find_dotenv())

#global vars
RPC_ENDPOINT = ''
ETHPLORER_API_KEY = ''
provider = ''
ETHPLORER_API_URL = "https://api.ethplorer.io"


def check_env() -> bool:
    global RPC_ENDPOINT
    global ETHPLORER_API_KEY
    global provider

    RPC_ENDPOINT = environ.get('RPC_ENDPOINT')
    ETHPLORER_API_KEY = environ.get('ETHPLORER_API_KEY')
    if (bool(RPC_ENDPOINT and ETHPLORER_API_KEY)):
        provider = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
        return provider.isConnected()
    else:
        return False


def cli_detail(contract_address: str) -> str:
    try:
        global provider
        erc20token = provider.eth.contract(
            address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

        name = erc20token.functions.name().call()
        symbol = erc20token.functions.symbol().call()
        decimal = erc20token.functions.decimals().call()

        return f'name : {name},\nsymbol : {symbol},\ndecimal : {decimal},'

    except ValueError:
        return "Invalid CONTRACT_ADDRESS"

    except Exception:
        return "CONTRACT_ADDRESS isn't ERC20 Token address"


def cli_balanceOf(contract_address: str, target_address: str) -> str:
    try:
        global provider
        erc20token = provider.eth.contract(
            address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

        balance_wei = erc20token.functions.balanceOf(
            Web3.toChecksumAddress(target_address)).call()
        decimal = erc20token.functions.decimals().call()
        balance_decimal = Web3.fromWei(balance_wei, int_to_unit[decimal])

        return f'balanceof : {balance_decimal}'

    except ValueError:
        return "Invalid CONTRACT_ADDRESS or TRAGET_ADDRESS"

    except Exception:
        return "CONTRACT_ADDRESS isn't ERC20 Token address"


def cli_watch_tx(contract_address: str) -> str:
    try:
        global provider
        is_printed_waiting = False
        while True:
            tx_fromBlock = provider.eth.filter(
                {'fromBlock': 'latest', "address": Web3.toChecksumAddress(contract_address)}).get_new_entries()
            tx_set = set()
            if tx_fromBlock:
                for tx in tx_fromBlock:
                    tx_hash = tx['transactionHash'].hex()
                    if tx_hash not in tx_set:
                        print(f'{environ.get("TX_URL")}{tx_hash}')
                        tx_set.add(tx_hash)
                        is_printed_waiting = False
            else:
                if not is_printed_waiting:
                    print("Waiting new transactions ...")
                    is_printed_waiting = True
    except ValueError:
        return "Invalid CONTRACT_ADDRESS"
    except Exception as e:
        return str(e)


def cli_latest_tx(N: str, contract_address: str):
    try:
        params = {

        }
    except ValueError:
        return "Invalid N or CONTRACT_ADDRESS"
    except Exception as e:
        return str(e)


def cli_holder(contract_address: str, N: str = '10') -> str:
    try:
        global ETHPLORER_API_KEY
        global ETHPLORER_API_URL

        # * input validation
        n = int(N)
        contract_address = Web3.toChecksumAddress(contract_address)

        # * url and params for the request
        url = f'{ETHPLORER_API_URL}/getTopTokenHolders/{contract_address}'
        params = {
            'apiKey': ETHPLORER_API_KEY,
            'limit': n,
        }

        resp = requests.get(url, params=params).json()

        if resp.get('error'):
            return resp.get('error').get('message')
        else:
            with open('top_holders.json', 'w+') as f:
                data = [{'address': temp.get('address'), 'balance': temp.get(
                    'balance')} for temp in resp.get('holders')]
                json.dump(data, f)
            return "Updated top_holders.json success"

    except ValueError:
        return "Invalid N or CONTRACT_ADDRESS"
    except Exception as e:
        return str(e)
