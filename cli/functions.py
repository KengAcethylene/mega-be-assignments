import json
from web3 import Web3
from dotenv import load_dotenv
from os import environ
from utils import erc20_ABI, int_to_unit, decode_tx_input
import requests

load_dotenv()

# * global vars
RPC_ENDPOINT = ''
ETHPLORER_API_KEY = ''
ETHSCAN_API_KEY = ''
provider = ''

ETHPLORER_API_URL = "https://api.ethplorer.io"
ETHSCAN_API_URL = "https://api.etherscan.io/api"
TX_URL = 'https://etherscan.io/tx/'


def check_env() -> bool:
    global RPC_ENDPOINT
    global ETHPLORER_API_KEY
    global ETHSCAN_API_KEY
    global provider

    RPC_ENDPOINT = environ.get('RPC_ENDPOINT')
    ETHPLORER_API_KEY = environ.get('ETHPLORER_API_KEY')
    ETHSCAN_API_KEY = environ.get('ETHSCAN_API_KEY')

    if (bool(RPC_ENDPOINT and ETHPLORER_API_KEY and ETHSCAN_API_KEY)):
        provider = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
        return provider.isConnected()
    else:
        return False


def cli_detail(contract_address: str) -> str:
    try:
        erc20token = provider.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

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
        erc20token = provider.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

        balance_wei = erc20token.functions.balanceOf(Web3.toChecksumAddress(target_address)).call()
        decimal = erc20token.functions.decimals().call()
        balance_decimal = Web3.fromWei(balance_wei, int_to_unit[decimal])

        return f'balanceof : {balance_decimal}'

    except ValueError:
        return "Invalid CONTRACT_ADDRESS or TRAGET_ADDRESS"

    except Exception:
        return "CONTRACT_ADDRESS isn't ERC20 Token address"


def cli_watch_tx(contract_address: str) -> str:
    try:
        is_printed_waiting = False
        while True:
            tx_fromBlock = provider.eth.filter({'fromBlock': 'latest', "address": Web3.toChecksumAddress(contract_address)}).get_new_entries()
            tx_set = set()
            if tx_fromBlock:
                for tx in tx_fromBlock:
                    tx_hash = tx['transactionHash'].hex()
                    if tx_hash not in tx_set:
                        print(f'{TX_URL}{tx_hash}')
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


def cli_latest_tx(contract_address: str, N: str = '10'):
    try:
        # * input validation
        n = int(N)
        contract_address = Web3.toChecksumAddress(contract_address)

        # * params for the request
        params = {
            "module": "account",
            "action": "txlist",
            "address": contract_address,
            "page": 1,
            "offset": n,
            "sort": "desc",
            "apikey": ETHSCAN_API_KEY
        }

        resp = requests.get(ETHSCAN_API_URL, params=params).json()
        if resp.get('status') != '1':
            return resp.get('message')
        else:
            data: list = resp.get('result')
            instance = provider.eth.contract(
                address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

            formatted_data = [{'sender': tx.get('from'), 'txHash': tx.get(
                'hash'), 'params': decode_tx_input(tx.get('input'), instance)} for tx in data]

            with open('latest_tx.json', 'w+') as f:
                json.dump(formatted_data, f)
            return "Updated latest_tx.json success"
    except ValueError:
        return "Invalid N or CONTRACT_ADDRESS"
    except Exception as e:
        return str(e)


def cli_holder(contract_address: str, N: str = '10') -> str:
    try:
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
                data = [{'address': temp.get('address'), 'balance': temp.get('balance')} for temp in resp.get('holders')]
                json.dump(data, f)
            return "Updated top_holders.json success"

    except ValueError:
        return "Invalid N or CONTRACT_ADDRESS"
    except Exception as e:
        return str(e)
