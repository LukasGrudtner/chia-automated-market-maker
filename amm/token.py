from driver import clsp, rpc, utils, wallet
from amm.definitions import *
import json
import asyncio
import time


#TODO: Extract duplicated code
def deploy():
    clsp.build([TOKEN_PROGRAM], TOKEN_PROGRAM_INCLUDES)
    token_puzzlehash = clsp.curry(program=f'{TOKEN_PROGRAM}.hex',
                                args=[str(INITIAL_RELATION)],
                                include=TOKEN_PROGRAM_INCLUDES,
                                treehash=True)
    save_puzzlehash(token_puzzlehash)
    token_address = utils.encode(token_puzzlehash, prefix='txch')
    wallet.send(amount=0, target=token_address, override=True)
    coin_records = fetch_coin_records(token_puzzlehash)

    print('Coin records')
    print(json.dumps(coin_records, sort_keys=True, indent=4))
    print('XCH smart coin deployed successfully!')
    print()


def fetch_coin_records(coin_puzzlehash: str, as_name_dict: bool = False) -> dict:
    coin_records = asyncio.run(rpc.coinrecords([coin_puzzlehash], as_name_dict))

    while len(coin_records) == 0:
        print('Transaction not confirmed in blockchain yet. Trying again in 10 seconds...')
        time.sleep(10)
        coin_records = asyncio.run(rpc.coinrecords([coin_puzzlehash], as_name_dict))

    return coin_records


def save_puzzlehash(puzzlehash: str):
    config = load_config()
    config['puzzlehash'] = puzzlehash
    save_config(config)


def save_config(config: dict) -> None:
    file = open(TOKEN_CONFIG_PATH, 'w')
    file.write(json.dumps(config, sort_keys=True, indent=4))
    file.close()


def load_config() -> dict:
    file = open(TOKEN_CONFIG_PATH, 'r')
    config = json.loads(file.read())
    file.close()

    if config is None:
        return {}
    return config
