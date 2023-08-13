from elevenlabs import clone, generate, play, set_api_key, stream, voices
from elevenlabs.api import History, Voice
import config


def clone_voice():
    voice = clone(
        name="Steve",
        description="An old American male voice with a slight hoarseness in his throat. Perfect for news.",
        files=["./sample.mp3"],
    )
    return voice


def talk(text: str):
    audio = generate(text=text, voice='steve2', stream=False)
    play(audio)

set_api_key(config.ELEVEN_LABS_API_KEY)
# voice_list=voices()
# print([voice.name for voice in voice_list])
talk("Hi, I am steve jobs")