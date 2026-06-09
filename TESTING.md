# Testing Strategy (TESTING.md)

## 1. Unit Testing
- Extraction logic (passing mock email text to LLM mocks).
- Date/Time parsing and normalization.
- Conflict detection logic.

## 2. Integration Testing
- Google API authentication flow.
- End-to-end flow: Mock Email -> Agent -> Mock Calendar Event.

## 3. Test Cases
- **Scenario A:** Valid request, slot is free -> Event created + Reply sent.
- **Scenario B:** Valid request, slot is busy -> No event + Rejection sent.
- **Scenario C:** Vague email (no date) -> Agent asks for clarification (Stretch Goal).
- **Scenario D:** Non-meeting email -> Ignored.

## 4. Tools
- Jest / Vitest (Node) or Pytest (Python).
- Nock for HTTP mocking.
