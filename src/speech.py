import os
from google.cloud import texttospeech
from google.oauth2.service_account import Credentials


class Speech():
    def __init__(self):
        credentials = Credentials.from_service_account_info({
          'type': os.getenv('type'),
          'project_id': os.getenv('project_id'),
          'private_key_id': os.getenv('private_key_id'),
          'private_key': os.getenv('private_key'),
          'client_email': os.getenv('client_email'),
          'client_id': os.getenv('client_id'),
          'auth_uri': os.getenv('auth_uri'),
          'token_uri': os.getenv('token_uri'),
          'auth_provider_x509_cert_url': os.getenv('auth_provider_x509_cert_url'),
          'client_x509_cert_url': os.getenv('client_x509_cert_url'),
        })
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)

    def text_to_speech(self, text, voice_name, translate_language, audio_path):
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            name=voice_name,
            language_code=translate_language
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open(audio_path, 'wb') as out:
            out.write(response.audio_content)