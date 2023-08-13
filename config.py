OPENAI_API_KEY = ""

TRANSCRIPT_FILE = "transcriptions/transcript.txt"
RECORDING_FOLDER = "recordings"

COMMAND_START_WORD = "whisper"
COMMAND_STOP_WORD = "stop"

CELEBRITY_NAME = 'Steve Jobs'

PROMPT_INSTRUCTIONS_CELEBRITY = f"""
Imagine you are {CELEBRITY_NAME}.
Respond to the following input.

Input:
"""


ELEVEN_LABS_API_KEY=''

PROMPT_OUTPUT_FORMAT = """
Return the result in the following json format
{
    "text": ""
}
"""