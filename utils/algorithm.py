class ALGORITHM:
    SMART_MINING = 'smart_mining'
    ETHASH = 'ethash'
    KAWPOW = 'kawpow'
    MEOWPOW = 'meowpow'
    QUAIPOW = 'quaipow'
    BLAKE3 = 'blake3'
    AUTOLYKOS_V2 = 'autolykos_v2'
    WORKFLOW = 'workflow'

    @classmethod
    def values(cls):
        return [v for k, v in vars(cls).items() if not k.startswith('_') and isinstance(v, str)]
