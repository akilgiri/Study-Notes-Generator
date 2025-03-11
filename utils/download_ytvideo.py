from pytubefix import YouTube

video_url = str(input("Input the URL for the youtube video: "))

# YouTube('https://www.youtube.com/watch?v=4kkJOtvTxdc&list=PLUVKdrSzO0M61rb6v_3D1C9bCv0cEBxP7&index=16').streams.first().download()
# yt = YouTube('https://www.youtube.com/watch?v=4kkJOtvTxdc&list=PLUVKdrSzO0M61rb6v_3D1C9bCv0cEBxP7&index=16')

YouTube(video_url).streams.first().download()
yt = YouTube(video_url)

yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()