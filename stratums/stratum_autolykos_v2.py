import logging

from stratums import Stratum


class StratumAutolykosv2(Stratum):

    def __init__(self):
        super(StratumAutolykosv2, self).__init__()

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

    def __on_mining_subscribe(self, sock,  request_id: int or str):
        extra_nonce = '996e'
        size = 6

        key_id = f'"id":{request_id}'
        if type(request_id) is str:
            key_id = f'"id":"{request_id}"'

        body = '{' \
               f'{key_id},' \
               f'"result":[null,\"{extra_nonce}\",{size}],' \
               f'"error":null' \
               '}'
        self.send(sock, body)

    def __on_mining_authorize(self, sock, request_id: int or str):
        key_id = f'"id":{request_id}'
        if type(request_id) is str:
            key_id = f'"id":"{request_id}"'

        body = '{' \
               f'{key_id},' \
               f'"result":true,' \
               f'"error":null' \
               '}'
        self.send(sock, body)

        difficulty = 1
        body = '{' \
               '"id":null,' \
               '"method":"mining.set_difficulty",' \
               f'"params":[{difficulty}]' \
               '}'
        self.send(sock, body)

        params = '["3",' \
                 '1415098,' \
                 '"6f109ba5226d1e0814cdeec79f1231d1d48196b5979a6d816e3621a1ef47ad80",' \
                 '"",' \
                 '"",' \
                 '2,' \
                 '"28948022309329048855892746252171976963209391069768726095651290785380",' \
                 '"",' \
                 'true]'
        body = '{' \
               '"id":null,' \
               '"method":"mining.notify",' \
               f'"params":{params}' \
               '}'
        self.send(sock, body)

    def __on_mining_submit(self, sock, request_id: int or str, params: list):
        key_id = request_id
        if type(request_id) is str:
            key_id = f'"{request_id}"'

        logging.info(f'Nonce: {params}')
        body = '{"id":-1,"result":true,"error":null}'
        body = body.replace('-1', str(key_id))
        self.send(sock, body)
