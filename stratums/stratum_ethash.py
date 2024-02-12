import logging

from stratums import Stratum


class StratumEthash(Stratum):

    def __init__(self):
        super(StratumEthash, self).__init__()

    def on_message(self, fd: int, __socket, data: dict):
        if 'method' in data:
            self.__on_method(__socket, data)
        else:
            self.__on_response(__socket, data)

    def __on_response(self, __socket, data: dict):
        logging.info(f'response => {data}')

    def __on_method(self, __socket, data: dict):
        method = data['method']
        params = data['params']

        if method == 'mining.subscribe':
            self.__on_mining_subscribe(__socket, data['id'])
        elif method == 'mining.authorize':
            self.__on_mining_authorize(__socket, data['id'])
        elif method == 'mining.submit':
            self.__on_mining_submit(__socket, data['id'], params)
        else:
            logging.error(f'Unknow method [{method}][{params}]')

    def __on_mining_subscribe(self, __socket, request_id):
        extra_nonce = '0197'
        body = '{'\
                 f'"id":{request_id}, ' \
                 f'"result":[["mining.notify","1405ba371b0d0e4526961935bd5dbeee","EthereumStratum/1.0.0"],' \
                 f'"{extra_nonce}"],'\
                 f'"error":null' \
                 '}'
        self.send(__socket, body)

    def __on_mining_authorize(self, __socket, request_id):
        body = '{' \
               f'"id":{request_id},' \
               f'"result":true,' \
               f'"error":null' \
               '}'
        self.send(__socket, body)

        difficulty = 0.46565418188038166
        body = '{' \
                 '"id":null,' \
                 '"method":"mining.set_difficulty",' \
                 f'"params":[{difficulty}]' \
                 '}'
        self.send(__socket, body)

        params = '["7a2f8335",'\
                 '"02deafa02fa49495962fa2d5a2cdaa6226b83e98931eaea31ec53e49fe29a14d",' \
                 '"585f6925be23c7348c95af0f4b7edd4292c075a70ae0e99e3f349356ab3ad090",' \
                 'true]'
        body = '{'\
                '"id":null,'\
                '"method":"mining.notify",'\
                f'"params":{params}'\
                '}'
        self.send(__socket, body)

    def __on_mining_submit(self, socket, request_id: dict, params: list):
        logging.info(f'Nonce: {params}')
        body = '{"id":-1,"result":true,"error":null}'
        body.replace('-1', str(request_id))
        self.send(socket, body)
