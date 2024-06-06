from youtube_transcript_api import YouTubeTranscriptApi

video_id = ''
assert video_id != '', 'Please provide a video_id'
raw_transcript = list(YouTubeTranscriptApi.get_transcript(video_id))
trancript = ""
for t in raw_transcript:
    trancript += t['text'] + " "

with open('transcript.txt', 'w') as f:
    f.write(trancript)
