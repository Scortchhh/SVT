import sounddevice as sd
import os
import speech_recognition as sr

sd.default.dtype = 'int32', 'int32'
from scipy.io.wavfile import write
from pathlib import Path
from googletrans import Translator

dir_path = os.path.dirname(os.path.realpath(__file__))
all_audio_files = []

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}


def find_files(root, extensions):
    for ext in extensions:
        yield from Path(root).glob(f'**/*.{ext}')


for file in find_files(dir_path, ['wav']):
    all_audio_files.append(file)

supported_lang = ''
for lang in LANGUAGES.keys():
    supported_lang = supported_lang + lang + ", "


def convert_speech_to_text(name_file):
    audio_file = sr.AudioFile(name_file)
    recognizer = sr.Recognizer()
    with audio_file as source:
        audio = recognizer.record(source)
    speech_lang = input('In which language is the audio file? \n available options: ' + supported_lang + '\n')
    language = speech_lang + '-' + speech_lang.upper()
    text = recognizer.recognize_google(audio, language=language)
    if text != "":
        print(text)
        translate_choice = input('Do you want to translate the text to a different language (Y/N)')
        if translate_choice == "Y" or translate_choice == "y":
            lang_choice = input('Chose your language to translate to:'
                                ' \n available options: ' + supported_lang + '\n')
            translator = Translator()
            converted_lang = translator.translate(text, dest=lang_choice)
            print('Original text: \n' + text)
            print('Translated text from language(' + LANGUAGES.get(lang_choice) + ')\n' + converted_lang.text)


def record_audio():
    choice_recording = input('do you want to start recording ? (Y/N)')
    if choice_recording == "Y" or choice_recording == "y":
        fs = 44100  # Sample rate
        duration = int(input('how long do you want to record?(in seconds)'))
        seconds = duration  # Duration of recording
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        name_file = input('how do you want to name your audio fragment') + '.wav'
        write(name_file, fs, my_recording)  # Save as WAV file
        convert_speech_to_text(name_file)


if len(all_audio_files) > 0:
    choice = input('do you want to use a existing wav file (Y/N)')
    if choice == "Y" or choice == "y":
        for file in all_audio_files:
            print(file)
        file_to_convert = input('type file name')
        if file_to_convert.find(".") == -1:
            file_to_convert = file_to_convert + '.wav'
        convert_speech_to_text(file_to_convert)
    else:
        record_audio()
else:
    record_audio()
