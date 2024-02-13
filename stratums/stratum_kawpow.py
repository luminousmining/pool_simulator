import logging

from stratums import Stratum


class StratumKawpow(Stratum):

    def __init__(self):
        super(StratumKawpow, self).__init__()

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
        extra_nonce = 'c797'
        body = '{' \
               f'"id":{request_id}, ' \
               f'"result":[null, "{extra_nonce}"],' \
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

        target = '00000004c5adf9601f294e237e477a16da83737a977a9898ed5f5fe6ad94fdd8'
        body = '{' \
               '"id":null,' \
               '"method":"mining.set_target",' \
               f'"params":["{target}"]' \
               '}'
        self.send(sock, body)

        self.__mining_notify(sock)

    def __on_mining_submit(self, __socket, request_id: dict, params: list):
        logging.info(f'Nonce: {params}')
        body = '{"id":-1,"result":true,"error":null}'
        body.replace('-1', str(request_id))
        self.send(__socket, body)

    def __mining_notify(self, sock):
        params = '"121c",' \
                 '"ac9591f269daea1814735388e44c1cd14c991bbbbf387fbc6d1d079d7eeec1bf",' \
                 '"db767d7b81c87067d9d8bf2347f783b7bbb367d345a33f3e5fd9c76e0d1b2156",' \
                 '"00000004c5adf9601f294e237e477a16da83737a977a9898ed5f5fe6ad94fdd8",' \
                 'true,' \
                 '2523642,' \
                 '"1a592935"'
        body = '{' \
               '"id": null, '\
               '"method": "mining.notify", '\
               f'"params": [{params}]'\
               '}'
        self.send(sock, body)
