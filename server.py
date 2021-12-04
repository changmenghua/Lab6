import speech_recognition
from bluedot.btcomm import BluetoothServer
import tempfile
from gtts import gTTS
from pygame import mixer
import time

def get_message():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
      r.adjust_for_ambient_noise(source, duration=1)
      print("Say 'Activate/Deactivate white/yellow socket' or 'Retrieve information':")
      audio = r.listen(source)
    try:
      return r.recognize_google(audio, language="en-US")
    except speech_recognition.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
      print("No response from Google Speech Recognition serve: {0}".format(e))

def play(sentence, lang, loops_count):
  with tempfile.NamedTemporaryFile(delete=True) as file:
    tts = gTTS(text=sentence, lang=lang)
    tts.save('{}.mp3'.format(file.name))
    mixer.init()
    mixer.music.load('{}.mp3'.format(file.name))
    mixer.music.play(loops_count)

def receive_client_message(client_msg):
  print("Received from client:")
  print(client_msg)
  try:
    play(client_msg, 'en', 1)
    if len(client_msg) > 50:
      time.sleep(25)
    else:
      time.sleep(2)
    msg = get_message()
    print("Google Speech Recognition thinks you said:")
    print(msg)
    s.send(msg)
  except Exception as e:
    print(e)

s = BluetoothServer(receive_client_message)
while True: # for bluetooth server to listen
  pass
