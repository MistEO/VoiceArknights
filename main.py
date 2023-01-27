
from paddlespeech.cli.asr.infer import ASRExecutor
from maa.Python import asst

from src.vad import pyvad
from src.gamedata.operators import all_opers

import signal
import pathlib
import re
import cn2an


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
    "向上": "上",
    "朝上": "上",
    "向下": "下",
    "朝下": "下",
    "向左": "左",
    "朝左": "左",
    "向右": "右",
    "朝右": "右",
}

relative_location = {
    "左边": [-1, 0],
    "左侧": [-1, 0],
    "右边": [1, 0],
    "右侧": [1, 0],
    "上边": [0, -1],
    "上面": [0, -1],
    "下边": [0, 1],
    "下面": [0, 1],
    "左上": [-1, -1],
    "左下": [-1, 1],
    "右上": [1, -1],
    "右下": [1, 1],
}

location_re = "第(.+)[行排]第(.+)列"

location_cache = {}

def parse_action(text):
    # sample: 
    # 部署桃金娘到第七排第五列朝左
    # 把风笛放到桃金娘左边朝右
    # 桃金娘开技能
    # 撤退桃金娘
    # 二倍速

    action = {}

    ### type
    for key, value in type_dict.items():
        if key in text:
            action["type"] = value
            break
    
    ### direction
    for key, value in direction_dict.items():
        if key in text:
            action["direction"] = value
            break

    ### name
    name_list = []
    for name in all_opers:
        if name in text:
            name_list.append(name)

    def name_order(name):
        return text.index(name)

    name_list.sort(key=name_order)
    print(name_list)

    if name_list:
        action["name"] = name_list[0]

    ### location
    global location_cache
    x = 0
    y = 0
    loc_match = re.search(location_re, text)
    if loc_match:
        x_cn = loc_match.group(1)
        y_cn = loc_match.group(2)
        try:
            x = cn2an.cn2an(x_cn)
            y = cn2an.cn2an(y_cn)
        except ValueError:
            print("位置识别错误")
            pass

    elif len(name_list) == 2 and name_list[1] in location_cache:
        for key, value in relative_location.items():
            if key in text:
                base = location_cache[name_list[1]]
                x = base[0] + value[0]
                y = base[1] + value[1]
                break

    action["location"] = [x, y]
    if name_list:
        location_cache[name_list[0]] = [x, y]

    print(action)
    return action


leave = False

def handle_int(sig, chunk):
    global leave
    leave = True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_int)
    
    init_maa()

    while not leave:
        pyvad.run()
        result = asr(audio_file=pyvad.WAV_PATH)
        print(result)
        action = parse_action(result)
        if action:
            start_step(action)
