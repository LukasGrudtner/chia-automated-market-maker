from chia.util.bech32m import encode_puzzle_hash, decode_puzzle_hash


def encode(puzzle_hash: str, prefix: str = None) -> str:
    return encode_puzzle_hash(bytes.fromhex(puzzle_hash), prefix)


def decode(address: str) -> str:
    return decode_puzzle_hash(address).hex()