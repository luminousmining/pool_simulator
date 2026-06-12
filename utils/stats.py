import logging
import socket
import threading
import time


class Statistics:

    def __init__(self):
        self.__pending: dict[tuple[int, str], float] = {}
        self.__round_trip_times: list[float] = []
        self.__lock = threading.Lock()

    def on_send(self, sock: socket.socket, msg_id: int | str) -> None:
        key = (id(sock), str(msg_id))
        with self.__lock:
            self.__pending[key] = time.perf_counter()

    def on_receive(self, sock: socket.socket, msg_id: int | str) -> None:
        key = (id(sock), str(msg_id))
        now = time.perf_counter()
        with self.__lock:
            send_time = self.__pending.get(key)
            if send_time is None:
                return
            self.__pending[key] = now
        rtt_ms = (time.perf_counter() - send_time) * 1000
        with self.__lock:
            self.__round_trip_times.append(rtt_ms)
        logging.info(f'[stats] id={msg_id} rtt={rtt_ms:.2f}ms')

    def summary(self) -> dict:
        with self.__lock:
            data = list(self.__round_trip_times)
        if not data:
            return {'count': 0}
        return {
            'count': len(data),
            'min_ms': round(min(data), 2),
            'max_ms': round(max(data), 2),
            'avg_ms': round(sum(data) / len(data), 2),
        }
