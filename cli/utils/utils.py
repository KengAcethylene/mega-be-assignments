from web3.contract import Contract
from os.path import join, dirname
import json

f = open(join(dirname(__file__), 'abi', 'ERC20.json'))

erc20_ABI = json.load(f)


f.close()

int_to_unit = {
    18: 'ether',
    15: 'milli',
    12: 'micro',
    9: 'gwei',
    6: 'mwei',
    3: 'kwei',
}


def decode_tx_input(input: str, contract_instance: Contract) -> dict:
    if (len(input)) == 0:
        return {}
    else:
        try:
            func, data = contract_instance.decode_function_input(input)
            data['function_name'] = str(func)
            return data
        except Exception:
            return "It isn't ERC20 Function"
