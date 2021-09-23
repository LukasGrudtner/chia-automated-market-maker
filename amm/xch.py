import json
import asyncio

from amm import service
from amm import transaction
from amm.definitions import *
from driver import clsp, rpc, utils, wallet


def deploy():
    clsp.build([XCH_PROGRAM], XCH_PROGRAM_INCLUDES)
    xch_puzzlehash = clsp.curry(program=f'{XCH_PROGRAM}.hex',
                                args=[],
                                include=XCH_PROGRAM_INCLUDES,
                                treehash=True)

    save_puzzlehash(xch_puzzlehash)
    save_puzzle_reveal()

    xch_address = utils.encode(xch_puzzlehash, prefix='txch')
    wallet.send(amount=0, target=xch_address, override=True)
    coin_records = service.fetch_coin_records(xch_puzzlehash)

    print('Coin records')
    print(json.dumps(coin_records, sort_keys=True, indent=4))
    print('XCH smart coin deployed successfully!')
    print()


def deposit(amount: int, receive_address: str):
    spend_bundle = generate_spend_bundle(amount, receive_address)
    asyncio.run(rpc.pushtx([json.dumps(spend_bundle)]))


def generate_spend_bundle(amount: int, receive_address: str) -> dict:
    xch_puzzlehash = load_config()['puzzlehash']

    # coin_id = get_coin_id(xch_puzzlehash)
    xch_coin_id, xch_coin = service.retrieve_coin_with_amount(xch_puzzlehash, minimum_amount=0)

    xch_coin_spend = generate_coin_spend(amount, receive_address, xch_coin)

    transaction_coin_spend = transaction.generate_coin_spend(amount, xch_coin_id)

    return {
        'coin_spends': [xch_coin_spend, transaction_coin_spend],
        'aggregated_signature': DEFAULT_AGGREGATED_SIGNATURE
    }


def generate_coin_spend(amount: int, receive_address: str, coin: dict) -> dict:
    config = service.load_config(path=XCH_CONFIG_PATH)
    puzzle_reveal = config['puzzle_reveal']
    xch_puzzlehash = config['puzzlehash']

    coin['parent_coin_info'] = service.remove_suffix(coin['parent_coin_info'], '0x')
    coin['puzzle_hash'] = service.remove_suffix(coin['puzzle_hash'], '0x')

    return {
        'coin': coin,
        'puzzle_reveal': puzzle_reveal,
        'solution': clsp.solution([int(coin['amount']), amount + int(coin['amount']), bytes.fromhex(xch_puzzlehash)])
    }


def solution(my_amount: int, new_amount: int, my_puzzlehash: str):
    return clsp.solution([my_amount, new_amount, bytes.fromhex(my_puzzlehash)])


def show(unspent: bool = False):
    config = service.load_config(path=XCH_CONFIG_PATH)
    service.show(config, unspent)


def save_puzzlehash(puzzlehash: str):
    config = service.load_config(path=XCH_CONFIG_PATH)
    config['puzzlehash'] = puzzlehash
    service.save_config(path=XCH_CONFIG_PATH, config=config)


def save_puzzle_reveal():
    puzzle_reveal = clsp.curry(program=XCH_PROGRAM,
                               args=[],
                               include=XCH_PROGRAM_INCLUDES,
                               dump=True)

    print(f'xch puzzle reveal = {puzzle_reveal}')

    config = service.load_config(path=XCH_CONFIG_PATH)
    config['puzzle_reveal'] = puzzle_reveal
    service.save_config(path=XCH_CONFIG_PATH, config=config)
