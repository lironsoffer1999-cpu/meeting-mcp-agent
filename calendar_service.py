import logging
from datetime import datetime, timedelta
from typing import Optional, List

from google_auth import get_google_service
from config import config

logger = logging.getLogger(__name__)

class CalendarService:
    """
    Handles interactions with the Google Calendar API.
    """
    def __init__(self):
        self.service = get_google_service('calendar', 'v3')

    def is_slot_available(self, start_iso: str, end_iso: str) -> bool:
        """
        Checks if the user is 'Free' during the requested time range using freebusy query.
        """
        logger.info(f"Checking availability from {start_iso} to {end_iso}")
        try:
            body = {
                "timeMin": start_iso,
                "timeMax": end_iso,
                "items": [{"id": "primary"}]
            }
            events_result = self.service.freebusy().query(body=body).execute()
            busy_slots = events_result.get('calendars', {}).get('primary', {}).get('busy', [])
            
            return len(busy_slots) == 0
        except Exception as e:
            logger.error(f"Error checking calendar availability: {e}")
            return False # Assume busy on error for safety

    def find_alternative_slot(self, start_iso: str, duration_minutes: int = 60) -> Optional[str]:
        """
        Finds the next available slot starting from the requested time.
        Checks in 1-hour increments for the next 24 hours.
        """
        logger.info(f"Searching for alternative slot after {start_iso}")
        try:
            current_attempt = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
            
            for _ in range(24): # Try next 24 slots
                current_attempt += timedelta(hours=1)
                potential_start = current_attempt.isoformat().replace('+00:00', 'Z')
                potential_end = (current_attempt + timedelta(minutes=duration_minutes)).isoformat().replace('+00:00', 'Z')
                
                if self.is_slot_available(potential_start, potential_end):
                    logger.info(f"Found alternative slot: {potential_start}")
                    return potential_start
            
            return None
        except Exception as e:
            logger.error(f"Error finding alternative slot: {e}")
            return None

    def create_event(self, summary: str, start_iso: str, end_iso: str, attendees: List[str], location: str = "Virtual"):
        """
        Creates a new event on the primary calendar.
        """
        logger.info(f"Creating event: {summary} at {start_iso}")
        try:
            event = {
                'summary': summary,
                'location': location,
                'description': 'Automatically scheduled by Meeting MCP Agent',
                'start': {'dateTime': start_iso, 'timeZone': config.TIMEZONE},
                'end': {'dateTime': end_iso, 'timeZone': config.TIMEZONE},
                'attendees': [{'email': email} for email in attendees],
            }
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f"Event created: {event.get('htmlLink')}")
            return event
        except Exception as e:
            logger.error(f"Failed to create calendar event: {e}")
            return None
