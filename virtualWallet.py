import click
from wallet import Wallet
import apiBroker

w = Wallet('wallet.db')


@click.group()
def cli():
    """
    Virtual wallet app
    Try COMMAND --help to see the usage of specific commands
    """
    pass


@cli.command()
def show_state():
    """Show state of the wallet"""
    for resource in w.wallet:
        click.echo(f"{resource}: {w.wallet[resource]}")


@cli.command()
@click.option('-n', '--new', is_flag=True, help="add completely new resource")
@click.argument('resource', type=str)
@click.argument('amount', type=float)
def add_resource(resource, amount, new):
    """Add an amount of resource to the wallet, see --help for options """
    if apiBroker.api_supports_resource(resource):
        if new:
            w.add_new_resource(resource, base_amount=amount)
        else:
            if resource in w.wallet.keys():
                w.add_resources(resource, amount)
            else:
                click.echo("no such resource in wallet")
    else:
        click.echo(f"resource {resource} not supported")


@cli.command()
@click.argument('resource', type=str)
@click.argument('amount', type=float)
def lower_resource(resource, amount):
    """lower an amount of resource in the wallet"""
    if resource in w.wallet.keys():
        w.remove_resources(resource, amount)
    else:
        click.echo("No such resource in the wallet")


@cli.command()
@click.argument('resource', type=str)
def remove_resource(resource):
    """remove resource from the wallet"""
    if resource in w.wallet.keys():
        w.remove_resource_from_wallet(resource)
    else:
        click.echo("No such resource in the wallet")


@cli.command()
@click.argument('resource', type=str)
@click.argument('amount', type=float)
def set_resource(resource, amount):
    """set resource to a given amount"""
    if resource in w.wallet.keys():
        w.set_resource_state(resource, amount)


@cli.command()
@click.argument('currency', type=str)
@click.option('-o', '--omit-fee', is_flag=True, help="omit taker fee when calculating value")
def check_value_in(currency, omit_fee):
    """Evaluate value of wallet in given currency"""
    consider_fee = not omit_fee  # this exists for clarity's sake
    w.eval_wallet_value(currency, consider_fee)


if __name__ == '__main__':
    cli()
