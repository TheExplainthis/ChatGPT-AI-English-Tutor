import subprocess
import json


class Audio():
    def convert_to_aac(self, input_file, output_file):
        subprocess.run(['ffmpeg', '-i', input_file, '-c:a', 'aac', '-strict', '-2', output_file, '-y'])

    def convert_to_wav(self, input_file, output_file):
        subprocess.run(['ffmpeg', '-i', input_file, output_file])

    def get_audio_duration(self, input_file):
        out = subprocess.check_output(['ffprobe', '-v', 'quiet', '-show_format', '-print_format', 'json', input_file])
        ffprobe_data = json.loads(out)
        return float(ffprobe_data['format']['duration'])


audio = Audio()