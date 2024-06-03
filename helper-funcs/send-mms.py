import os
from dotenv import load_dotenv
from twilio.rest import Client
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


text='This is the ship that made the Kessel Run in fourteen parsecs? what up what up'

aiclient = OpenAI()
response = aiclient.images.generate(
  model="dall-e-3",
  prompt=text,
  size="1024x1024",
  quality="standard",
  n=1,
)

media_url=response.data[0].url


# actual twilio SMS (use with care!!!!!!!!!)
message = client.messages \
    .create(
         body=text,
         media_url=media_url,
         from_='+18337991342',
         to='+'
     )


print(message.sid)
