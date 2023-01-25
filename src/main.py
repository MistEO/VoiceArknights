from vad import pyvad
from operators import all_opers
import wenetruntime as wenet
import signal

leave = False

def handle_int(sig, chunk):
    global leave
    leave = True

signal.signal(signal.SIGINT, handle_int)


context = all_opers
context += ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "杠"]
context += ["部署", "放到", "撤退", "技能", "二倍速", "一倍速", "挂机"]

asr = wenet.Decoder(lang='chs', context=context, context_score=10.0)


while not leave:
    pyvad.run()
    result = asr.decode_wav(pyvad.WAV_PATH)
    print(result)
    asr.reset()
