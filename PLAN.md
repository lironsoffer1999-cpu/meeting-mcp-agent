# Development Plan (PLAN.md)

## Phase 1: Environment & Authentication
- [ ] Set up Google Cloud Project.
- [ ] Configure OAuth2 consent screen and credentials.
- [ ] Implement local token management for Gmail and Calendar APIs.

## Phase 2: Email Processing Engine
- [ ] Develop Gmail polling service.
- [ ] Implement email parsing (metadata and body extraction).
- [ ] Create LLM integration layer (OpenAI/Anthropic/Gemini).

## Phase 3: Logic & Calendar Integration
- [ ] Develop extraction prompts for the LLM.
- [ ] Implement Calendar availability checker.
- [ ] Implement Event Creation logic.

## Phase 4: Automated Communication
- [ ] Create email templates for confirmations and rejections.
- [ ] Integrate SMTP/Gmail Send for replies.

## Phase 5: Automation & Deployment
- [ ] Set up CRON job/Scheduler (15-minute intervals).
- [ ] Logging and monitoring setup.
