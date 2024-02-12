import logging


class Stratum:

    def __init__(self):
        pass

    def send(self, __socket, msg) -> bool:
        try:
            msg_print = msg.replace("\n", "")
            logging.debug(f'send => {msg_print}')
            if '\n' not in msg:
                msg = f'{msg}\n'
            __socket.settimeout(0.1)
            __socket.sendall(bytes(msg, encoding="utf-8"))
        except TimeoutError:
            pass
        except Exception as error:
            logging.error(f'{error}.')
            return False

        return True
