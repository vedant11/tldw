import litellm
import os

from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

video_id = ''
assert video_id != '', 'Please provide a video_id'
raw_transcript = list(YouTubeTranscriptApi.get_transcript(video_id))
trancript = ""
for t in raw_transcript:
    trancript += t['text'] + " "

with open('transcript.txt', 'w') as f:
    f.write(trancript)

res = litellm.completion(
    model=os.getenv('MODEL', 'llama3'),
    messages=[
        {"role":"system","content":"help the user to summarize this transcript"},
        {"role":"user","content":trancript}
    ]
)

with open('summary.txt', 'w') as f:
    f.write(res.choices[0].message['content'])
