# System Architecture (ARCHITECTURE.md)

## 1. High-Level Diagram
[Polling Service] -> [Gmail API] -> [LLM Processor] -> [Logic Engine] -> [Calendar API]
                                         |               |
                                         v               v
                                   [Entity Store]   [Gmail Send]

## 2. Components

### A. Polling Service
A scheduled task (Node-cron or Python Schedule) that triggers every 15 minutes. It maintains a `last_processed_timestamp` to avoid duplicates.

### B. Perception Layer (LLM)
Uses an LLM (e.g., GPT-4o, Gemini 1.5 Pro) to convert unstructured email text into a structured JSON object:
```json
{
  "is_meeting_request": true,
  "start_time": "2024-06-10T10:00:00Z",
  "end_time": "2024-06-10T11:00:00Z",
  "location": "Zoom",
  "participants": ["client@example.com"]
}
```

### C. Logic Engine
The "Brain" of the agent. 
1. Receives structured data.
2. Checks Calendar API for conflicts.
3. Decides: `CREATE_EVENT` or `REJECT_REQUEST`.

### D. Integration Layer
Wrappers for Google APIs using official SDKs. Handles token refresh and rate limiting.

## 3. Tech Stack
- **Language:** TypeScript / Node.js (or Python)
- **AI:** OpenAI API / LangChain
- **APIs:** Google Workspace (Gmail/Calendar)
- **Storage:** Local JSON or SQLite for state management.
