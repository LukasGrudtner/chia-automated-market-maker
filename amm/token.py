from driver import clsp, rpc, utils, wallet
from amm.definitions import *
import json
import asyncio
import time
from amm import service


def deploy():
    clsp.build([TOKEN_PROGRAM], TOKEN_PROGRAM_INCLUDES)
    token_puzzlehash = clsp.curry(program=f'{TOKEN_PROGRAM}.hex',
                                  args=[str(TOKEN_ID)],
                                  include=TOKEN_PROGRAM_INCLUDES,
                                  treehash=True)

    save_puzzlehash(token_puzzlehash)
    save_puzzle_reveal()

    token_address = utils.encode(token_puzzlehash, prefix='txch')
    wallet.send(amount=0, target=token_address, override=True)
    coin_records = service.fetch_coin_records(token_puzzlehash)

    print('Coin records')
    print(json.dumps(coin_records, indent=4))
    print('Token smart coin deployed successfully!')
    print()


def generate_coin_spend(amount: int, provider_puzzlehash: str) -> dict:
    config = load_config()
    puzzle_reveal = config['puzzle_reveal']
    # transaction_puzzlehash = config['puzzlehash']

    token_coin_id, token_coin = service.retrieve_coin_with_amount(provider_puzzlehash, minimum_amount=0)
    token_coin['parent_coin_info'] = service.remove_suffix(token_coin['parent_coin_info'], '0x')
    token_coin['puzzle_hash'] = service.remove_suffix(token_coin['puzzle_hash'], '0x')

    current_amount = int(token_coin['amount'])
    new_amount = current_amount + amount

    return {
        'coin': token_coin,
        'puzzle_reveal': puzzle_reveal,
        'solution': clsp.solution([current_amount, new_amount, bytes.fromhex(config['puzzlehash'])])
    }


def show(unspent: bool = False):
    config = load_config()
    service.show(config, unspent)


def save_puzzlehash(puzzlehash: str):
    config = load_config()
    config['puzzlehash'] = puzzlehash
    save_config(config)


def save_puzzle_reveal():
    puzzle_reveal = clsp.curry(program=TOKEN_PROGRAM,
                               args=[str(TOKEN_ID)],
                               include=TOKEN_PROGRAM_INCLUDES,
                               dump=True)

    config = load_config()
    config['puzzle_reveal'] = puzzle_reveal
    save_config(config)


def load_config():
    return service.load_config(path=TOKEN_CONFIG_PATH)


def save_config(config: dict) -> None:
    service.save_config(path=TOKEN_CONFIG_PATH, config=config)
