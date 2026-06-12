# Pool Simulator

A local mining pool simulator that speaks the Stratum protocol over TCP. Connect any miner to it and it will respond with static but valid-shaped job data — useful for testing miner software, debugging protocol implementations, and replaying custom message sequences without needing a real pool or blockchain.

## Supported algorithms

| Algorithm | `--algo` value | Protocol variant |
|---|---|---|
| Ethash | `ethash` | EthereumStratum/1.0.0 |
| KawPow | `kawpow` | KawPow (RVN-style, `mining.set_target`) |
| MeowPow | `meowpow` | MeowPow |
| QuaiPow | `quaipow` | EthereumStratum/2.0.0 |
| Blake3 | `blake3` | Alephium Blake3 (JSON-RPC 2.0) |
| Autolykos v2 | `autolykos_v2` | Ergo Autolykos v2 |
| Smart Mining | `smart_mining` | LuminousMiner multi-algo protocol |
| Workflow | `workflow` | JSON-driven custom sequence (see below) |

## Usage

```bash
python main.py --algo <algorithm> [--host <host>] [--port <port>]
```

Defaults: `--host 127.0.0.1 --port 7878`.

**Examples:**

```bash
python main.py --algo ethash
python main.py --algo kawpow --port 4444
python main.py --algo autolykos_v2 --host 0.0.0.0 --port 9999
```

## Installation

No external dependencies at runtime. `pyinstaller` is listed for building a standalone binary:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Workflow

The `workflow` algorithm lets you define an arbitrary sequence of JSON packets in a config file and replay them against any connecting miner — no code required.

### How it works

1. A client connects → the server immediately sends **step 1**.
2. The client replies with a message containing an `id` field → the server sends **step 2**.
3. This repeats until all steps are exhausted.

Messages from the client that have no `id` field are ignored (logged at DEBUG level).

### JSON format

```json
{
    "my_workflow": {
        "description": "Optional human-readable description",
        "steps": [
            {
                "name": "step_1",
                "id": 1,
                "body": {
                    "method": "mining.notify",
                    "params": ["job_001", "aabbcc"]
                }
            },
            {
                "name": "step_2",
                "id": 2,
                "body": {
                    "method": "mining.set_difficulty",
                    "params": [1.0]
                }
            }
        ]
    }
}
```

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Label for the step (used in logs) |
| `body` | Yes | The JSON object sent to the client |
| `id` | No | If present, added to the outgoing `body` before sending |

A single file can contain multiple named workflows. The `--workflow-name` flag selects which one to run.

### Running a workflow

```bash
python main.py --algo workflow --workflow-file workflow_example.json --workflow-name workflow_sample_1
```

A ready-to-use example is provided in [`workflow_example.json`](workflow_example.json).

### Testing manually

```bash
# Terminal 1 — start the simulator
python main.py --algo workflow --workflow-file workflow_example.json --workflow-name workflow_sample_1

# Terminal 2 — connect and drive the sequence
nc 127.0.0.1 7878
# server sends step_1 immediately
{"id":1,"result":true}    # → server sends step_2
{"id":2,"result":true}    # → sequence complete
```
