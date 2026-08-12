from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os
import base64

from bs4 import BeautifulSoup


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# 1. CONNECT TO GMAIL

def connect_gmail():

    creds = None

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
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

        with open("token.json", "w") as token:

            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


# 2. EXTRACT EMAIL BODY

def get_email_body(message_data):

    payload = message_data["payload"]

    # Simple email
    if "body" in payload and payload["body"].get("data"):

        body = payload["body"]["data"]

        decoded_body = base64.urlsafe_b64decode(
            body
        ).decode(
            "utf-8",
            errors="ignore"
        )

        if payload.get("mimeType") == "text/html":

            soup = BeautifulSoup(
                decoded_body,
                "html.parser"
            )

            return soup.get_text(
                separator="\n",
                strip=True
            )

        return decoded_body

    # Multipart email
    if "parts" in payload:

        # First look for plain text
        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                body = part["body"].get("data")

                if body:

                    return base64.urlsafe_b64decode(
                        body
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

        # If plain text isn't available, use HTML
        for part in payload["parts"]:

            if part["mimeType"] == "text/html":

                body = part["body"].get("data")

                if body:

                    decoded_body = base64.urlsafe_b64decode(
                        body
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

                    soup = BeautifulSoup(
                        decoded_body,
                        "html.parser"
                    )

                    return soup.get_text(
                        separator="\n",
                        strip=True
                    )

    return ""


# 3. GET LATEST EMAILS

def get_latest_emails(service, max_results=5):

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get(
        "messages",
        []
    )

    emails = []

    for message in messages:

        message_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = message_data["payload"]["headers"]

        sender = ""
        receiver = ""
        subject = ""
        date = ""

        for header in headers:

            name = header["name"].lower()

            if name == "from":

                sender = header["value"]

            elif name == "to":

                receiver = header["value"]

            elif name == "subject":

                subject = header["value"]

            elif name == "date":

                date = header["value"]

        body = get_email_body(
            message_data
        )

        email = {
            "id": message["id"],
            "from": sender,
            "to": receiver,
            "subject": subject,
            "date": date,
            "body": body
        }

        emails.append(email)

    return emails