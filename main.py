import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
AI_DEVS_KEY = os.getenv("AIDEVS_API_KEY")

TOKEN = "https://tasks.aidevs.pl/token/whisper"
ANSWER = "https://tasks.aidevs.pl/answer"
TASK = "https://tasks.aidevs.pl/task"
TOKEN_PARAMS = {
    "apikey": AI_DEVS_KEY
}

token_response = requests.post(url=TOKEN, json=TOKEN_PARAMS)
token_response.raise_for_status()
token_data = token_response.json()
token = token_data["token"]

get_task_response = requests.get(url=f"{TASK}/{token}")
token_response.raise_for_status()
task_data = get_task_response.json()

file_link = task_data["msg"].split(': ')[-1]


audio_response = requests.get(file_link)
with open("mateusz.mp3", "wb") as f:
    f.write(audio_response.content)

client = OpenAI()
audio_file = open("mateusz.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)

audio_text = transcription.text

answer = {
    "answer": audio_text
}
send_answer = requests.post(url=f"{ANSWER}/{token}", json=answer)