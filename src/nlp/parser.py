from src.gamedata.operators import all_opers_piyin, to_pinyin

import re
import cn2an


start_keys = ["开始", "行动"]

def parse_text(text):
    is_start = False
    for key in start_keys:
        if key in text:
            is_start = True

    params = {}

    if is_start:
        
        params = {
            "type": "copilot",
            "subtype": "start",
        }
    else:
        actions = parse_actions(text)
        if not actions:
            return None
        
        params = {
            "type": "copilot",
            "subtype": "action",
            "details": {
                "actions": actions,
            },
        }

    print(params)
    return params


type_dict = {
    "部署": "部署",
    "放到": "部署",
    "撤退": "撤退",
    "技能": "技能",
    "倍速": "二倍速",
    "倍数": "二倍速",
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

# 行和列，反过来的
location_re = "第([零一二三四五六七八九十]+).第([零一二三四五六七八九十]+)."

location_cache = {}

def parse_actions(text):
    # sample: 
    # 部署桃金娘到第七排第五列朝左
    # 把风笛放到桃金娘左边朝右
    # 桃金娘开技能
    # 撤退桃金娘
    # 二倍速

    action = {}

    ### type
    invalid = True
    for key, value in type_dict.items():
        if key in text:
            action["type"] = value
            invalid = False
            break
    
    if invalid:
        return None

    ### direction
    for key, value in direction_dict.items():
        if key in text:
            action["direction"] = value
            break

    ### name
    name_list = []
    text_pinyin = to_pinyin(text)
    for name, pinyin in all_opers_piyin.items():
        if " " + pinyin + " " in text_pinyin:
            text_pinyin = text_pinyin.replace(pinyin, "")
            name_list.append((name, pinyin))

    text_pinyin = to_pinyin(text)

    def name_order(pair):
        return text_pinyin.index(pair[1])

    name_list.sort(key=name_order)
    print(name_list)
    
    name_list = [name for name, _ in name_list]
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

    elif len(name_list) == 1 and name_list[0] in location_cache:
        loc = location_cache[name_list[0]]
        x = loc[0]
        y = loc[1]

    elif len(name_list) == 2 and name_list[1] in location_cache:
        for key, value in relative_location.items():
            if key in text:
                base = location_cache[name_list[1]]
                x = base[0] + value[0]
                y = base[1] + value[1]
                break

    if x != 0 and y != 0:
        action["location"] = [x, y]
        if name_list:
            location_cache[name_list[0]] = [x, y]

    ### Generate maa copilot json
    actions_list = [action]

    print(actions_list)
    return actions_list
