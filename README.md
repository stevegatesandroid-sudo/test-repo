# test-repo

This repository contains a small sample web page and a command-line ATM
simulation written in Python.

## Contents

- [`abc.html`](abc.html) - a responsive HTML5 sample page with embedded CSS.
- [`atm_simulation.py`](atm_simulation.py) - an interactive ATM application
  supporting PIN authentication, balance checks, deposits, and withdrawals.

## Running the ATM simulation

Python 3.9 or newer is recommended. From the repository root, run:

```bash
python atm_simulation.py
```

The demo accounts are:

| Account number | PIN  | Starting balance |
| --- | --- | ---: |
| `1001` | `1234` | $1,250.00 |
| `1002` | `2468` | $500.00 |

The application keeps account data in memory, so changes are reset when the
program exits. This is intentionally a local demonstration and does not
connect to a real banking service.

## HTML validation

The GitHub Actions workflow in
`.github/workflows/test-html.yml` validates HTML files on pull requests
targeting `main`.
