# 🛡️ AI Broker: Safety and Control Documentation

This guide explains how the **AI Broker** enforces safety protocols within the **Ollama Systems Journal** project.  
Its purpose is to **prevent accidental data loss**, **protect sensitive actions**, and **provide transparency** for all automated workflows.

---

## 1. Purpose of the Broker

The Systems Journal project combines:
- **LLM automation** using Ollama models.
- **Python scripts** for syncing, exporting, and data management.
- **GitHub integration** for version control and backups.

Because these tools are powerful, errors can cause:
- Permanent loss of files or research notes.
- Sensitive or private data being accidentally pushed to GitHub.
- Infinite loops or unstable actions triggered by LLMs or scripts.

The broker acts as a **circuit breaker** for your workflow, providing:
- **Gatekeeping** – only approved actions are allowed.
- **Logging** – every action is tracked for review.
- **Fail-safes** – blocks destructive or risky commands.

---

## 2. How the Workflow Operates

Below is the high-level flow of how actions move through the system:

```plaintext
VS Code Terminal / Scripts
     │
     ▼
Broker (ai_broker.py)
     │
     ├── Reads `policy.json`
     │       │
     │       └─ Decision Points:
     │            • Allow action (safe)
     │            • Warn user (review required)
     │            • Block action (unsafe)
     │
     ▼
Scripts Execute → Results synced to Master_Project_Tracker
