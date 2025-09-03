# Ollama Systems Journal

## Overview
The **Ollama Systems Journal** is a secure, structured workspace for:
- AI-assisted journaling and research  
- Simulation design for real-world systems  
- Governance and safety controls for local AI experimentation  
- Tracking and managing multiple interconnected projects  

This repository integrates safe AI operations with tools for creative thinking, complex problem-solving, and secure data workflows.

---

## Key Components

- **[AI Broker](ai_broker/README.md)**  
  Acts as a safety layer between AI models and the local environment, enforcing:
  - Directory permissions  
  - Network controls  
  - Security guardrails  
  - Logging and monitoring  

- **[Master Project Tracker](Master_Project_Tracker/README.md)**  
  Provides a central hub for:
  - Project tracking  
  - Simulation templates  
  - Shared dashboards and reports  

- **[AI Safety Operating Procedure](docs/AI_Safety_Operating_Procedure.md)**  
  Defines rules, roles, and processes to ensure responsible AI usage and risk mitigation.

---

## Repository Structure
```text
Ollama_Systems_Journal/
├── .vscode/                  # VS Code settings for project consistency
│   └── settings.json
├── ai_broker/                # AI Broker for permissions, safety, and guardrails
│   ├── docs/                 # AI Broker documentation
│   │   └── AI_Broker_Explanation.md
│   ├── __init__.py
│   ├── __main__.py
│   ├── ai_broker.py
│   ├── broker.log
│   ├── policy.json
│   └── README.md
├── coffee_sim/               # Coffee simulation project
│   ├── coffee_sim.md
│   └── market_analysis.md
├── content/                   # Placeholder for generated or shared content
├── data/                       # Input data for simulations and workflows
├── docs/                       # Governance and safety documentation
│   └── AI_Safety_Operating_Procedure.md
├── exports/                    # Generated exports and reports
├── logs/                        # Runtime logs
│   └── .gitkeep                # Keeps folder tracked even when empty
├── Master_Project_Tracker/     # Central hub for project tracking
│   ├── master_project_tracker.md # Main tracker document
│   ├── project_status.yaml      # YAML project configuration
│   ├── README.md                # Folder-level documentation
│   └── show_projects.py         # Utility script for viewing project statuses
├── prompts/                     # Prompt templates for AI workflows
├── .gitignore                    # Git ignore rules
├── .last_prompt                   # Records last used AI prompt
├── fixed_test_voice.py            # Audio/voice system testing
├── frontmatter_dashboard.csv      # Dashboard metadata for tracking
├── journal_log.txt                # Journal logging
├── journal_voice.py               # Voice journal script
├── ollama-conversation.md         # Notes on Ollama Systems Journal conversations
├── requirements.txt               # Python dependencies
├── run_scenario.py                 # Scenario execution script
├── start_voice_journal.bat         # Windows batch file to launch voice journal
├── sync_frontmatter.py             # Sync YAML/CSV frontmatter utility
├── sync_utils.py                    # Shared sync utilities
├── temp.wav                          # Temporary audio file
├── test_save_audio.py                 # Test audio saving functionality
├── test_voice.py                      # Test voice processing script
└── README.md                          # Root README with overview and structure
```
