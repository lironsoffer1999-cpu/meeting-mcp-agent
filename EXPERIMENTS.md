# Experiments & Research (EXPERIMENTS.md)

## LLM Prompt Iterations

### Version 1: Basic Extraction
"Extract the meeting time from this email."
*Result:* High variance in format.

### Version 2: Structured Output (JSON)
"Act as a scheduling assistant. Extract time, date, and location in JSON format."
*Result:* Improved reliability.

## Research Findings
- Gmail API "Labels" can be used to track agent progress (e.g., `PROCESSED_BY_AI`).
- Timezone handling is the most common failure point in extracted dates.

## Prototype Notes
- Initial tests with Gemini 1.5 Pro show high reasoning capability for complex thread contexts.
