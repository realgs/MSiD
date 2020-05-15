import click
from wallet import Wallet

w = Wallet('USD', 'wallet.db')

w.add_resources('USD', 20)


@click.group()
def cli():
    pass


@click.command()
def show_state():
    """Show state of the wallet"""
    for resource in w.wallet:
        click.echo(f"{resource}: {w.wallet[resource]}\n")


@click.command()
@click.option('-n', '--new', is_flag=True, help="add completely new resource")
@click.argument('resource')
@click.argument('amount', type=float)
def add_resource(resource, amount, new):
    """Add resource to the wallet"""
    if new:
        w.add_new_resource(resource, base_amount=amount)
    else:
        w.add_resources(resource, amount)


cli.add_command(show_state)
cli.add_command(add_resource)

if __name__ == '__main__':
    cli()
