from langchain_core.tools import tool

from gmail_service import (
    connect_gmail,
    get_latest_emails
)


@tool
def gmail_latest_emails():
    """
    Get the latest emails from the user's Gmail account.
    Returns sender, receiver, subject, date, message ID, and body.
    """

    gmail = connect_gmail()

    emails = get_latest_emails(gmail)

    return emails