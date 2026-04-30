from langchain.tools import tool
from datetime import datetime, timedelta

from auth import get_calendar_service

service = get_calendar_service()

@tool
def create_calendar_event(summary: str):
    """
    Create a Google Calendar event.
    """

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    event = {
        "summary": summary,

        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },

        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return "Event created successfully"
# TEST
print(
    create_calendar_event.invoke(
        "DSA Practice Session"
    )
)