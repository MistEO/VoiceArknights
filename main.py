
from paddlespeech.cli.asr.infer import ASRExecutor
from maa.Python import asst

from src.vad import pyvad
from src.gamedata.operators import all_opers

import signal
import pathlib
import re
import cn2an

leave = False

def handle_int(sig, chunk):
    global leave
    leave = True

signal.signal(signal.SIGINT, handle_int)

asr = ASRExecutor()

maa = None


def init_maa():
    global maa

    assert asst.Asst.load(pathlib.Path.cwd() / "maa"), "MAA 资源读取错误"

    maa = asst.Asst()

    # 改成你自己的 adb 路径和地址
    assert maa.connect('adb.exe', '127.0.0.1:5555'), "ADB 连接失败"


def start_step(action):
    params = {
        "type": "copilot",
        "subtype": "action",
        "details": {
            "actions": [
                action
            ]
        }
    }
    print(params)

    maa.append_task("SingleStep", params)
    if not maa.running():
        maa.start()


type_dict = {
    "部署": "部署",
    "放到": "部署",
    "撤退": "撤退",
    "技能": "技能",
    "倍速": "二倍速",
}

direction_dict = {
    "上": "上",
    "下": "下",
    "左": "左",
    "右": "右",
}

location_re = "第(.+)[行排]第(.+)列"

def parse_action(text):
    action = {}

    for key, value in type_dict.items():
        if key in text:
            action["type"] = value
            break
    
    for key, value in direction_dict.items():
        if key in text:
            action["direction"] = value
            break

    for name in all_opers:
        if name in text:
            action["name"] = name
            break

    loc_match = re.search(location_re, text)
    if loc_match:
        x_cn = loc_match.group(1)
        y_cn = loc_match.group(2)
        try:
            x = cn2an.cn2an(x_cn)
            y = cn2an.cn2an(y_cn)
            action["location"] = [x, y]
        except ValueError:
            print("位置识别错误")
            pass

    return action

if __name__ == "__main__":

    init_maa()

    while not leave:
        pyvad.run()
        result = asr(audio_file=pyvad.WAV_PATH)
        print(result)
        action = parse_action(result)
        if action:
            start_step(action)
