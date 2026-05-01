from langchain.tools import tool
from datetime import datetime, timedelta, timezone
from dateparser import parse

from auth import get_calendar_service

service = get_calendar_service()

@tool
def create_calendar_event(summary: str, start_time: str, end_time: str):
    """
    Create a Google Calendar event.
    """
    start_time = parse(start_time,
        settings={
            "TIMEZONE": "Asia/Kolkata",
            "RETURN_AS_TIMEZONE_AWARE": True
        })
    if end_time:
        end_time = parse(end_time,
                          settings={
                              "TIMEZONE": "Asia/Kolkata",
                              "RETURN_AS_TIMEZONE_AWARE": True
                          })
    else:
        end_time = start_time + timedelta(hours=1)    
    print(f"Parsed end time: {end_time}")
    

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
    print(f"Creating event: {event}")

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return "Event created successfully"

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
        maxResults=24,
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
            "id": event["id"],
            "summary": event["summary"],
            "start": start,
            "end": end
        })
        
    if len(event_list) == 0:
        return "No upcoming events found."
    
    return event_list   

print(get_upcoming_events.invoke({}))

@tool
def delete_calendar_event(event_id: str):
    """
    Delete a Google Calendar event using its event ID.
    """
    service.events().delete(
        calendarId="primary",
        eventId=event_id
    ).execute()

    return f"Event {event_id} deleted successfully."