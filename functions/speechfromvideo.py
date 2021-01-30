import speech_recognition as sr 
import moviepy.editor as mp

VIDEO_FILE = "video_recording.mp4"
OUTPUT_AUDIO_FILE = "converted.wav"
OUTPUT_TEXT_FILE = "recognized.txt"

video_clip = mp.VideoFileClip(r"{}".format(VIDEO_FILE))
video_clip.audio.write_audiofile(r"{}".format(OUTPUT_AUDIO_FILE))

r = sr.Recognizer()
audio_clip = sr.AudioFile(r"{}".format(OUTPUT_AUDIO_FILE))
with audio_clip as source:
  audio_file = r.record(source)
result = r.recognize_google(audio_file)

# exporting the result 
with open('recognized.txt',mode ='w') as file: 
   file.write("Recognized Speech:") 
   file.write("\n") 
   file.write(result) 
   print("ready!")
