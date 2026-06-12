import logging

from stratums import Stratum


class StratumBlake3(Stratum):

    def __init__(self):
        super(StratumBlake3, self).__init__()

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

        if method == 'mining.authorize':
            self.__on_mining_authorize(sock, data['id'])
        elif method == 'mining.submit':
            self.__on_mining_submit(sock, data['id'], params)
        else:
            logging.error(f'Unknow method [{method}][{params}]')

    def __on_mining_authorize(self, sock, request_id):
        body_authorize = '{' \
               '"jsonrpc":"2.0",' \
               '"method":"mining.authorize",' \
               '"params":true,' \
               f'"id":{request_id}' \
               '}'
        self.send(sock, body_authorize)

        self.__mining_set_extranonce(sock)
        self.__mining_set_difficulty(sock)
        self.__mining_notify(sock)

    def __on_mining_submit(self, sock, request_id: int, params: dict):
        logging.info(f'Nonce:{params}')

        body = '{"id":-1,"jsonrpc":"2.0","error":null,"result":true}'
        body = body.replace('-1', str(request_id))
        self.send(sock, body)

    def __mining_set_extranonce(self, sock):
        body_set_target = '{"jsonrpc":"2.0","method":"mining.set_extranonce","params":["914544"],"id":null}'
        self.send(sock, body_set_target)

    def __mining_set_difficulty(self, sock):
        body = '{"jsonrpc":"2.0","method":"mining.set_difficulty","params":[2.0],"id":null}'
        self.send(sock, body)

    def __mining_notify(self, sock):
        #                 '"targetBlob":"00000001ffffffffffffffffffffffffffffffffffffffffffffffffffffffff"'\
        #                 '"targetBlob":"1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"'\
        body = '{'\
            '"jsonrpc":"2.0",'\
            '"method":"mining.notify",'\
            '"params":[{'\
                '"jobId":"00024844",'\
                '"fromGroup":3,'\
                '"toGroup":3,'\
                '"headerBlob":"00070000000000007d10335f5e27e328c4fdc15c6a8a5393bd90a65ba604db37fa70000000000001457e989b3596cf3e533e82be23bb10fa40a6dd65b8e0f3eb2035000000000000ddb8a934011f82901e36ab8294c2ac406c8c68333ee55e08ca9a0000000000027d741491fc5651c4bcecdd00ffaab8529e81bb410095c5957bec00000000000256d5c0d43e3a05021d9cef0f6fe357b91cf6b2065ad5ca057d9d0000000000018a2744eb996e3e54f556bfb0c8b684ec6ab6e83a8e9df1cd4b2e000000000000d7a65f5402f687390cd33ad90beb0e2e1ec5f4b57541c84410cf76228c9acba946fd8d64fed95f90997779e1b7c6c68c6ee93e8b49ba006cff9097ecc10ccced69fdc5769d4e5469ce523f09590370cb844ec46c33cca1148cc20000018eaa9ea03a1b02cd79",'\
                '"targetBlob":"00000001ffffffffffffffffffffffffffffffffffffffffffffffffffffffff"'\
                '}],'\
            '"id":null'\
            '}'
        self.send(sock, body)
