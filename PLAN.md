# Development Plan (PLAN.md)

## Phase 1: Environment & Authentication
- [x] Set up Google Cloud Project.
- [x] Configure OAuth2 consent screen and credentials.
- [x] Implement local token management for Gmail and Calendar APIs.

## Phase 2: Email Processing Engine
- [x] Develop Gmail polling service.
- [x] Implement email parsing (metadata and body extraction).
- [x] Create LLM integration layer (OpenAI/Anthropic/Gemini).

## Phase 3: Logic & Calendar Integration
- [x] Develop extraction prompts for the LLM.
- [x] Implement Calendar availability checker.
- [x] Implement Event Creation logic.

## Phase 4: Automated Communication
- [x] Create email templates for confirmations and rejections.
- [x] Integrate SMTP/Gmail Send for replies.

## Phase 5: Automation & Deployment
- [x] Set up CRON job/Scheduler (15-minute intervals).
- [x] Logging and monitoring setup.

## Phase 6: Model Context Protocol (MCP)
- [x] Implement MCP server using FastMCP.
- [x] Expose core agent functions as MCP tools.
- [x] Verify tool discovery with demo client.
