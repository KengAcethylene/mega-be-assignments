from web3 import Web3
from dotenv import load_dotenv, find_dotenv
from os import environ
from utils import erc20_ABI, int_to_unit
load_dotenv(find_dotenv())
provider = Web3(Web3.HTTPProvider(environ.get('RPC_ENDPOINT')))
# provider = Web3(Web3.WebsocketProvider(environ.get('WSC_ENDPOINT')))


def cli_detail(contract_address: str):
    if (Web3.isAddress(contract_address)):
        try:
            erc20token = provider.eth.contract(
                address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

            name = erc20token.functions.name().call()
            symbol = erc20token.functions.symbol().call()
            decimal = erc20token.functions.decimals().call()

            return f'name : {name},\nsymbol : {symbol},\ndecimal : {decimal},'
        except Exception:
            return "Invalid contract address, Maybe it isn't ERC20 Token address"
    else:
        return "Invalid Input Address"


def cli_balanceOf(contract_address: str, target_address: str):
    if (Web3.isAddress(contract_address) and Web3.isAddress(target_address)):
        try:
            erc20token = provider.eth.contract(
                address=Web3.toChecksumAddress(contract_address), abi=erc20_ABI)

            balance_wei = erc20token.functions.balanceOf(
                Web3.toChecksumAddress(target_address)).call()
            decimal = erc20token.functions.decimals().call()
            balance_decimal = Web3.fromWei(balance_wei, int_to_unit[decimal])

            return f'balanceof : {balance_decimal}'
        except Exception:
            return "Invalid contract address, Maybe it isn't ERC20 Token address"
    else:
        return "Invalid Input Contract Address or Target Address"


def cli_watch_tx(contract_address: str):
    if (Web3.isAddress(contract_address)):
        try:
            while True:
                print(provider.eth.filter(
                    {'fromBlock': 'latest', "address": Web3.toChecksumAddress(contract_address)}).get_new_entries())
            return f'Valid'
        except Exception:
            return "Error"
    else:
        return "Invalid Input Contract Address or Target Address"


def cli_latest_tx():
    pass


def cli_holder():
    pass
