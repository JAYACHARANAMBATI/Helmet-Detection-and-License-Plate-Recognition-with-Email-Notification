from twilio.rest import Client
import os

# Your Twilio account credentials
account_sid = 'AC994e319c13db232cca6f817a56dc3fbe'
auth_token = 'bdf02a41fd3f2aab1ba899ac24536cc6'
twilio_phone_number = '+19042404324'  # Add country code to your Twilio number

# Initialize Twilio client
client = Client(account_sid, auth_token)

# List of clients with their phone numbers
clients = [
    {"name": "Ambati Jaya Charan", "phone": "+918074897353"},
]

# Message to send
message_body = "Hello, this is a reminder from [Your Company]. Please check our services."

# Send SMS to each client
for client_info in clients:
    message = client.messages.create(
        body=f"Hi {client_info['name']}, {message_body}",
        from_=twilio_phone_number,
        to=client_info["phone"]
    )
    print(f"Message sent to {client_info['name']} at {client_info['phone']}: SID {message.sid}")
