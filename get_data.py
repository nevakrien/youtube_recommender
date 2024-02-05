from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api

# def get_data(url):
# 	yt = YouTube(url)
# 	ts=YouTubeTranscriptApi.get_transcript(yt.video_id)
	
# 	yt.transcript=ts 

# 	return yt#.__dict__

def get_transcript(url):
	return YouTubeTranscriptApi.get_transcript(url.split('watch?v=')[-1])

if __name__=="__main__":
	url='https://www.youtube.com/watch?v=p60L-TOecik'

	print(dir(youtube_transcript_api))
	#print(get_transcript(url))
	