class ALGORITHM:
    SMART_MINING = 'smart_mining'
    ETHASH = 'ethash'
    KAWPOW = 'kawpow'
    MEOWPOW = 'meowpow'
    BLAKE3 = 'blake3'


def is_valid_algorithm(algo: str) -> bool:
    if algo == ALGORITHM.SMART_MINING:
        return True
    elif algo == ALGORITHM.ETHASH:
        return True
    elif algo == ALGORITHM.KAWPOW:
        return True
    elif algo == ALGORITHM.MEOWPOW:
        return True
    elif algo == ALGORITHM.BLAKE3:
        return True
    return False
