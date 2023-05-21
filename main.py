from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, AudioMessage, AudioSendMessage

from src.audio import audio
from src.models import OpenAIModel
from src.speech import Speech
from src.storage import Storage, FileStorage

import datetime
import math
import os
import uuid
load_dotenv()


app = Flask(__name__, static_url_path='/audio', static_folder='files/')

model = OpenAIModel(os.getenv('OPENAI_API_KEY'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

speech = Speech()
storage = None
memory = None
CHAT_MODEL = os.getenv('CHAT_COMPLETION_MODEL', 'gpt-3.5-turbo')
AUDIO_MODEL = os.getenv('AUDIO_MODEL_ENGINE', 'whisper-1')
SERVER_URL = os.getenv('SERVER_URL', None)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    user_id = event.source.user_id
    audio_content = line_bot_api.get_message_content(event.message.id)
    input_audio_path = f'{str(uuid.uuid4())}.m4a'
    with open(input_audio_path, 'wb') as fd:
        for chunk in audio_content.iter_content():
            fd.write(chunk)
    text = model.audio_transcriptions(input_audio_path, AUDIO_MODEL)
    history = storage.get(user_id)
    if len(history) % 10 == 0:
        messages = [{
            'role': 'system',
            'content': "You are now an experienced English teacher who knows how to guide students, summarize their learning, and set goals for them."
        }, {
            'role': 'user',
            'content': f"""
            Regarding the previous 10 conversations with the student: {history[-10:]}

            Please reflect on the following:
            1. At which stage and level are the students' questions regarding learning English?
            2. Are the answers given by the teacher really helpful to the student?
            3. If you were the teacher, how would you modify your responses to better assist the student?

            """
        }]
        _, content = model.chat_completion(messages, CHAT_MODEL)
        memory.save({
            'user_id': user_id,
            'reflect': content,
            'created_at': datetime.datetime.now()
        })

    memory_prompt = ''
    memories = memory.get(user_id)[-5:]
    if len(memories) > 0:
        memory_prompt = f'This is a record of what you have done for the student in the past: {memories}'
    messages = [{
        'role': 'system',
        'content': "You are an English teacher currently living in the United States. You know how to correct students' grammatical mistakes and guide them to improve their English proficiency."
    }, {
        'role': 'user',
        'content': f"""
        {memory_prompt}

        And now, the student's question here: '''{text}''' \n\n please answer to him with specific and actionable advice. Please reply to him in English directly, without the need for formalities or repeating his question. at most 200 words'
        """
    }]

    _, content = model.chat_completion(messages, CHAT_MODEL)
    storage.save({
        'user_id': user_id,
        'log': f'student\'s question: {text}, teacher\'s answer: {content}',
        'created_at': datetime.datetime.now()
    })

    output_audio_path = f'{str(uuid.uuid4())}.mp3'
    speech.text_to_speech(content, 'en-US-Studio-O', 'en-US', output_audio_path)
    audio_name = f'{str(uuid.uuid4())}.m4a'
    response_audio_path = f'files/{audio_name}'
    audio.convert_to_aac(output_audio_path, response_audio_path)
    duration = audio.get_audio_duration(output_audio_path)
    audio_url = f'{SERVER_URL}/audio/{audio_name}'

    if input_audio_path in os.listdir('./'):
        os.remove(input_audio_path)
    if output_audio_path in os.listdir('./'):
        os.remove(output_audio_path)

    line_bot_api.reply_message(
        event.reply_token,
        [
            AudioSendMessage(original_content_url=audio_url, duration=math.ceil(duration*1000)),
            TextSendMessage(text=f'{content}')
        ]
    )


@app.route("/", methods=['GET'])
def home():
    return 'Hello World!'


if __name__ == '__main__':
    storage = Storage(FileStorage('tinydb/file.db'))
    memory = Storage(FileStorage('tinydb/reflect.db'))
    app.run(host='0.0.0.0', port=8080)
