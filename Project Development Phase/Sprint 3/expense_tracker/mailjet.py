
from mailjet_rest import Client
from flask import current_app, g


def send_email_alert():

    mail_api_key = "21c0ad8bf9d858b7254a01283e29d097"
    mail_api_secret = "90a702edf91a1d6832ca6bd0475c3b4b"
    mail_admin = "ajaisaikumar@student.tce.edu"
    mailjet = Client(auth=(mail_api_key, mail_api_secret), version='v3.1')
    name = g.user["NAME"]
    email = g.user["EMAIL"]
    data = {
        'Messages': [
            {
                "From": {
                    "Email": mail_admin,
                    "Name": "Admin"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": name
                    }
                ],
                "Subject": "Expense Alert",
                "HTMLPart": f"<h3>Dear {name},<br/> your expenses have crossed the monthly expense limit set by you.",
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result)