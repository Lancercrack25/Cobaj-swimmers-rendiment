import speech_recognition as sr
import pyttsx3

# Configuración del reconocimiento de voz
r = sr.Recognizer()
# Configuración de la voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Voz en español 0, 1 para ingles,

#funcion para que funcione el asistente
def funciona():
    with sr.Microphone() as source:
        audio = r.listen(source)
        texto = r.recognize_google(audio, language='es')
    try:
        texto = r.recognize_google(audio, language='es')
        return texto.lower()  # Convertimos todo a minúscula
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""

#Funcion para que nuestro asistente hable
def talk(texto):    
    engine.say(texto)
    engine.runAndWait()