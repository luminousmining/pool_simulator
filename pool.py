import logging
import socket
import threading
import json

from algorithm import ALGORITHM
from stratums import StratumEthash, StratumKawpow


class Pool:

    def __init__(self, algo: str, hostname: str, port: int):
        self.algo = str(algo)
        self.hostname = str(hostname)
        self.port = int(port)
        self.clients = dict()
        self.server = None
        self.alive = False
        self.threadAccept = None
        self.stratum = None

        if algo == ALGORITHM.ETHASH:
            self.stratum = StratumEthash()
        elif algo == ALGORITHM.KAWPOW:
            self.stratum = StratumKawpow()

    def is_alive(self) -> bool:
        return self.alive

    def start(self):
        self.alive = True

        logging.info(f'Open server {self.hostname}:{self.port} - {self.algo}')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, self.port))
        self.server.listen(1)

        self.threadAccept = threading.Thread(target=self.__accept, args=())
        self.threadAccept.start()

    def stop(self):
        pass

    def __accept(self):
        __socket, addr = self.server.accept()
        self.clients[addr[1]] = __socket
        logging.info(f'New client[{addr[1]}] connected! - Total clients {len(self.clients)}')

        self.threadAccept = threading.Thread(target=self.__accept, args=())
        self.threadAccept.start()

    def remove_client(self, fd: int):
        logging.warning(f'Remove client {fd}')
        del self.clients[fd]

    def on_receive(self):
        for fd, __socket in self.clients.items():
            try:
                __socket.settimeout(0.1)
                raw = __socket.recv(2040)
                if not raw:
                    self.remove_client(fd)
                    continue
                packets = raw.decode("utf-8").split('\n')
                if len(packets):
                    for packet in packets:
                        if len(packet):
                            data = json.loads(packet)
                            logging.info(f'recv <= {data}')
                            self.stratum.on_message(fd, socket, data)
            except TimeoutError:
                pass
            except ConnectionAbortedError:
                self.remove_client(fd)
            except Exception as err:
                logging.error(err)
                self.remove_client(fd)
