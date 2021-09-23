from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.program import Program
from chia.types.condition_opcodes import ConditionOpcode
from chia.util.ints import uint64
from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

from cdv.util.load_clvm import load_clvm

XCH_MOD = load_clvm("xch.clsp", "smartcoins")


def create_xch_puzzle(initial_relation: float):
    return XCH_MOD.curry(initial_relation)


def solution_for_xch():
    pass
