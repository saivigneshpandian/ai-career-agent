from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os
import base64
from bs4 import BeautifulSoup

# Gmail permission
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# 1. CONNECT TO GMAIL

def connect_gmail():

    creds = None

    # Check if we already authenticated before
    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # If credentials don't exist or are invalid
    if not creds or not creds.valid:

        # Refresh expired credentials
        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        # First-time login
        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open("token.json", "w") as token:

            token.write(creds.to_json())

    # Create Gmail API client
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
        ).decode("utf-8", errors="ignore")

        # If HTML, convert it to clean text
        if payload.get("mimeType") == "text/html":

            soup = BeautifulSoup(decoded_body, "html.parser")

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
                    ).decode("utf-8", errors="ignore")


        # If plain text isn't available, use HTML
        for part in payload["parts"]:

            if part["mimeType"] == "text/html":

                body = part["body"].get("data")

                if body:

                    decoded_body = base64.urlsafe_b64decode(
                        body
                    ).decode("utf-8", errors="ignore")

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

def get_latest_emails(service):

    # Get latest 5 email messages
    results = service.users().messages().list(
        userId="me",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    print("\nLatest Gmail Messages:\n")


    # Process each email
    for message in messages:

        # Get complete email information
        message_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()


        # -----------------------------
        # Extract email headers
        # -----------------------------

        headers = message_data["payload"]["headers"]

        sender = ""
        receiver = ""
        subject = ""
        date = ""


        for header in headers:

            if header["name"].lower() == "from":

                sender = header["value"]


            elif header["name"].lower() == "to":

                receiver = header["value"]


            elif header["name"].lower() == "subject":

                subject = header["value"]


            elif header["name"].lower() == "date":

                date = header["value"]


        # -----------------------------
        # Extract email body
        # -----------------------------

        body = get_email_body(message_data)


        # -----------------------------
        # Display email
        # -----------------------------

        print("--------------------------------")

        print("From:", sender)

        print("To:", receiver)

        print("Subject:", subject)

        print("Date:", date)

        print("Message ID:", message["id"])

        print("Body:")

        print(body)


# 4. PROGRAM START

if __name__ == "__main__":

    gmail = connect_gmail()

    print("Gmail connected successfully")

    get_latest_emails(gmail)