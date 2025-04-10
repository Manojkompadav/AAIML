import speech_recognition as sr
from googletrans import Translator

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize translator
translator = Translator()

def recognize_speech():
    with sr.Microphone() as source:
        print("🎤 Please speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("❌ Sorry, the service is down.")
        return None

def translate_text(text, target_language='es'):
    translated = translator.translate(text, dest=target_language)
    print(f"🌍 Translated Text ({target_language}): {translated.text}")
    return translated.text

def speech_to_text_and_translate():
    # Prompt user to select a language
    print("\n🌐 Enter the target language code (e.g., 'fr' for French, 'de' for German, 'hi' for Hindi, 'ja' for Japanese):")
    target_language = input("Target language code: ").strip().lower()

    recognized_text = recognize_speech()
    if recognized_text:
        translated_text = translate_text(recognized_text, target_language)
        return translated_text

# Run the program
if __name__ == "__main__":
    final_output = speech_to_text_and_translate()
    if final_output:
        print(f"\n✅ Final Translated Output: {final_output}")
