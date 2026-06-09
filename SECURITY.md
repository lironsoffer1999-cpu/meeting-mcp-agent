# Security Protocol (SECURITY.md)

## 1. Data Protection
- **Credentials:** All API keys and secrets must be stored in `.env` files and never committed to source control.
- **Tokens:** Google OAuth2 tokens should be stored securely (encrypted at rest if possible).

## 2. Principle of Least Privilege
- The Google Cloud Project should only be granted specific scopes:
  - `https://www.googleapis.com/auth/gmail.modify` (Read/Mark as Read)
  - `https://www.googleapis.com/auth/calendar` (Manage events)

## 3. PII Handling
- Emails are processed in-memory. 
- No permanent storage of email bodies beyond the processing window.

## 4. LLM Safety
- Input sanitization to prevent prompt injection.
- Explicit checks to ensure the LLM doesn't "hallucinate" permissions.
