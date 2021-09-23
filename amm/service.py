import time
import json
import asyncio

from driver import clsp, rpc, utils, wallet


def show(config: dict, unspent: bool = False):
    puzzlehash = config['puzzlehash']
    coin_records = fetch_coin_records(puzzlehash, as_name_dict=True)

    coin_records = dict(sorted(coin_records.items(), key=lambda x: x[1]['timestamp'], reverse=False))

    if unspent:
        coin_records = list(filter(lambda coin_record: coin_record['spent'] is False, coin_records.values()))

    print(json.dumps(coin_records, indent=4))


def retrieve_coin_with_amount(coin_puzzlehash: str, minimum_amount: int) -> tuple:
    coin_records = fetch_coin_records(coin_puzzlehash, as_name_dict=True)
    unspent_coin_records = dict([cr for cr in coin_records.items() if cr[1]['spent'] is False])
    sorted_unspent_coin_records = dict(
        sorted(unspent_coin_records.items(), key=lambda x: x[1]['timestamp'], reverse=True))
    coins_records_with_amount = dict(
        [cr for cr in sorted_unspent_coin_records.items() if cr[1]['coin']['amount'] >= minimum_amount])

    if len(coins_records_with_amount) == 0:
        raise Exception(f'No coins available with at least {minimum_amount} mojos!')

    coin_id = list(coins_records_with_amount.items())[0][0]
    coin = list(coins_records_with_amount.items())[0][1]['coin']
    return coin_id, coin


def fetch_coin_records(coin_puzzlehash: str, as_name_dict: bool = False) -> dict:
    coin_records = asyncio.run(rpc.coinrecords([coin_puzzlehash], as_name_dict))

    while len(coin_records) == 0:
        print('Transaction not confirmed in blockchain yet. Trying again in 10 seconds...')
        time.sleep(10)
        coin_records = asyncio.run(rpc.coinrecords([coin_puzzlehash], as_name_dict))

    return coin_records


def save_config(path: str, config: dict) -> None:
    file = open(path, 'w')
    file.write(json.dumps(config, sort_keys=True, indent=4))
    file.close()


def load_config(path: str) -> dict:
    file = open(path, 'r')
    config = json.loads(file.read())
    file.close()

    if config is None:
        return {}
    return config


def remove_suffix(string: str, suffix: str):
    if string.startswith(suffix):
        return string[len(suffix):]
    return string
