from typing import Any, Dict, List, Optional

from fastmcp import FastMCP


mcp = FastMCP("Meeting MCP Agent")


@mcp.tool()
def fetch_new_emails(query: str = "is:unread") -> List[Dict[str, Any]]:
    """
    Fetch new Gmail messages that match the given Gmail search query.
    Default query fetches unread emails.
    """
    from gmail_service import GmailService

    gmail_service = GmailService()
    return gmail_service.fetch_new_emails(query=query)


@mcp.tool()
def parse_meeting_request(email_body: str) -> Dict[str, Any]:
    """
    Parse an email body and extract structured meeting-request details.
    """
    from email_parser import EmailParser

    email_parser = EmailParser()
    details = email_parser.parse_with_llm(email_body)
    return details.model_dump()


@mcp.tool()
def check_calendar_availability(start_iso: str, end_iso: str) -> bool:
    """
    Check whether the primary Google Calendar is free between start_iso and end_iso.
    Both inputs should be ISO 8601 date-time strings.
    """
    from calendar_service import CalendarService

    calendar_service = CalendarService()
    return calendar_service.is_slot_available(start_iso=start_iso, end_iso=end_iso)


@mcp.tool()
def find_alternative_slot(start_iso: str, duration_minutes: int = 60) -> Optional[str]:
    """
    Find an alternative available calendar slot starting from the requested time.
    """
    from calendar_service import CalendarService

    calendar_service = CalendarService()
    return calendar_service.find_alternative_slot(
        start_iso=start_iso,
        duration_minutes=duration_minutes,
    )


@mcp.tool()
def create_calendar_event(
    summary: str,
    start_iso: str,
    end_iso: str,
    attendees: List[str],
    location: str = "Virtual",
) -> Dict[str, Any]:
    """
    Create a Google Calendar event with summary, time range, attendees and location.
    """
    from calendar_service import CalendarService

    calendar_service = CalendarService()
    return calendar_service.create_event(
        summary=summary,
        start_iso=start_iso,
        end_iso=end_iso,
        attendees=attendees,
        location=location,
    )


@mcp.tool()
def send_gmail_reply(
    thread_id: str,
    to: str,
    subject: str,
    body: str,
) -> str:
    """
    Send a Gmail reply inside an existing email thread.
    """
    from gmail_service import GmailService

    gmail_service = GmailService()
    gmail_service.send_reply(
        thread_id=thread_id,
        to=to,
        subject=subject,
        body=body,
    )
    return "Reply sent successfully."


@mcp.tool()
def mark_email_as_read(message_id: str) -> str:
    """
    Mark a Gmail message as read after it was processed by the agent.
    """
    from gmail_service import GmailService

    gmail_service = GmailService()
    gmail_service.mark_as_read(message_id=message_id)
    return "Email marked as read."


if __name__ == "__main__":
    mcp.run()
