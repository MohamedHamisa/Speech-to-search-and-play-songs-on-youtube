# ## Speech Recognition using Python



# Import Speech Recogition Package
!pip install SpeechRecognition
import speech_recognition as spr




# Validate the installation
spr.__version__




recog = spr.Recognizer()






# ### Convert Speech to Text



speech = spr.AudioFile('speech.wav')
with speech as filesource:
    audio = recog.record(filesource)




recog.recognize_google(audio)


# ### Convert Speech to Text - Capture only particular segments of audio using offset and duration



with speech as filesource:
    audio = recog.record(filesource, duration=5)
    
recog.recognize_google(audio)




# Capture multiple portions of speech one after another
with speech as filesource:
    audio_1 = recog.record(filesource, duration=5)
    audio_2 = recog.record(filesource, duration=5)

recog.recognize_google(audio_1)




recog.recognize_google(audio_2)




# Capturing second portion of the speech using an offset argument
with speech as filesource:
    audio = recog.record(filesource, offset=5, duration=7) #offset is an arguemet that specifies the stating point & represent the number of second from the beinging of the file to ignore before starting to record

recog.recognize_google(audio)


# ### Convert Speech to Text - Effect of Noise



noisyspeech = spr.AudioFile('noisy_speech.wav')

with noisyspeech as noisesource:
    audio = recog.record(noisesource)

recog.recognize_google(audio)




with noisyspeech as noisesource:
    recog.adjust_for_ambient_noise(noisesource) #to detect spoken phrase if there is silence
    audio = recog.record(noisesource)

recog.recognize_google(audio)




recog.recognize_google(audio, show_all=True) #to show the several possible sentences


# ### Convert Speech to Text in Real Time using Microphone
#PyAudio package to detect the voice from mic


mc = spr.Microphone()




#sr.Microphone.list_microphone_names()
#if there are more than 1 mic
mc.list_microphone_names()




mc = spr.Microphone(device_index=0) #the number of the mic




with mc as source:
    audio = recog.listen(source)



recog.recognize_google(audio) #when you speak the computer capture your voice




#Reducing the effect of Noise
with mc as source:
    recog.adjust_for_ambient_noise(source)
    audio = recog.listen(source)


# ## Speech Recognition based Project



#Import Necessary Libraries
import speech_recognition as spr
import webbrowser as wb
import pafy #package to retrieve a youtube content and the related metadata like keywords
#Metadata is the data that provides data about other data but not the content  
import vlc #package to play video and audio in vlc player on computer
import urllib.request #to fetch url 
from bs4 import BeautifulSoup #beautiful soup to pull out the data of HTML & XML files
import time #to get the vlc media opened for a specific period of time

#Create an empty list to store all the video URLs from the youtube.com page
linklist = []

#Create Recognizer() class objects called recog1 and recog2
recog1 = spr.Recognizer()
recog2 = spr.Recognizer()

#Create microphone instance with device microphone chosen whose index value is 0
mc = spr.Microphone(device_index=0)

#Capture voice
with mc as source:
    print("Search Youtube video to play")
    print("----------------------------")
    print("You can speak now")
    audio = recog1.listen(source)

#Based on speech, open youtube search page in a browser, get the first video link and play it in VLC media player
if 'search' in recog1.recognize_google(audio):
    recog1 = spr.Recognizer()
    url = 'https://www.youtube.com/results?search_query='
    with mc as source:
        print('Searching for the video(s)...')
        audio = recog2.listen(source)
        
        try:
            get_keyword = recog1.recognize_google(audio)
            print(get_keyword)
            wb.get().open_new(url+get_keyword)
            response = urllib.request.urlopen(url+get_keyword)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                linklist.append('https://www.youtube.com' +vid['href'])
            videolink = pafy.new(linklist[1])
            bestlink = videolink.getbest()
            media = vlc.MediaPlayer(bestlink.url)
            media.play()
#             time.sleep(60)
#             media.stop()
        except spr.UnknownValueError:
            print("Unable to understand the input")
        except spr.RequestError as e:
            print("Unable to provide required output".format(e))




media.stop()



