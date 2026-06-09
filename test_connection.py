import os
import logging
from google_auth import get_google_service
from datetime import datetime

# Configure logging for the test script
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def test_google_setup():
    """
    Diagnostic script to verify Google API connectivity and authentication.
    """
    print("-" * 50)
    print("Meeting MCP Agent - Connection Test")
    print("-" * 50)

    # 1. Check for credentials.json
    if not os.path.exists('credentials.json'):
        print("[FAIL] credentials.json not found in the root directory.")
        print("       Please follow the README instructions to download it from Google Cloud Console.")
        return
    print("[PASS] credentials.json exists.")

    try:
        # 2. Test Authentication and Services
        print("\nChecking Authentication & Initializing Services...")
        
        # Test Gmail Service
        gmail_service = get_google_service('gmail', 'v1')
        print("[PASS] Gmail Service authenticated.")

        # Test Calendar Service
        calendar_service = get_google_service('calendar', 'v3')
        print("[PASS] Calendar Service authenticated.")

        # 3. Check for token.json
        if os.path.exists('token.json'):
            print("[PASS] token.json generated/exists.")
        else:
            print("[WARN] token.json not found (this is normal on the very first run).")

        # 4. Fetch 5 Recent Emails
        print("\nFetching last 5 emails...")
        results = gmail_service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])
        if not messages:
            print("       No emails found.")
        for msg in messages:
            msg_data = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
            print(f"       - {msg_data.get('snippet')[:70]}...")

        # 5. Fetch 5 Upcoming Calendar Events
        print("\nFetching next 5 calendar events...")
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = calendar_service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=5, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            print("       No upcoming events found.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"       - {start}: {event.get('summary')}")

        print("\n" + "=" * 50)
        print("  SUCCESS: Google API environment is correctly configured!")
        print("=" * 50)

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Test failed: {e}")
        print("Please check your credentials.json and ensure you have enabled Gmail and Calendar APIs.")

if __name__ == "__main__":
    test_google_setup()
