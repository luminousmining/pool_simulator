import logging

from stratums import Stratum
from stratums import STRATUM_VERSION


class StratumQuaipow(Stratum):

    def __init__(self):
        super(StratumQuaipow, self).__init__()

    def on_message(self, sock, data: dict) -> None:
        if 'method' in data:
            self.__on_method(sock, data)
        else:
            self.__on_response(sock, data)

    def __on_response(self, sock, data: dict) -> None:
        logging.info(f'response => {data}')

    def __on_method(self, sock, data: dict) -> None:
        method = data['method']
        params = data['params'] if 'params' in data else None

        if method == 'mining.hello':
            self.__on_mining_hello(sock, data['id'])
        elif method == 'mining.subscribe':
            self.__on_mining_subscribe(sock, data['id'])
        elif method == 'mining.authorize':
            self.__on_mining_authorize(sock, data['id'])
        elif method == 'mining.submit':
            self.__on_mining_submit(sock, data['id'], params)
        elif method == 'mining.noop':
            pass
        else:
            logging.error(f'Unknow method [{method}][{params}]')

    def __on_mining_hello(self, sock, request_id) -> None:
        self.stratum_version = STRATUM_VERSION.ETHEREUMSTRATUM2
        result = '{' \
                 '"encoding":"plain",' \
                 '"maxerrors":999,' \
                 '"node":"go-quai/development",' \
                 '"proto":"EthereumStratum/2.0.0",' \
                 '"resume":0,' \
                 '"timeout":30' \
                 '}'
        body = '{' \
               f'"id":{request_id},' \
               f'"result":{result},' \
               '"error":null' \
               '}'
        self.send(sock, body)

    def __on_mining_subscribe(self, sock, request_id) -> None:
        body = '{' \
               f'"id":{request_id},' \
               '"result":"s-12345",' \
               '"error":null' \
               '}'
        self.send(sock, body)

    def __on_mining_authorize(self, sock, request_id) -> None:
        body = '{' \
               f'"id":{request_id},' \
               '"result":"s-12345",' \
               '"error":null' \
               '}'
        self.send(sock, body)

        if self.stratum_version == STRATUM_VERSION.ETHEREUMSTRATUM2:
            self.__mining_set(sock)
        self.__mining_notify(sock)

    def __on_mining_submit(self, sock, request_id: int, params: list) -> None:
        logging.info(f'Nonce: {params}')
        body = '{"id":-1,"result":true,"error":null}'
        body = body.replace('-1', str(request_id))

    def __mining_set(self, sock):
        params = '{' \
                 '"algo":"progpow",' \
                 '"epoch":"0",' \
                 '"extranonce":"c41a",' \
                 '"target":"000000001920931418b137a47a808e0e218e55bfefaaf157853edf290f431b28"' \
                 '}'

        body = '{' \
               '"method":"mining.set",' \
               f'"params":{params}' \
               '}'
        self.send(sock, body)

    def __mining_notify(self, sock) -> None:
        params = '"1d9",' \
                 '"c2b",' \
                 '"efdd22cc2af5cae474e7f2bb9b9383ebf847f5a780e84b7a27cb65f70cab6bdf",' \
                 '"0"'
        body = '{' \
               '"method":"mining.notify",' \
               f'"params":[{params}]' \
               '}'
        self.send(sock, body)
