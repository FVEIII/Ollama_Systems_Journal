# ai_broker (Minimal Safety Broker)

This is a tiny guard layer for local AI workflows. It enforces:
- Directory scopes for file read/write
- Autonomy budget (max tool calls per task)
- Network allowlist (GET only, optional confirmation for off‑list domains)
- Tripwires for risky text patterns
- Tamper‑evident append‑only logs

## Layout
```
ai_broker/
  __init__.py
  __main__.py         # enables `python -m ai_broker`
  ai_broker.py        # library + CLI implementation
  policy.json         # edit this for your project
  broker.log          # generated at runtime
```

## Quickstart
1. Edit `policy.json` paths/domains/budgets to fit your repo.
2. Try some commands:
```bash
python -m ai_broker write --path "./exports/hello.txt" --text "hello"
python -m ai_broker read  --path "./exports/hello.txt"
python -m ai_broker http_get --url "https://example.com"
```
3. Open `ai_broker/broker.log` to see hash‑chained records.

## Integrating in Python
```python
from ai_broker import Broker, PolicyError
b = Broker("ai_broker/policy.json", log_path="ai_broker/broker.log")
b.write_file("./exports/out.txt", "hi")
print(b.read_file("./exports/out.txt"))
```

## Notes
- Network is off by default (`enabled: false`). Flip it once you’re comfortable.
- The broker is intentionally minimal—extend it with CNC exporters, email draft writers, etc., but always route through the broker, not the model directly.
