# Meeting MCP Agent

An automated AI agent that monitors Gmail for meeting requests, analyzes them using LLMs, and manages Google Calendar events autonomously.

## Overview

The Meeting MCP Agent is designed to act as a virtual personal assistant. It periodically scans an inbox, interprets natural language meeting requests, checks for scheduling conflicts, and either confirms the appointment or suggests a graceful rejection.

## Key Features

- **Automated Scanning:** Runs every 15 minutes to process new communications.
- **Natural Language Understanding:** Extracts date, time, location, and participants using state-of-the-art LLMs.
- **Calendar Integration:** Seamlessly interacts with Google Calendar API to check availability and create events.
- **Automated Correspondence:** Sends professional replies based on scheduling outcomes.

## Getting Started

### 1. Google API Setup
To use this agent, you need a Google Cloud Project with the Gmail and Calendar APIs enabled.
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable **Gmail API** and **Google Calendar API**.
4. Configure the **OAuth Consent Screen** (Internal or External/Testing).
5. Go to **Credentials** -> **Create Credentials** -> **OAuth Client ID**.
6. Select **Desktop App** as the application type.
7. Download the JSON file containing your client secrets.
8. Copy this file to the root of the project directory and rename it to `credentials.json`.

### 2. Environment Variables
1. Copy `.env.example` to `.env`.
2. Fill in your LLM API keys (OpenAI/Gemini).

### 3. Installation
```bash
pip install -r requirements.txt
python main.py
```

## Documentation

- [PRD.md](./docs/PRD.md) - Product Requirements Document
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System Design & Architecture
- [SECURITY.md](./docs/SECURITY.md) - Security & Privacy Protocols
- [TESTING.md](./docs/TESTING.md) - Testing Strategy
- [EXPERIMENTS.md](./docs/EXPERIMENTS.md) - LLM Prompt Engineering & Research
