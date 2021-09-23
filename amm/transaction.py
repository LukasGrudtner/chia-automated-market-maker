import json

from amm import service
from amm.definitions import *
from driver import clsp, rpc, utils, wallet


def deploy(amount: int):
    clsp.build([TRANSACTION_PROGRAM], TRANSACTION_PROGRAM_INCLUDES)
    transaction_puzzlehash = clsp.curry(program=f'{TRANSACTION_PROGRAM}.hex',
                                        args=[],
                                        include=TRANSACTION_PROGRAM_INCLUDES,
                                        treehash=True)

    save_puzzlehash(transaction_puzzlehash)
    save_puzzle_reveal()

    transaction_address = utils.encode(transaction_puzzlehash, prefix='txch')
    wallet.send(amount=amount, target=transaction_address, override=True)
    coin_records = service.fetch_coin_records(transaction_puzzlehash)

    print('Coin records')
    print(json.dumps(coin_records, sort_keys=True, indent=4))
    print('Transaction smart coin deployed successfully!')
    print()


def generate_coin_spend(amount: int, coin_id: str) -> dict:
    config = service.load_config(path=TRANSACTION_CONFIG_PATH)
    puzzle_reveal = config['puzzle_reveal']
    transaction_puzzlehash = config['puzzlehash']

    transaction_coin = service.retrieve_coin_with_amount(transaction_puzzlehash, amount)
    transaction_coin['parent_coin_info'] = service.remove_suffix(transaction_coin['parent_coin_info'], '0x')
    transaction_coin['puzzle_hash'] = service.remove_suffix(transaction_coin['puzzle_hash'], '0x')

    return {
        'coin': transaction_coin,
        'puzzle_reveal': puzzle_reveal,
        'solution': clsp.solution([bytes.fromhex(coin_id), amount])
    }


def show(unspent: bool = False):
    config = service.load_config(path=XCH_CONFIG_PATH)
    service.show(config, unspent)


def save_puzzlehash(puzzlehash: str):
    config = service.load_config(path=TRANSACTION_CONFIG_PATH)
    config['puzzlehash'] = puzzlehash
    service.save_config(path=TRANSACTION_CONFIG_PATH, config=config)


def save_puzzle_reveal():
    puzzle_reveal = clsp.curry(program=TRANSACTION_PROGRAM,
                               args=[],
                               include=TRANSACTION_PROGRAM_INCLUDES,
                               dump=True)
    config = service.load_config(path=TRANSACTION_CONFIG_PATH)
    config['puzzle_reveal'] = puzzle_reveal
    service.save_config(path=TRANSACTION_CONFIG_PATH, config=config)
