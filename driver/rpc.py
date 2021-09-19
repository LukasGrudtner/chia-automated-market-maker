import aiohttp
import json

from typing import Dict, Optional, List
from pprint import pprint

from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.config import load_config
from chia.util.ints import uint16
from chia.util.byte_types import hexstr_to_bytes
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_record import CoinRecord

from cdv.cmds.util import fake_context
from cdv.cmds.chia_inspect import do_inspect_spend_bundle_cmd


async def get_client() -> Optional[FullNodeRpcClient]:
    try:
        config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
        self_hostname = config["self_hostname"]
        full_node_rpc_port = config["full_node"]["rpc_port"]
        full_node_client = await FullNodeRpcClient.create(
            self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
        )
        return full_node_client
    except Exception as e:
        if isinstance(e, aiohttp.ClientConnectorError):
            pprint(f"Connection error. Check if full node is running at {full_node_rpc_port}")
        else:
            pprint(f"Exception from 'harvester' {e}")
        return None


async def coinrecords(values: List[str], as_name_dict: bool = False):
    coin_record_dicts: List[Dict]

    try:
        node_client: FullNodeRpcClient = await get_client()
        clean_values: bytes32 = map(lambda hex: hexstr_to_bytes(hex), values)
        coin_records: List[CoinRecord] = await node_client.get_coin_records_by_puzzle_hashes(clean_values)
        coin_record_dicts = [rec.to_json_dict() for rec in coin_records]
    finally:
        node_client.close()
        await node_client.await_closed()

    if as_name_dict:
        cr_dict = {}
        for record in coin_record_dicts:
            cr_dict[Coin.from_json_dict(record["coin"]).name().hex()] = record
        return cr_dict
    else:
        return coin_record_dicts


async def pushtx(spendbundles: List[str]):
    try:
        node_client: FullNodeRpcClient = await get_client()
        # It loads the spend bundle using cdv inspect
        for bundle in do_inspect_spend_bundle_cmd(fake_context(), spendbundles, print_results=False):
            try:
                result: Dict = await node_client.push_tx(bundle)
                print(json.dumps(result, sort_keys=True, indent=4))
            except ValueError as e:
                pprint(str(e))
    finally:
        node_client.close()
        await node_client.await_closed()