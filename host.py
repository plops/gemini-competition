#!/usr/bin/env python

from fasthtml.common import *
import requests
import json

app, rt = fast_app(live=True)

# Load your Google Gemini API key
with open("/home/kiel/api_key.txt") as f:
    api_key = f.read().strip()

@rt("/")
def get():
    frm = Form(
        Group(Textarea(placeholder="Paste YouTube video transcript here", name="transcript"), 
              Button("Send Transcript", hx_post="/process_transcript")), 
        hx_post="/process_transcript", 
        hx_target="#summary"
    )
    return Title("Video Transcript Summarizer"), Main(
        H1("Summarizer Demo"),
        Card(Div(id="summary"), header=frm)
    )

@rt("/process_transcript")
async def post(transcript: str):
    # Prepare the prompt for the Gemini API
    prompt = "I don't want to watch the video. Create a self-contained bullet list summary from the following transcript that I can understand without watching the video. " + transcript

    # Set up the API request
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + api_key
    safety = [{"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE"},
              {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE"}]
    data = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 2.0},
            "safetySettings": safety}
    data = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    # Make the API call
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        summary = response.json()['candidates'][0]['content']['parts'][0]['text']
        # Youtube comments are not proper markdown, modify the summary to be more readable
        summary = summary.replace("**", "*")
        summary = summary.replace("*:", ":")
        return Div(f"*Summary*\n{summary}", id="summary")
    else:
        return Div(f"Error: {response.status_code}", id="summary")

serve()