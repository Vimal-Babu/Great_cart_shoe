# Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client
# from decouple import config



# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = config("TWILIO_ACCOUNT_SID")
# auth_token = config("TWILIO_AUTH_TOKEN")

# client = Client(account_sid, auth_token)

# message = client.messages \
#     .create(
#         body='This is the ship that made the Kessel Run in fourteen parsecs?',
#         from_='+18159892367',
#         to='+919567250335'
#     )

# print(message.sid)