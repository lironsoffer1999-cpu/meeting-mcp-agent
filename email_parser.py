import logging
import json
import re
from datetime import datetime
import pytz
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from config import config

logger = logging.getLogger(__name__)

class MeetingDetails(BaseModel):
    """
    Structured representation of a meeting request extracted by LLM.
    """
    is_meeting_request: bool = Field(description="Whether the email contains a request for a meeting")
    subject: Optional[str] = Field(None, description="A brief title for the meeting")
    start_time: Optional[str] = Field(None, description="ISO 8601 formatted start time")
    end_time: Optional[str] = Field(None, description="ISO 8601 formatted end time. If not specified, default to 1 hour after start.")
    location: Optional[str] = Field("Virtual", description="Physical location or virtual link")
    participants: list[str] = Field(default_factory=list, description="List of email addresses mentioned")
    reasoning: Optional[str] = Field(None, description="Short explanation of why this was identified as a meeting")

class EmailParser:
    """
    Uses Gemini API to parse unstructured email text into structured meeting data.
    """
    def __init__(self):
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY not found in configuration.")
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-flash-latest")

    def parse_with_llm(self, email_body: str) -> MeetingDetails:
        """
        Sends the email body to Gemini and parses the JSON response.
        """
        # Get current date in the configured timezone
        tz = pytz.timezone(config.TIMEZONE)
        now = datetime.now(tz)
        current_date_str = now.strftime("%A, %B %d, %Y")
        current_time_str = now.strftime("%H:%M:%S")

        system_prompt = (
            "You are a professional scheduling assistant. "
            "Your task is to extract meeting details from the provided email body. "
            "Return a valid JSON object matching the requested schema.\n"
            "Schema:\n"
            "{\n"
            "  \"is_meeting_request\": boolean,\n"
            "  \"subject\": string,\n"
            "  \"start_time\": \"ISO 8601 string\",\n"
            "  \"end_time\": \"ISO 8601 string\",\n"
            "  \"location\": string,\n"
            "  \"participants\": [\"email1\", \"email2\"],\n"
            "  \"reasoning\": string\n"
            "}\n"
            "If the email is NOT a meeting request, set 'is_meeting_request' to false. "
            f"Assume the current date is {current_date_str}. Current time is {current_time_str}. "
            f"Current timezone is {config.TIMEZONE}. "
            "Format dates as ISO 8601 strings, preferably with the timezone offset."
        )

        try:
            prompt = f"{system_prompt}\n\nExtract details from this email:\n\n{email_body}"
            generation_config = {"response_mime_type": "application/json"}
            
            logger.info("--- GEMINI API CALL START ---")
            logger.info(f"Model: {self.model.model_name}")
            logger.info(f"Prompt sent:\n{prompt}")
            logger.info(f"Generation Config: {generation_config}")
            
            # Direct synchronous call to identify if it hangs here
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            logger.info("--- GEMINI API CALL SUCCESS ---")
            raw_content = response.text
            logger.info(f"Raw Gemini response: {raw_content}")
            
            data = json.loads(raw_content)
            
            details = MeetingDetails(**data)
            logger.info(f"Successfully parsed email. is_meeting_request: {details.is_meeting_request}")
            return details

        except Exception as e:
            logger.error("--- GEMINI API CALL FAILURE ---")
            logger.error(f"Error parsing email with Gemini: {e}", exc_info=True)
            # Return a 'safe' negative result on error
            return MeetingDetails(is_meeting_request=False, reasoning=f"Error: {str(e)}")
