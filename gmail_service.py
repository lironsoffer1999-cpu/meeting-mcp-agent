import logging
import base64
from typing import List, Dict, Any
from email.mime.text import MIMEText

from google_auth import get_google_service

logger = logging.getLogger(__name__)

class GmailService:
    """
    Handles interactions with the Gmail API.
    """
    def __init__(self):
        self.service = get_google_service('gmail', 'v1')

    def fetch_new_emails(self, query: str = "is:unread") -> List[Dict[str, Any]]:
        """
        Retrieves unread emails from the inbox and decodes their content.
        """
        logger.info(f"Fetching emails with query: {query}")
        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            
            processed_emails = []
            for msg in messages:
                txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                
                # Basic decoding of email body
                payload = txt.get('payload', {})
                body = ""
                
                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body'].get('data', '')
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                else:
                    data = payload.get('body', {}).get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')

                # Extract Sender
                headers = txt.get('payload', {}).get('headers', [])
                sender = ""
                for header in headers:
                    if header['name'] == 'From':
                        sender = header['value']
                        break

                processed_emails.append({
                    'id': msg['id'],
                    'threadId': txt['threadId'],
                    'body': body,
                    'snippet': txt.get('snippet', ''),
                    'sender': sender
                })
            
            return processed_emails
        except Exception as e:
            logger.error(f"Error fetching emails from Gmail: {e}")
            return []

    def _extract_email(self, address_string: str) -> str:
        """
        Extracts clean email from "Name <email@domain.com>" or returns original.
        """
        import re
        match = re.search(r'[\w\.-]+@[\w\.-]+', address_string)
        return match.group(0) if match else address_string

    def send_reply(self, thread_id: str, to: str, subject: str, body: str):
        """
        Sends an automated reply to a specific email thread.
        """
        clean_to = self._extract_email(to)
        logger.info(f"Sending reply to {clean_to} (original: {to}) on thread {thread_id}")
        try:
            message = MIMEText(body)
            message['to'] = clean_to
            message['subject'] = subject
            message['In-Reply-To'] = thread_id
            message['References'] = thread_id
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            self.service.users().messages().send(userId='me', body={'raw': raw, 'threadId': thread_id}).execute()
            logger.info("Reply sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send reply: {e}")

    def mark_as_read(self, message_id: str):
        """
        Removes the 'UNREAD' label from a message.
        """
        try:
            self.service.users().messages().modify(
                userId='me', 
                id=message_id, 
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            logger.error(f"Error marking email {message_id} as read: {e}")
