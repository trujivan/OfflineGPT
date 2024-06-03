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
aiclient = OpenAI()

prompt='This is the ship that made the Kessel Run in fourteen parsecs? what up what up'

completion = aiclient.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an assistant that is being fed various prompts via python script"},
    {"role": "user", "content": prompt}
  ]
)

text=completion.choices[0].message.content

print(text)


# actual twilio SMS (use with care!!!!!!!!!)
message = client.messages \
    .create(
         body=text,
         from_='+18337991342',
         to='+'
     )

print(message.sid)
