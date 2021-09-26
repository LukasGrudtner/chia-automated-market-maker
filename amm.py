import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
from amm import xch, usd, token, transaction
from amm import definitions


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@click.group(
    "xch",
    short_help="XCH smart coin commands"
)
def xch_cmd():
    pass


@xch_cmd.command(
    "deploy",
    short_help="Deploy XHC smart coin"
)
@click.option(
    "-v",
    "--version",
    required=False,
    default=definitions.XCH_DEFAULT_VERSION,
    help="XCH deploy version"
)
def xch_deploy_cmd(version: str) -> None:
    xch.deploy(version)


@xch_cmd.command(
    "deposit",
    short_help="Deposit to XCH smart coin"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount of mojos"
)
def xch_deposit_cmd(amount: str) -> None:
    xch.deposit(int(amount))


@xch_cmd.command(
    "withdraw",
    short_help="Withdraw from XCH smart coin"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount of mojos"
)
def xch_withdraw_cmd() -> None:
    pass


@xch_cmd.command(
    "show",
    short_help="Show XCH smart coin information"
)
@click.option(
    "--unspent/--spent",
    required=False,
    default=False,
    help="Filter unspent smart coins"
)
def xch_show_cmd(unspent: bool) -> None:
    xch.show(unspent)


@click.group(
    "usd",
    short_help="USD smart coin commands"
)
def usd_cmd() -> None:
    pass


@usd_cmd.command(
    "deploy",
    short_help="Deploy USD smart coin"
)
def usd_deploy_cmd() -> None:
    pass


@usd_cmd.command(
    "deposit",
    short_help="Deposit to USD smart coin"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount of mojos"
)
def usd_deposit_cmd() -> None:
    pass


@usd_cmd.command(
    "withdraw",
    short_help="Withdraw from USD smart coin"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount of mojos"
)
def usd_withdraw_cmd() -> None:
    pass


@usd_cmd.command(
    "show",
    short_help="Show USD smart coin information"
)
@click.option(
    "--unspent/--spent",
    required=False,
    default=False,
    help="Filter unspent smart coins"
)
def usd_show_cmd(unspent: bool) -> None:
    pass


@click.group(
    "transaction",
    short_help="Transaction smart coin commands"
)
def transaction_cmd() -> None:
    pass


@transaction_cmd.command(
    "deploy",
    short_help="Deploy transaction smart coin"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount of mojos"
)
def transaction_deploy_cmd(amount: str) -> None:
    transaction.deploy(int(amount))


@transaction_cmd.command(
    "show",
    short_help="Show transaction smart coin information"
)
@click.option(
    "--unspent/--spent",
    required=False,
    default=False,
    help="Filter unspent smart coins"
)
def transaction_show_cmd(unspent: bool) -> None:
    transaction.show(unspent)


@click.group(
    "token",
    short_help="Token smart coin commands"
)
def token_cmd():
    pass


@token_cmd.command(
    "deploy",
    short_help="Deploy Token smart coin"
)
def token_deploy_cmd() -> None:
    token.deploy()

@token_cmd.command(
    "show",
    short_help="Show Token smart coin information"
)
@click.option(
    "--unspent/--spent",
    required=False,
    default=False,
    help="Filter unspent smart coins"
)
def token_show_cmd(unspent: bool) -> None:
    token.show(unspent)


cli.add_command(xch_cmd)
cli.add_command(usd_cmd)
cli.add_command(transaction_cmd)
cli.add_command(token_cmd)


def main() -> None:
    cli()


if __name__ == '__main__':
    main()
