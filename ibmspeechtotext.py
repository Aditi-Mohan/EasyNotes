from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from write_transcript_to_notion import write_transcript
# from ../../Desktop import converted.wav

api_key = IAMAuthenticator("acyFMIII31gP3u8wJKIwnDAS6mx5NMiUV698g9VFsodj")
speech_2_text = SpeechToTextV1(authenticator=api_key)
speech_2_text.set_service_url("https://api.jp-tok.speech-to-text.watson.cloud.ibm.com/instances/f8ab0ba3-dcfd-427f-8506-d3822ca14d21")

audio_file_path = "../../Desktop/converted.wav"
with open(audio_file_path, "rb") as audio_file:
    result = speech_2_text.recognize(
        audio=audio_file,
        content_type="audio/wav"
    ).get_result()

result = result['results']

text = []
para_break = 
for i in result:
    alts = i['alternatives']
    confs = [x['confidence'] for x in alts]
    imax = 0
    if len(alts) > 1:
        imax = confs.index(max(confs))
    res = alts[imax]['transcript']
    text += [res+"."]
print(text)
write_transcript("Lesson 2", transcript=text, sub_name="Happiness")

# Frame as Paraghraphs
# slice audio into parts and send to model to show in progress bar
# 60 mins of audio -> 36 second = 1%
# therefore feed 36 second long sections of audio to model at a time

# diferrentiate between voices - and assign colors