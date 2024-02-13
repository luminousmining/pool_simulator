import logging
import socket


class Stratum:

    def __init__(self):
        pass

    def send(self, __socket, msg) -> bool:
        try:
            msg_print = msg.replace("\n", "")
            logging.debug(f'send => {msg_print}')
            if '\n' not in msg:
                msg = f'{msg}\n'
            __socket.settimeout(0.5)
            __socket.sendall(bytes(msg, encoding="utf-8"))
        except TimeoutError:
            logging.warning(f'Skipped send timeout!')
        except socket.timeout:
            logging.warning(f'Skipped send timeout!')
            pass
        except Exception as error:
            logging.error(f'{error}.')
            return False

        return True
