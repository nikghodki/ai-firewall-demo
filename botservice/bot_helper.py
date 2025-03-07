import logging
import openai
import os, json
from gtts import gTTS
import tempfile
from io import BytesIO
import base64

rules_file_path = './rules.json'


def get_rules():
    rules_list = {}
    if os.path.exists(rules_file_path):
        with open(rules_file_path, 'r') as file:
            rules = json.loads(file.read())
            c=0
            for rule in rules:
                rules_list[c] = rule
                c +=1
    return rules_list

def get_new_rule_config():
    rules = ''
    if os.path.exists(new_rule_config_file):
        with open(new_rule_config_file, 'r') as file:
            new_rule = json.loads(file.read())
    return new_rule

def set_new_rule_config(new_rule):
    try:
        with open(new_rule_config_file, 'r') as file:
            file.write(new_rule)
    except Exception as exp:
        logging.exception(f"Error when trying to write to the new rule json file: {exp}")
        return False
    return True

def verify_reply(reply):
    if reply:
        try:
            json_reply = json.loads(reply)
        except ValueError as err:
            return False
    return json_reply

welcome_message = "Hello, Welcome to Firewall Management Center for Pfsense. I am your Firewall management assistant. How can I help you?"

#
def text_to_speech(text):
    tts = gTTS(text)
    speech_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(speech_file.name)
    return speech_file.name

def text_to_speech_2(text):
    tts = gTTS(text)
    tts.save('hello_world.mp3')

    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    audio = base64.b64encode(audio_bytes.read()).decode("utf-8")
    audio_player = f'<audio src="data:audio/mpeg;base64,{audio}" controls autoplay></audio>'

    return audio_player

def get_completion_from_messages(messages, model="gpt-4", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def curtail_memory(message):
    first = message[:2]
    last_three = message[-3:]
    message = []
    message = first + last_three
    return message
