import click
from functions import cli_detail, cli_balanceOf, cli_watch_tx


@click.group()
def cli():
    """ERC20 Helper, CLI program for someone who hates GUI on Etherscan!!!"""
    pass


@click.command(help="Show name, symbol and decimals of CONTRACT_ADDRESS")
@click.argument('contract_address')
def detail(contract_address):
    response = cli_detail(contract_address)
    click.echo(response)


@click.command(help="Show the balanceOf TARGET_ADDRESS on the CONTRACT_ADDRESS in decimals format")
@click.argument('contract_address')
@click.argument('target_address')
def balanceOf(contract_address, target_address):
    response = cli_balanceOf(contract_address, target_address)
    click.echo(response)


@click.command(name="watch_tx")
@click.argument('contract_address')
def watch_tx(contract_address):
    response = cli_watch_tx(contract_address)
    click.echo(response)


cli.add_command(detail)
cli.add_command(balanceOf)
cli.add_command(watch_tx)


if __name__ == '__main__':
    cli()
