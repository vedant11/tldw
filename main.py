import argparse
import os

import litellm
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()  # Load environment variables from .env file

parser=argparse.ArgumentParser()
parser.add_argument("-v","--vid", help="Add video ID", required=True)
parser.add_argument("-s","--summary_type", help="Summary type freetext, e.g. short/medium/long/technical/SFW/etc.", default="succinct")
parser.add_argument("-d", "--debug", help="Print debug information", action="store_true")
args=vars(parser.parse_args())

# args
video_id = args['vid']
summary_desc = args['summary_type']
debug = args['debug']

# assert and process arg
assert video_id != '', 'Please provide a video_id'
if debug:
    litellm.set_verbose = True

# Get summary
raw_transcript = list(YouTubeTranscriptApi.get_transcript(video_id))
trancript = ""
for t in raw_transcript:
    trancript += t['text'] + " "

with open('transcript.txt', 'w') as f:
    f.write(trancript)

res = litellm.completion(
    model=os.getenv('MODEL', 'ollama/llama3'),
    messages=[
        {"role":"system","content":f"help the user to summarize this transcript. Summary should be according to what user needs: {summary_desc}"},
        {"role":"user","content":trancript}
    ]
)

# Save summary
with open('summary.txt', 'w') as f:
    f.write(res.choices[0].message['content'])
