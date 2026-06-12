# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A local mining pool simulator that speaks the Stratum protocol over TCP. Miners connect to it, subscribe/authorize, receive fake jobs, and submit shares — useful for testing miner software without a real pool.

## Running the simulator

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Start with a specific algorithm (default: ethash, port: 7878)
python main.py --algo ethash --host 127.0.0.1 --port 7878

# Supported algorithms
python main.py --algo kawpow
python main.py --algo meowpow
python main.py --algo quaipow
python main.py --algo blake3
python main.py --algo autolykos_v2
python main.py --algo smart_mining
```

There are no automated tests; validation is done by connecting a real miner.

## Architecture

```
main.py          ← CLI entry point: parse args, create Pool, call bind()+process()
pool.py          ← TCP server: accept connections, recv JSON lines, dispatch to stratum
algorithm.py     ← ALGORITHM constants + is_valid_algorithm()
stratums/
  stratum.py             ← Base class: send() helper (adds \n, logs)
  stratum_version.py     ← STRATUM_VERSION enum (unused at runtime, kept for typing)
  stratum_ethash.py      ← EthereumStratum/1.0.0 variant
  stratum_kawpow.py      ← KawPow (RVN-style) with set_target
  stratum_meowpow.py     ← MeowPow (same shape as kawpow)
  stratum_quaipow.py     ← QuaiPow variant
  stratum_blake3.py      ← Alephium Blake3 (jsonrpc 2.0 framing, no subscribe step)
  stratum_autolykos_v2.py ← Ergo Autolykos v2 (request_id can be str or int)
  stratum_smart_mining.py ← LuminousMiner smart_mining protocol (set_algo + set_extra_nonce before notify)
```

## Protocol flow (general Stratum)

Each stratum class implements `on_message(sock, data)` and handles three inbound methods:

1. `mining.subscribe` → respond with `[extra_nonce]`, optional session info
2. `mining.authorize` → respond `true`, then push `mining.set_difficulty` + `mining.notify` (the fake job)
3. `mining.submit`    → respond `true` (all shares accepted)

**Blake3 exception:** skips `subscribe`; the authorize response triggers all setup messages.  
**smart_mining exception:** subscribe triggers `smart_mining.set_algo` + `smart_mining.set_extra_nonce` before the job.

## Adding a new algorithm

1. Add a constant to `ALGORITHM` in `algorithm.py` and return `True` for it in `is_valid_algorithm()`.
2. Create `stratums/stratum_<name>.py` — subclass `Stratum`, implement `on_message()` following the pattern above.
3. Export it in `stratums/__init__.py`.
4. Add the branch in `Pool.__init__()` in `pool.py`.
5. Update the `--algo` help string in `main.py`.

## Key implementation details

- **JSON framing:** each Stratum message is a single JSON object terminated by `\n`. `Pool.__on_client` splits on `\n` and parses each non-empty chunk independently.
- **`autolykos_v2` request_id:** can arrive as either `int` or `str`; the class handles both when serialising the response.
- **Hardcoded job data:** all job params (header hash, seed hash, target, nonce, etc.) are static test fixtures — no real blockchain data.
- **PyInstaller** is the only dependency (`requirements.txt`); stdlib only at runtime.
