from pytube import YouTube, Channel
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api

class VideoData (YouTube):
	def __init__(self,url):
		super().__init__(url)
		self.transcript=YouTubeTranscriptApi.get_transcript(self.video_id)


def get_transcript(url):
	return YouTubeTranscriptApi.get_transcript(url.split('watch?v=')[-1])

if __name__=="__main__":
	url='https://www.youtube.com/watch?v=p60L-TOecik'

	#print(dir(youtube_transcript_api))
	#print(get_transcript(url))
	data=VideoData(url)
	ch=Channel(data.channel_url)
	print(ch.videos_generator)
	#print(dir(ch))
	#print(ch.videos)
	#print(dir(data))
	#print(data.__dict__.keys())
	