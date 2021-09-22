import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
from amm import xch, usd, token, transaction


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@click.group(
    "deploy",
    short_help="Deploy smart coin"
)
def deploy_cmd():
    pass


@deploy_cmd.command(
    "xch",
    short_help="Deploy XHC smart coin"
)
def deploy_xch_cmd() -> None:
    xch.deploy()


@deploy_cmd.command(
    "usd",
    short_help="Deploy USD smart coin"
)
def deploy_usd_cmd() -> None:
    pass


@deploy_cmd.command(
    "transaction",
    short_help="Deploy transaction smart coin"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount of mojos"
)
def deploy_transaction_cmd(amount: str) -> None:
    transaction.deploy(int(amount))


@click.group(
    "deposit",
    short_help="Make a deposit to AMM"
)
def deposit_cmd():
    pass


@deposit_cmd.command(
    "xch",
    short_help="Deposit XHC"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount"
)
def deposit_xch_cmd(amount: str) -> None:
    pass


@deposit_cmd.command(
    "usd",
    short_help="Deposit USD"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount"
)
def deposit_usd_cmd(amount: str) -> None:
    pass


@click.group(
    "withdraw",
    short_help="Withdraw money from AMM"
)
def withdraw_cmd():
    pass


@withdraw_cmd.command(
    "xch",
    short_help="Withdraw XHC"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount"
)
def withdraw_xch_cmd(amount: str) -> None:
    pass


@withdraw_cmd.command(
    "usd",
    short_help="Withdraw USD"
)
@click.option(
    "-a",
    "--amount",
    required=True,
    help="Amount"
)
def withdraw_usd_cmd(amount: str) -> None:
    pass


cli.add_command(deploy_cmd)
cli.add_command(deposit_cmd)
cli.add_command(withdraw_cmd)


def main() -> None:
    cli()


if __name__ == '__main__':
    main()
