import json
import asyncio

from amm import service
from amm import transaction
from amm.definitions import *
from driver import clsp, rpc, utils, wallet


def deploy(version: str) -> None:
    clsp.build([XCH_PROGRAM], XCH_PROGRAM_INCLUDES)
    xch_puzzlehash = clsp.curry(program=f'{XCH_PROGRAM}.hex',
                                args=[version],
                                include=XCH_PROGRAM_INCLUDES,
                                treehash=True)

    save_puzzlehash(xch_puzzlehash)
    save_puzzle_reveal(version)

    xch_address = utils.encode(xch_puzzlehash, prefix='txch')
    wallet.send(amount=0, target=xch_address, override=True)
    coin_records = service.fetch_coin_records(xch_puzzlehash)

    print('Coin records')
    print(json.dumps(coin_records, indent=4))
    print('XCH smart coin deployed successfully!')
    print()


def deposit(amount: int):
    spend_bundle = generate_spend_bundle(amount)
    asyncio.run(rpc.pushtx([json.dumps(spend_bundle)]))


def generate_spend_bundle(amount: int) -> dict:
    xch_puzzlehash = load_config()['puzzlehash']

    xch_coin_id, xch_coin = service.retrieve_coin_with_amount(xch_puzzlehash, minimum_amount=0)
    xch_coin_spend = generate_coin_spend(amount, xch_coin)

    transaction_coin_spend = transaction.generate_coin_spend(amount, xch_coin_id)

    return {
        'coin_spends': [xch_coin_spend, transaction_coin_spend],
        'aggregated_signature': DEFAULT_AGGREGATED_SIGNATURE
    }


def generate_coin_spend(amount: int, coin: dict) -> dict:
    config = load_config()
    puzzle_reveal = config['puzzle_reveal']
    xch_puzzlehash = config['puzzlehash']

    coin['parent_coin_info'] = service.remove_suffix(coin['parent_coin_info'], '0x')
    coin['puzzle_hash'] = service.remove_suffix(coin['puzzle_hash'], '0x')

    current_amount = int(coin['amount'])
    new_amount = current_amount + amount

    return {
        'coin': coin,
        'puzzle_reveal': puzzle_reveal,
        'solution': solution(current_amount, new_amount, xch_puzzlehash)
    }


def solution(my_amount: int, new_amount: int, my_puzzlehash: str):
    return clsp.solution([
        my_amount,
        new_amount,
        bytes.fromhex(my_puzzlehash)
    ])


def show(unspent: bool = False):
    config = load_config()
    service.show(config, unspent)


def save_puzzlehash(puzzlehash: str):
    config = load_config()
    config['puzzlehash'] = puzzlehash
    save_config(config)


def save_puzzle_reveal(version: str = XCH_DEFAULT_VERSION):
    puzzle_reveal = clsp.curry(program=XCH_PROGRAM,
                               args=[version],
                               include=XCH_PROGRAM_INCLUDES,
                               dump=True)

    config = load_config()
    config['puzzle_reveal'] = puzzle_reveal
    save_config(config)


def load_config():
    return service.load_config(path=XCH_CONFIG_PATH)


def save_config(config: dict) -> None:
    service.save_config(path=XCH_CONFIG_PATH, config=config)