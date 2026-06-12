import logging

from stratums import Stratum


class StratumMeowpow(Stratum):

    def __init__(self):
        super(StratumMeowpow, self).__init__()

    def on_message(self, sock, data: dict):
        if 'method' in data:
            self.__on_method(sock, data)
        else:
            self.__on_response(sock, data)

    def __on_response(self, sock, data: dict):
        logging.info(f'response => {data}')

    def __on_method(self, sock, data: dict):
        method = data['method']
        params = data['params']

        if method == 'mining.subscribe':
            self.__on_mining_subscribe(sock, data['id'])
        elif method == 'mining.authorize':
            self.__on_mining_authorize(sock, data['id'])
        elif method == 'mining.submit':
            self.__on_mining_submit(sock, data['id'], params)
        else:
            logging.error(f'Unknow method [{method}][{params}]')

    def __on_mining_subscribe(self, sock, request_id):
        weird = '0HN7JVA7GAKU9'
        extra_nonce = '8071'
        body = '{' \
               f'"id":{request_id}, ' \
               f'"result":["{weird}", "{extra_nonce}"],' \
               f'"error":null' \
               '}'
        self.send(sock, body)

    def __on_mining_authorize(self, sock, request_id):
        body = '{' \
               f'"id":{request_id},' \
               f'"result":true,' \
               f'"error":null' \
               '}'
        self.send(sock, body)

        self.__mining_notify(sock)

    def __on_mining_submit(self, sock, request_id: int, params: list):
        logging.info(f'Nonce: {params}')
        body = '{"id":-1,"result":true,"error":null}'
        body = body.replace('-1', str(request_id))
        self.send(sock, body)

    def __mining_notify(self, sock):
        params = '"00001058",' \
                 '"44cf248a77ce1623d4fd833ec13ceab83d40591fb9dd7cf7ec28d08f298ba709",' \
                 '"cfa3e37c459ebd9b4138bd2141a52d89f6f8f671ecf91456f5a29176eb132fc0",' \
                 '"0000000500000000000000000000000000000000000000000000000000000000",' \
                 'true,' \
                 '1118706,' \
                 '"1c014de3"'
        body = '{' \
               '"id": null, '\
               '"method": "mining.notify", '\
               f'"params": [{params}]'\
               '}'
        self.send(sock, body)
