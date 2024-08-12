
# Video Transcript Summarizer using Google Gemini API

This Python application uses the Google Gemini API to generate summaries of video transcripts with timestamps. It features a simple web interface built with FastHTML, allowing users to paste a transcript and receive a concise summary.

## Features

* **Summary Generation:** Extracts key information from a YouTube video transcript using the Google Gemini API.
* **Timestamp Integration:** Includes timestamps in the summary, indicating the start time of each bullet point.
* **Simple Web Interface:** Provides a user-friendly interface for pasting transcripts and viewing summaries.
* **Model Selection:** Offers a choice between `gemini-1.5-flash-latest` and `gemini-1.5-pro-exp-0801` models.
* **YouTube Comment Formatting:** Replaces `**` with `*` and `*: ` with `:*` to make the summary more readable in YouTube comments.


## Installation

1. **Install Micromamba:**

   ```bash
   ${SHELL} <(curl -L micro.mamba.pm/install.sh)
   ```

2. **Create a Python environment:**

   ```bash
   micromamba create python
   ```

3. **Install required packages:**

   ```bash
   pip install python-fasthtml requests
   ```

4. **Obtain a Google Gemini API Key:**

   * Follow the instructions to get an API key from the Google Cloud Platform.
   * Save the API key in a file named `api_key.txt` in the same directory as the `host.py` script.


## Usage

1. **Run the application:**

   ```bash
   python host.py
   ```

2. **Open the web interface:**

   * Navigate to `http://127.0.0.1:5001` in your web browser.

3. **Copy the YouTube Transcript:**

   * Go to a YouTube video.
   * Click on the "Show Transcript" button below the video.
   * Copy the entire transcript, including timestamps.

4. **Paste the Transcript into the Web Interface:**

   * Paste the copied transcript into the text area provided.
   * Choose your desired model from the dropdown menu.
   * Click the "Send Transcript" button.

5. **View the Summary:**

   * The summarized transcript with timestamps will be displayed below the input area.

## Alternative: Google AI Studio with Prompts

You can achieve similar results using Google AI Studio with two prompts:

**Prompt 1:**
```
I don't want to watch the video. Create a self-contained bullet list summary from the following transcript that I can understand without watching the video. [Paste Transcript Here]
```

**Prompt 2:**
```
Add starting (not stopping) timestamps to each bullet point.
```
This refers to the previous response.

**Model Recommendation:** Pro for Accurate Timestamps
While the application offers a choice between Flash and Pro models, it's highly recommended to always use the Pro model for accurate timestamps. The Flash model struggles to provide reliable timestamps unless the video is very short (under 5 minutes).


## Limitations

* **Word Limit:** The current implementation restricts transcript length to 20,000 words.
* **Rate Limiting:** The free Gemini tier may require a waiting period to avoid rate limiting, especially for longer transcripts.


## Potential Improvements

* **Real-Time Feedback:** Provide users with feedback on the progress of the summarization process.
* **Rate Limiting Handling:** Implement strategies to handle rate limiting gracefully, such as adding pauses or displaying informative messages.
