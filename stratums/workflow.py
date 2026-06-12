import json
import logging
import socket
import threading

from stratums import Stratum


class StratumWorkflow(Stratum):

    def __init__(self, workflow_name: str, workflow_file: str):
        super().__init__()
        self.__steps = []
        self.__client_step = {}
        self.__lock = threading.Lock()
        self.__load(workflow_name, workflow_file)

    def __load(self, workflow_name: str, workflow_file: str) -> None:
        with open(workflow_file, encoding='utf-8') as f:
            data = json.load(f)
        self.__steps = data[workflow_name]['steps']
        logging.info(f'Workflow "{workflow_name}" loaded — {len(self.__steps)} steps')

    def on_connect(self, sock: socket.socket) -> None:
        sock_id = id(sock)
        with self.__lock:
            self.__client_step[sock_id] = 0
        self.__send_current_step(sock)

    def on_disconnect(self, sock: socket.socket) -> None:
        with self.__lock:
            self.__client_step.pop(id(sock), None)

    def on_message(self, sock: socket.socket, data: dict) -> None:
        if 'id' in data:
            self.__advance(sock)
        else:
            logging.debug(f'workflow: message without id ignored => {data}')

    def __advance(self, sock: socket.socket) -> None:
        sock_id = id(sock)
        with self.__lock:
            if sock_id not in self.__client_step:
                return
            self.__client_step[sock_id] += 1
        self.__send_current_step(sock)

    def __send_current_step(self, sock: socket.socket) -> None:
        sock_id = id(sock)
        with self.__lock:
            index = self.__client_step.get(sock_id)
        if index is None or index >= len(self.__steps):
            logging.info(f'workflow: sequence complete for client {sock_id}')
            return
        step = self.__steps[index]
        body = dict(step['body'])
        if 'id' in step:
            body['id'] = step['id']
        logging.info(f'workflow: sending step "{step["name"]}" (index {index})')
        self.send(sock, json.dumps(body))
