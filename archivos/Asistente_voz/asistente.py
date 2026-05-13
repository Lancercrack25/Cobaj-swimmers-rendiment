#este es el archivo que logra darle voz al sistema para una mejor interaccion con el usuario
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
# Ajustes para mejorar estabilidad del micrófono
r.dynamic_energy_threshold = True
r.pause_threshold = 0.8

def talk(texto):
    try:
        engine = pyttsx3.init('sapi5')  # más estable en Windows

        voices = engine.getProperty('voices')

        # intenta usar voz en español si existe
        for v in voices:
            if "spanish" in v.name.lower() or "es" in v.id.lower():
                engine.setProperty('voice', v.id)
                break

        engine.setProperty('rate', 200)
        engine.setProperty('volume', 1.0)

        engine.say(texto)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Error en voz:", e)