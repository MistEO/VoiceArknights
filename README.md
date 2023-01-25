# VoiceArknights | 明日方舟，有嘴就行

基于 ASR 技术 与 《MAA 明日方舟小助手》的明日方舟半自动化控制（其实是整活项目

## 使用说明

1. 安装依赖

    ```bash
    pip install -r src/requirements.txt
    ```

2. 下载 MAA

    目前带单控的接口 MAA 还没有作为正式版本发布，所以请下载 [最新内测版](https://github.com/MaaAssistantArknights/MaaRelease/releases)，这里只有 Windows 的，mac 或者 linux 可以去 MAA 的 [主仓库 CI](https://github.com/MaaAssistantArknights/MaaAssistantArknights/actions) 里面找。或者等一段时间正式版发布  

    解压到 maa 文件夹（小写），使用下面的目录结构

    ```tree
    ├─maa
    │  ├─Python
    │  ├─resource
    │  └─xxxx.dll
    ├─src
    │  ├─vad
    │  └─......
    └─......
    ```

3. 运行

    ```bash
    python src/main.py
    ```

## 开源库

- [python-vad](https://github.com/wangshub/python-vad): 🔈 Use python to achieve voice activity detection, this little program may be helpful for voice application
- [wenet](https://github.com/wenet-e2e/wenet): Production First and Production Ready End-to-End Speech Recognition Toolkit
- [MaaAssistantArknights](https://github.com/MaaAssistantArknights/MaaAssistantArknights): 《明日方舟》小助手，全日常一键长草！| An Arknights assistant compatible with EN, JP, KR, ZH_TW clients
