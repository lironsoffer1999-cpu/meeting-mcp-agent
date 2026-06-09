import schedule
import time
import logging
import re
from gmail_service import GmailService
from calendar_service import CalendarService
from email_parser import EmailParser
from config import config

logger = logging.getLogger(__name__)

class AgentScheduler:
    """
    Orchestrates the 15-minute polling cycle.
    """
    def __init__(self):
        self.gmail = GmailService()
        self.calendar = CalendarService()
        self.parser = EmailParser()

    def run_cycle(self):
        """
        The core logic executed every 15 minutes.
        """
        logger.info("Starting polling cycle...")
        
        # 1. Fetch unread emails with specific subject for E2E test
        emails = self.gmail.fetch_new_emails(query='is:unread subject:"Project Sync Meeting"')
        
        for email in emails:
            logger.info(f"Processing email ID: {email['id']}")
            
            # 2. Parse with LLM
            details = self.parser.parse_with_llm(email['body'])
            
            if details.is_meeting_request and details.start_time:
                # Ensure sender is in participants for the event
                sender_email = email['sender']
                # Basic extraction of email from "Name <email@domain.com>"
                match = re.search(r'[\w\.-]+@[\w\.-]+', sender_email)
                clean_sender = match.group(0) if match else sender_email

                all_attendees = details.participants
                if clean_sender not in all_attendees:
                    all_attendees.append(clean_sender)

                # 3. Check Calendar
                if self.calendar.is_slot_available(details.start_time, details.end_time):
                    # 4. Create Event
                    self.calendar.create_event(
                        summary=details.subject or "Meeting Request",
                        start_iso=details.start_time,
                        end_iso=details.end_time,
                        attendees=all_attendees,
                        location=details.location
                    )
                    # 5. Confirm via Email
                    self.gmail.send_reply(
                        thread_id=email['threadId'],
                        to=clean_sender,
                        subject=f"Re: {details.subject}",
                        body=f"Hello,\n\nI've successfully scheduled our meeting: {details.subject}.\nTime: {details.start_time}\nLocation: {details.location}\n\nSee you then!"
                    )
                else:
                    # 6. Adaptive Scheduling: Suggest alternative
                    alt_slot = self.calendar.find_alternative_slot(details.start_time)
                    alt_msg = f"How about {alt_slot} instead?" if alt_slot else "Please suggest another time."
                    
                    # 6b. Send Rejection with Alternative
                    self.gmail.send_reply(
                        thread_id=email['threadId'],
                        to=clean_sender,
                        subject=f"Re: {details.subject}",
                        body=f"Hello,\n\nThank you for the request. Unfortunately, I am busy at the requested time ({details.start_time}).\n\n{alt_msg}\n\nBest regards."
                    )
            
            # 7. Mark as read regardless of result to avoid infinite loops
            self.gmail.mark_as_read(email['id'])

    def start(self):
        """
        Starts the scheduler.
        """
        schedule.every(config.POLLING_INTERVAL_MINUTES).minutes.do(self.run_cycle)
        logger.info(f"Scheduler initialized. Running every {config.POLLING_INTERVAL_MINUTES} minutes.")
        
        # Run immediately on start
        self.run_cycle()
        
        while True:
            schedule.run_pending()
            time.sleep(1)
