class ALGORITHM:
    ETHASH = 'ethash'
    KAWPOW = 'kawpow'
    BLAKE3 = 'blake3'


def is_valid_algorithm(algo: str) -> bool:
    if algo == ALGORITHM.ETHASH:
        return True
    elif algo == ALGORITHM.KAWPOW:
        return True
    elif algo == ALGORITHM.BLAKE3:
        return True
    return False
