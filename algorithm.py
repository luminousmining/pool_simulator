class ALGORITHM:
    ETHASH = 'ethash'
    KAWPOW = 'kawpow'


def is_valid_algorithm(algo: str) -> bool:
    if algo == ALGORITHM.ETHASH:
        return True
    elif algo == ALGORITHM.KAWPOW:
        return True
    return False
