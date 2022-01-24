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
