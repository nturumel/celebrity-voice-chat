import config, json
import os, shutil
from elevenlabs.api import Voice

# import and configure OpenAI
import openai

from talk import clone_voice, talk
openai.api_key = config.OPENAI_API_KEY

# import and configure asyncio and Interactive Brokers ib_insync package
import asyncio
import nest_asyncio
nest_asyncio.apply()


last_occurrence_start = -1
last_occurrence_end = -1

async def check_transcript():
    global last_occurrence_start
    global last_occurrence_end

    with open(config.TRANSCRIPT_FILE) as f:
        text = f.read()
        occurrence_start = text.lower().rfind(config.COMMAND_START_WORD)
        occurrence_end = text.lower().rfind(config.COMMAND_STOP_WORD)

        if occurrence_start != last_occurrence_start:
            print(f"Found new {config.COMMAND_START_WORD} between {occurrence_start} and {occurrence_end}")


            # get command starting at occurrence of command word
            command = text[occurrence_start:occurrence_end]
            print(command)

            # store last occurrence so we don't repeat the same command
            last_occurrence_start = occurrence_start
            last_occurrence_end = occurrence_end

            prompt = f"""
            {config.PROMPT_INSTRUCTIONS_CELEBRITY}
            {command}
            
{config.PROMPT_OUTPUT_FORMAT}
            """

            print(prompt)

            engine = 'text-davinci-003'

            response = openai.Completion.create(
                engine=engine, 
                prompt=prompt,
                temperature=0.3,
                max_tokens=140,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=1
            )

            try:
                print(response['choices'][0]['text'].strip())
                response_dict = json.loads(response['choices'][0]['text'].strip())
                talk(response_dict['text'])
            except Exception as e:
                print(f"error parsing response from OpenAI {e}")
                return

            

async def run_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(asyncio.sleep(interval), periodic_function())

folder = config.RECORDING_FOLDER
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

open(config.TRANSCRIPT_FILE, 'w').close()

# voice = clone_voice()
asyncio.run(run_periodically(0.5, check_transcript))

# ib.run()
