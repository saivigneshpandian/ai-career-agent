from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


# Connect to Google Calendar

def connect_calendar():

    creds = None

    if os.path.exists("calendar_token.json"):

        creds = Credentials.from_authorized_user_file(
            "calendar_token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("calendar_token.json", "w") as token:

            token.write(creds.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


# Get upcoming calendar events

def get_upcoming_events(service, max_results=5):

    events_result = service.events().list(
        calendarId="primary",
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get(
        "items",
        []
    )

    print("\nUpcoming Calendar Events:\n")

    if not events:

        print("No upcoming events found.")

        return []

    for event in events:

        event_id = event.get("id")

        summary = event.get(
            "summary",
            "No title"
        )

        start = event.get(
            "start",
            {}
        )

        start_time = (
            start.get("dateTime")
            or start.get("date")
            or "Unknown"
        )

        print("--------------------------------")

        print("Event:", summary)

        print("Start:", start_time)

        print("Event ID:", event_id)

    return events


# Create a calendar event

def create_calendar_event(
    service,
    summary,
    start_time,
    end_time,
    description=""
):

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata"
        }
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    print("\nCalendar event created successfully! ✅")

    print(
        "Event:",
        created_event.get("summary")
    )

    print(
        "Event ID:",
        created_event.get("id")
    )

    print(
        "Link:",
        created_event.get("htmlLink")
    )

    return created_event