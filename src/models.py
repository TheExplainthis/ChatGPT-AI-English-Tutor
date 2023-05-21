import openai


class OpenAIModel:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def chat_completion(self, messages, model_engine) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=model_engine,
                messages=messages
            )
            role = response['choices'][0]['message']['role']
            content = response['choices'][0]['message']['content'].strip()
            return role, content
        except Exception as e:
            raise e

    def audio_transcriptions(self, file_path, model_engine) -> str:
        with open(file_path, 'rb') as f:
            audio_file = f.read()
            response = openai.Audio.transcribe(model_engine, audio_file)
        return response['text']
        