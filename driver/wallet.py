import os


def send(amount: int, target: str, override: bool = False) -> None:
    override_option = '--override' if override else ''
    amount_xch = amount / 1000000000000 if amount > 0 else 0
    command = f'chia wallet send -a {amount_xch} -t {target} {override_option}'
    os.system(command)