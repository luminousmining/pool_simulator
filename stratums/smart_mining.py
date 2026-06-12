import logging

from stratums import Stratum


class StratumSmartMining(Stratum):

    def __init__(self):
        super(StratumSmartMining, self).__init__()
        self.__current_algorithm = str()

    def on_message(self, sock, data: dict) -> None:
        if 'method' in data:
            self.__on_method(sock, data)
        else:
            self.__on_response(sock, data)

    def __on_response(self, sock, data: dict) -> None:
        logging.info('In response')

    def __on_method(self, sock, data: dict) -> None:
        request_id = data['id']
        method = data['method']

        if method == 'mining.subscribe':
            self.__on_mining_subscribe(sock, request_id)
        elif method == 'mining.submit':
            self.__on_submit(sock, request_id)

    def __on_submit(self, sock, request_id):
        body = '{"id":-1,"result":true,"error":null}'
        body = body.replace('-1', str(request_id))
        self.send(sock, body)

    def __on_mining_subscribe(self, sock, request_id) -> None:
        body = '{"id":-1,"result":true,"error":null}'
        body = body.replace('-1', str(request_id))
        self.send(sock, body)

        self.__set_algo_ethash(sock)
        self.__send_ethash_job(sock)

    def __set_algo_ethash(self, sock):
        self.__current_algorithm = 'ethash'

        # mining.set_algo
        body = '{'\
               '"id":1,'\
               '"method":"smart_mining.set_algo",'\
               '"params":"ethash"'\
               '}'
        self.send(sock, body)

        # mining.set_extra_nonce
        extra_nonce = '0197'
        body = '{'\
               '"id": 2,'\
               '"method":"smart_mining.set_extra_nonce",'\
               f'"params":"{extra_nonce}"'\
               '}'
        self.send(sock, body)

    def __send_ethash_job(self, sock):
        # mining.set_difficulty
        difficulty = 0.46565418188038166
        body = '{' \
                 '"id":null,' \
                 '"method":"mining.set_difficulty",' \
                 f'"params":[{difficulty}]' \
                 '}'
        self.send(sock, body)

        # mining.notify
        params = '["7a2f8335",'\
                 '"02deafa02fa49495962fa2d5a2cdaa6226b83e98931eaea31ec53e49fe29a14d",' \
                 '"585f6925be23c7348c95af0f4b7edd4292c075a70ae0e99e3f349356ab3ad090",' \
                 'true]'
        body = '{'\
                '"id":null,'\
                '"method":"mining.notify",'\
                f'"params":{params}'\
                '}'
        self.send(sock, body)
