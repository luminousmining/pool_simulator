import json
import socket
import sys
import time

HOST = '127.0.0.1'
PORT = 7878
EXPECTED_STEPS = 3
TIMEOUT = 10


def wait_for_server(timeout: int) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            s = socket.create_connection((HOST, PORT), timeout=1)
            s.close()
            return
        except OSError:
            time.sleep(0.2)
    print(f'Server did not open on {HOST}:{PORT} within {timeout}s', file=sys.stderr)
    sys.exit(1)


def run() -> None:
    wait_for_server(TIMEOUT)

    sock = socket.create_connection((HOST, PORT), timeout=TIMEOUT)
    steps_done = 0
    buf = ''

    try:
        while steps_done < EXPECTED_STEPS:
            chunk = sock.recv(4096).decode()
            if not chunk:
                print('Connection closed unexpectedly', file=sys.stderr)
                sys.exit(1)
            buf += chunk
            lines = buf.split('\n')
            buf = lines[-1]
            for line in lines[:-1]:
                line = line.strip()
                if not line:
                    continue
                msg = json.loads(line)
                msg_id = msg.get('id')
                if msg_id is None:
                    continue
                response = json.dumps({'id': msg_id, 'result': True}) + '\n'
                sock.sendall(response.encode())
                steps_done += 1
                print(f'step {steps_done}/{EXPECTED_STEPS} ok (id={msg_id})')
    finally:
        sock.close()

    print(f'{steps_done} steps completed successfully')


if __name__ == '__main__':
    run()
