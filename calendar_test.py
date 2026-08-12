from calendar_service import( 
    connect_calendar,
    get_upcoming_events,
    create_calendar_event)


calendar = connect_calendar()

print("Google Calendar connected successfully! ✅")
#get_upcoming_events(calendar)
event = create_calendar_event(
    calendar,
    summary="AI Career Agent Test",
    start_time="2026-08-12T10:00:00+05:30",
    end_time="2026-08-12T11:00:00+05:30",
    description="Testing Google Calendar integration for AI Career Agent."
)


