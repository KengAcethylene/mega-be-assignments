from urllib import response
import click
from functions import check_env, cli_detail, cli_balanceOf, cli_watch_tx, cli_latest_tx, cli_holder


@click.group()
def cli():
    """ERC20 Helper, CLI program for someone who hates GUI on Etherscan!!!"""
    pass


@click.command(help="Show name, symbol and decimals of CONTRACT_ADDRESS")
@click.argument('contract_address')
def detail(contract_address):
    response = cli_detail(contract_address)
    click.echo(response)


@click.command(name="balanceOf", help="Show the balanceOf TARGET_ADDRESS on the CONTRACT_ADDRESS")
@click.argument('contract_address')
@click.argument('target_address')
def balanceOf(contract_address, target_address):
    response = cli_balanceOf(contract_address, target_address)
    click.echo(response)


@click.command(name="watch_tx", help="Subscribe Tx from the CONTRACT_ADDRESS in watching mode")
@click.argument('contract_address')
def watch_tx(contract_address):
    response = cli_watch_tx(contract_address)
    click.echo(response)


@click.command(name="latest_tx")
@click.argument('N')
@click.argument('contract_address')
def latest_tx(n, contract_address):
    response = cli_latest_tx(contract_address, n)
    click.echo(response)


@click.command()
@click.argument('N')
@click.argument('contract_address')
def holders(n, contract_address):
    response = cli_holder(contract_address, n)
    click.echo(response)


cli.add_command(detail)
cli.add_command(balanceOf)
cli.add_command(watch_tx)
cli.add_command(latest_tx)
cli.add_command(holders)

if __name__ == '__main__' and check_env():
    cli()
else:
    print("Please ensure that you create .env correctly. More information is in .env.example")
