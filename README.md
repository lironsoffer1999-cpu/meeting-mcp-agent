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

### 3. Installation & Running
```bash
pip install -r requirements.txt
```

#### Running the Scheduler
To run the original background scheduler that polls for emails every 15 minutes:
```bash
python main.py
```

#### MCP Layer
The project includes a Model Context Protocol (MCP) layer built with [FastMCP](https://github.com/jlowin/fastmcp). This allows the agent's capabilities to be used as tools by MCP-compatible clients.

- **Purpose:** To provide a standardized interface for AI models to interact with the Gmail and Calendar tools.
- **Server:** `mcp_server.py` implements the MCP server.
    - *Note:* The server is designed to run over stdio and should normally be launched by an MCP host (e.g., Claude Desktop).
- **Verification:** You can verify the MCP server and list available tools using the provided demo client:
  ```bash
  python mcp_client_demo.py
  ```

**Expected MCP Tools Output:**
```text
Meeting MCP Agent - Available MCP Tools:
- fetch_new_emails
- parse_meeting_request
- check_calendar_availability
- find_alternative_slot
- create_calendar_event
- send_gmail_reply
- mark_email_as_read
```

## Documentation

- [PRD.md](./PRD.md) - Product Requirements Document
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System Design & Architecture
- [SECURITY.md](./SECURITY.md) - Security & Privacy Protocols
- [TESTING.md](./TESTING.md) - Testing Strategy
- [EXPERIMENTS.md](./EXPERIMENTS.md) - LLM Prompt Engineering & Research
