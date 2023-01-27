
from paddlespeech.cli.asr.infer import ASRExecutor
from maa.Python import asst

from src.vad import pyvad
from src.nlp import parser

import signal
import pathlib


asr = ASRExecutor()

maa = None


def init_maa():
    global maa

    assert asst.Asst.load(pathlib.Path.cwd() / "maa"), "MAA 资源读取错误"

    maa = asst.Asst()

    # 改成你自己的 adb 路径和地址
    assert maa.connect("adb.exe", "127.0.0.1:5555"), "ADB 连接失败"


def start_step(params):
    maa.append_task("SingleStep", params)
    if not maa.running():
        maa.start()


leave = False

def handle_int(sig, chunk):
    global leave
    leave = True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_int)
    
    init_maa()

    stage_name = input("请输入关卡名：")
    start_step(params = {
            "type": "copilot",
            "subtype": "stage",
            "details": {
                "stage_name": stage_name,
            },
        })

    while not leave:
        pyvad.run()
        result = asr(audio_file=pyvad.WAV_PATH)
        print(result)
        action = parser.parse_text(result)
        if action:
            start_step(action)
