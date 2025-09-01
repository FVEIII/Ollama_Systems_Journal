Use:
```bash
tail -n 20 ai_broker/broker.log
> python - <<'PY'
from pathlib import Path

text = r"""# AI Broker: Detailed Explanation for VS Code Users

## Mental model (how it fits your workflow)
The broker is a gatekeeper between the model and the real world. It ensures that risky operations (file access, network requests, CNC exports) are only performed under controlled conditions. You run the model in VS Code, but when it needs to access files or the network, those requests are routed through the broker, which checks policy rules, logs the action, and either allows or blocks it.

## What triggers the broker to act (and why)

### 1. Directory scopes
- **Why:** Prevents the model from accessing your entire drive.
- **How:** `policy.json → directories.allow_read / allow_write` define path prefixes.
- **Trigger:** If a path is outside the allowed list, you'll see a PolicyError.

### 2. Autonomy budget
- **Why:** Stops runaway loops.
- **How:** Controlled by `budgets.max_tool_calls_per_task` (default 5).
- **Trigger:** Budget exceeded → BudgetError.

### 3. Tripwires
- **Why:** Detects dangerous patterns like "ignore previous instructions".
- **How:** Regular expressions in `policy.json`.
- **Trigger:** If text matches, a TripwireError is raised.

### 4. Network guard
- **Why:** Default offline; explicit allowlists required.
- **How:** `network.enabled: false` unless turned on.
- **Trigger:** If disabled, requests are blocked. If enabled but domain not allowed, prompts for approval.

### 5. File size limits
- **Why:** Prevents accidental huge writes.
- **How:** Controlled by `budgets.max_bytes_write`.
- **Trigger:** Write too large → PolicyError.

## How to read the broker’s log
Every action is logged in `ai_broker/broker.log` with a hash chain for integrity. Logs include timestamp, action, parameters, and whether it was allowed or blocked.

Use: