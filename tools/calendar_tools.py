from langchain.tools import tool
from datetime import datetime, timedelta, timezone

from auth import get_calendar_service

service = get_calendar_service()

@tool
def create_calendar_event(summary: str):
    """
    Create a Google Calendar event.
    """

    start_time = datetime.now() + timedelta(minutes=5)  # Event starts 5 minutes from now
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


@tool
def get_upcoming_events():
    """
    Get the upcoming events from Google Calendar.
    """

    now = datetime.now(
        tz=timezone.utc
    ).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    if not events:
        return "No upcoming events found."
    
    event_list = []
    for event in events:

        start = (
            event["start"].get("dateTime")
            or event["start"].get("date")
        )

        end = (
            event["end"].get("dateTime")
            or event["end"].get("date")
        )

        event_list.append({
            "summary": event["summary"],
            "start": start,
            "end": end
        })
        
    return event_list

# TEST
print(
     get_upcoming_events.invoke({})
)   