from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
aiclient = OpenAI()

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Start our TwiML response
    resp = MessagingResponse()

    body = request.values.get('Body', None)
    response = aiclient.images.generate(
        model="dall-e-3",
        prompt=body,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    msg = resp.message()
    # Add a picture message
    msg.media(
        response.data[0].url
    )

    return str(resp)

if __name__ == "__main__":
    app.run( host='0.0.0.0',port=8080, debug=True)
