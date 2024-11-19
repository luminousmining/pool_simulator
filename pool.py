import logging
import socket
import threading
import json
import time

from algorithm import ALGORITHM
from stratums import (StratumSmartMining,
                      StratumEthash,
                      StratumKawpow,
                      StratumBlake3,
                      StratumMeowpow,
                      StratumQuaipow)


class Pool:

    def __init__(self, algo: str, hostname: str, port: int):
        self.algo = str(algo)
        self.hostname = str(hostname)
        self.port = int(port)
        self.__clients = dict()
        self.__socket = None
        self.alive = False
        self.threadAccept = None
        self.stratum = None

        if algo == ALGORITHM.SMART_MINING:
            self.stratum = StratumSmartMining()
        elif algo == ALGORITHM.ETHASH:
            self.stratum = StratumEthash()
        elif algo == ALGORITHM.KAWPOW:
            self.stratum = StratumKawpow()
        elif algo == ALGORITHM.MEOWPOW:
            self.stratum = StratumMeowpow()
        elif algo == ALGORITHM.QUAIPOW:
            self.stratum = StratumQuaipow()
        elif algo == ALGORITHM.BLAKE3:
            self.stratum = StratumBlake3()

    def is_alive(self) -> bool:
        return self.alive

    def bind(self):
        self.alive = True

        logging.info(f'Open server {self.hostname}:{self.port} - {self.algo}')

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.hostname, self.port))
        self.__socket.listen(1)

        self.threadAccept = threading.Thread(target=self.__accept, args=())
        self.threadAccept.start()

    def stop(self):
        pass

    def __accept(self):
        sock, addr = self.__socket.accept()
        self.__clients[addr[1]] = sock
        logging.info(f'New client[{addr[1]}] connected! - Total clients {len(self.__clients)}')

        thread_loop = threading.Thread(target=self.__on_client,
                                       args=(addr[1], sock))
        thread_loop.start()

        self.threadAccept = threading.Thread(target=self.__accept, args=())
        self.threadAccept.start()

    def remove_client(self, by: str, addr: int):
        logging.warning(f'Remove client {addr} - {by}')
        if addr in self.__clients:
            del self.__clients[addr]

    def process(self):
        while self.is_alive() is True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.alive = False

    def __on_client(self, addr, sock):
        while self.is_alive() is True:
            try:
                sock.settimeout(0.1)
                raw = sock.recv(2040)
                if not raw:
                    self.remove_client('packet is empty', addr)
                    return
                packets = raw.decode("utf-8").split('\n')
                if len(packets):
                    for packet in packets:
                        if len(packet):
                            data = json.loads(packet)
                            logging.info(f'recv <= {data}')
                            self.stratum.on_message(sock, data)
            except TimeoutError:
                pass
            except socket.timeout:
                pass
            except ConnectionAbortedError:
                self.remove_client('ConnectionAbortedError', addr)
                return
            except Exception as e:
                self.remove_client(f'Exception[{e}]', addr)
                return
