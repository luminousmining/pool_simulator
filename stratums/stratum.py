import json
import logging
import socket

from stratums import STRATUM_VERSION
from utils import Statistics


class Stratum:

    def __init__(self):
        self.stratum_version = STRATUM_VERSION.STRATUM
        self.stats = Statistics()

    def on_connect(self, sock: socket.socket) -> None:
        pass

    def on_disconnect(self, sock: socket.socket) -> None:
        pass

    def send(self, __socket: socket.socket, msg: str) -> bool:
        try:
            msg_print = msg.replace("\n", "")
            logging.debug(f'send => {msg_print}')
            if '\n' not in msg:
                msg = f'{msg}\n'
            __socket.settimeout(0.5)
            __socket.sendall(bytes(msg, encoding="utf-8"))
            try:
                msg_id = json.loads(msg).get('id')
                if msg_id is not None:
                    self.stats.on_send(__socket, msg_id)
            except (json.JSONDecodeError, AttributeError):
                pass
        except TimeoutError:
            logging.warning(f'Skipped send timeout!')
        except socket.timeout:
            logging.warning(f'Skipped send timeout!')
            pass
        except Exception as error:
            logging.error(f'{error}.')
            return False

        return True
