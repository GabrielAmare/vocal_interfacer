import os

from gtts import gTTS
import speech_recognition as sr
from os import remove

from playsound import playsound


class VocalInterface:
    """
        This object allows to handle the sound, I/O and make text/audio conversions using APIs
    """
    listener: sr.Recognizer
    temp_file_path: str
    phrase_time_limit: float

    def __init__(self, phrase_time_limit=5, temp_file_path="speech.mp3"):
        """
        :param phrase_time_limit: max amount of time of active recording by default
        :param temp_file_path: temporary audio file when speaking by default
                             : (auto removed after each call of ``VocalInterface.speak``)
        """
        self.listener = sr.Recognizer()
        self.phrase_time_limit = phrase_time_limit
        self.temp_file_path = temp_file_path

    def record(self, phrase_time_limit: float) -> sr.AudioData:
        """
            This method allow to record user voice for a certain amount of time
        :param phrase_time_limit: max amount of time of active recording
        :return: The audio sample recorded
        """
        with sr.Microphone() as microphone:
            audio_data = self.listener.listen(microphone, phrase_time_limit=phrase_time_limit)
        return audio_data

    @staticmethod
    def play(file_path) -> bool:
        """
            This function is used to play the audio file at ``file_path``
        :param file_path: The file path of the audio file
        :return: The status of the operation (ie, the file has been played correctly -> True)
        """
        try:
            playsound(file_path)
            return True
        except UnicodeDecodeError as e:
            return False
        except Exception as e:
            return False

    def listen(self, **kw) -> str:
        """
            This method listen to the user microphone and map the audio input to a corresponding text output
            :param lang: the lang used to understand the record
            :param phrase_time_limit: max amount of time of active recording
            :return: Text extracted from the user's record
        """
        phrase_time_limit = kw.get('phrase_time_limit', self.phrase_time_limit)

        audio_data = self.record(phrase_time_limit)

        try:
            return self.listener.recognize_google(audio_data, language=kw.get('lang', 'en-US'))
        except Exception as _:
            return ""

    def speak(self, text: str, lang: str, **kw) -> bool:
        """
            This method reads the given text out loud
            :param text: The text to read
            :param lang: lang in ISO_639_1 format
            :return: status of the operation (ie, the sound have been played correcty -> True)
        """
        temp_file_path = kw.get('temp_file_path', self.temp_file_path)

        try:
            gTTS(text=text, lang=lang, slow=False).save(temp_file_path)
            self.play(temp_file_path)
            return True
        except Exception as e:
            return False
        finally:
            if os.path.exists(temp_file_path):
                remove(temp_file_path)
