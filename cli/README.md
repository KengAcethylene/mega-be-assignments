# ERC20Helper CLI Description

---

## How to use this program

Following the step

-   Clone the project
-   Create `.env` file in `cli` folder
-   Copy .env format in `.env.example`
-   In `RPC_ENDPOINT` variable, you need to register [Infura](https://infura.io/) account, create infura project and get the rpc endpoint.
-   In `ETHPLORER_API_KEY` variable, you need to register [Ethplorer](https://ethplorer.io/) account and get the api key.
-   IN `ETHSCAN_API_KEY` variable, you need to register [Etherscan](https://etherscan.io/) get the api key.
-   Change directory to `cli` folder, using command `cd cli`
-   Install dependencies, using command

```shell
pip3 install -r requirements.txt
```

-   Run program, using command

```shell
python3 main.py [OPTIONS] COMMAND [ARGS]...
```

## Avaliable Command

Use `python main.py --help` for helper

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  ERC20 Helper, CLI program for someone who hates GUI on Etherscan!!!

Options:
  --help  Show this message and exit.

Commands:
  balanceOf  Show the balanceOf TARGET_ADDRESS on the CONTRACT_ADDRESS
  detail     Show name, symbol and decimals of CONTRACT_ADDRESS
  holders    Generate current top N holders to a text file
  latest_tx  Generate Latest N transaction of CONTRACT_ADDRESS to a file
  watch_tx   Subscribe Tx from the CONTRACT_ADDRESS in watching mode
```

> In command `watch_tx`, if you want to exit, you can use keyboard interupt with `ctrl + c`
