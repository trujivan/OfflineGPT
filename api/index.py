from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
aiclient = OpenAI()
DEFAULT_RESPONSE ="""Welcome to OfflineGPT.
- Text 'Gpt' to use ChatGPT 3.5-turbo to generate a response based on provided text.
- Text 'Dalle' to use DALL-E to generate an image based on provided text keywords.
- Text 'Stop' to no more messaging from the service."""

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Start our TwiML response
    resp = MessagingResponse()
    
    body = request.values.get('Body', '').strip().lower()
    
    if 'gpt' in body:
        prompt_text = body.replace('generate text', '', 1)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
           messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ]
        )
        msg = resp.message(response.choices[0].message['content'].strip())
    
    elif 'dalle' in body:
        prompt_text = body.replace('image generate ', '', 1)
         response = aiclient.images.generate(
        model="dall-e-2",
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
    elif 'stop' in body:
        msg = resp.message("No more messaging from the service.")
    
    else:
        msg = resp.message(DEFAULT_RESPONSE)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)