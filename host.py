#!/usr/bin/env python3

from fasthtml.common import *
import requests
import json

app, rt = fast_app(live=False)

# Load your Google Gemini API key
with open("api_key.txt") as f:
    api_key = f.read().strip()

@rt("/")
def get():
    frm = Form(
        Group(
            Textarea(placeholder="Paste YouTube video transcript here", name="transcript"),
            Select(
                Option("gemini-1.5-pro-exp-0801"),
                Option("gemini-1.5-flash-latest"),
                name="model" 
            ),
            Button("Send Transcript", hx_post="/process_transcript")
        ),
        hx_post="/process_transcript",
        hx_target="#summary"
    )
    return Title("Video Transcript Summarizer"), Main(
        H1("Summarizer Demo"),
        Card(Div(id="summary"), header=frm)
    )

@rt("/process_transcript")
async def post(transcript: str, model: str):
    # Check word count
    words = transcript.split()
    if len(words) > 20000:
        return Div("Error: Transcript exceeds 20,000 words. Please shorten it.", id="summary")

    # Prepare the prompt for the Gemini API
    prompt = "I don't want to watch the video. Create a self-contained bullet list summary from the following transcript that I can understand without watching the video. " + transcript

    # Set up the API request
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    safety = [{"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE"},
              {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE"}]
    data = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 2.0},
            "safetySettings": safety}
    data = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    # Make the API call for summary
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        summary = response.json()['candidates'][0]['content']['parts'][0]['text']
        input_tokens = response.json()['usageMetadata']['promptTokenCount']
        output_tokens = response.json()['usageMetadata']['candidatesTokenCount']
        # Second API call to add timestamps
        prompt_with_timestamps = f"Add starting (not stopping) timestamp to each bullet point in the following summary: {summary}\nThe full transcript is: {transcript}"
        data_with_timestamps = {"contents": [{"parts": [{"text": prompt_with_timestamps}]}],
                                "safetySettings": safety}
        data_with_timestamps = json.dumps(data_with_timestamps)
        response_with_timestamps = requests.post(url, headers=headers, data=data_with_timestamps)

        if response_with_timestamps.status_code == 200:
            summary_with_timestamps = response_with_timestamps.json()['candidates'][0]['content']['parts'][0]['text']
            input_tokens2 = response_with_timestamps.json()['usageMetadata']['promptTokenCount']
            output_tokens2 = response_with_timestamps.json()['usageMetadata']['candidatesTokenCount']
            # Youtube comments are not proper markdown, modify the summary to be more readable
            summary_with_timestamps = summary_with_timestamps.replace("**", "*")
            summary_with_timestamps = summary_with_timestamps.replace("*:", ":*")
            
            if model == "gemini-1.5-pro-exp-0801":
                price_input_token_usd_per_mio = 3.5
                price_output_token_usd_per_mio = 10.5
            else:
                price_input_token_usd_per_mio = 0.075
                price_output_token_usd_per_mio = 0.3
            cost_input = (input_tokens+input_tokens2) / 1_000_000 * price_input_token_usd_per_mio
            cost_output = (output_tokens+output_tokens2) / 1_000_000 * price_output_token_usd_per_mio

            summary_pre = f"""*Summary*
{summary_with_timestamps}
Summarized by AI model: {model}
Cost (if I didn't use the free tier): ${cost_input+cost_output:.4f}
Input tokens: {input_tokens+input_tokens2}
Output tokens: {output_tokens+output_tokens2}
"""
            return Pre(summary_pre, id="summary")
        else:
            return Div(f"Error adding timestamps: {response_with_timestamps.status_code}", id="summary")
    else:
        return Div(f"Error generating summary: {response.status_code}", id="summary")

serve()
