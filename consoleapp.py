import click
from wallet import Wallet
import apiBroker

w = Wallet('USD', 'wallet.db')


@click.group()
def cli():
    pass


@cli.command()
def show_state():
    """Show state of the wallet"""
    for resource in w.wallet:
        click.echo(f"{resource}: {w.wallet[resource]}\n")


@cli.command()
@click.option('-n', '--new', is_flag=True, help="add completely new resource")
@click.argument('resource')
@click.argument('amount', type=float)
def add_resource(resource, amount, new):
    """Add resource to the wallet"""
    if apiBroker.api_supports_resource(resource):
        if new:
            w.add_new_resource(resource, base_amount=amount)
        else:
            w.add_resources(resource, amount)
    else:
        print(f"resource {resource} not supported")

@cli.command()
@click.argument('resource')
@click.argument('amount', type=float)
def lower_resource(resource, amount):
    """lower an amount of resource in the wallet"""
    if resource in w.wallet.keys():
        w.remove_resources(resource, amount)
    else:
        print("No such resource in the wallet")


@cli.command()
@click.argument('resource')
def remove_resource(resource):
    """remove resource from the wallet"""
    if resource in w.wallet.keys():
        w.remove_resource_from_wallet(resource)
    else:
        print("No such resource in the wallet")

@cli.command()
@click.argument('resource')
@click.argument('amount')
def set_resource(resource, amount):
    """set resource to a given amount"""
    if resource in w.wallet.keys():
        w.set_resource_state(resource, amount)


@cli.command()
@click.argument('currency')
def check_value_in(currency):
    """Evaluate value of wallet in given currency"""
    w.eval_wallet_value(currency)


if __name__ == '__main__':
    cli()
