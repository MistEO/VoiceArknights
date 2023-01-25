from vad import pyvad
from paddlespeech.cli.asr.infer import ASRExecutor
import signal

leave = False

def handle_int(sig, chunk):
    global leave
    leave = True

signal.signal(signal.SIGINT, handle_int)

asr = ASRExecutor()

while not leave:
    pyvad.run()
    result = asr(audio_file=pyvad.WAV_PATH)
    print(result)
