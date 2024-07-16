# Local-Video-Player
**About the tool.** This tool aims to let the user share videos over his local network such that every browser of any device, after the webserver has started, can watch the videos shared. 
It is written in Python 3.12 (which is required), and is Open Source under the GPL-3.0 license.

**About new releases.** The development of this tool has just started and a lot of new features will come in next versions.

**How to compile the tool.**
1. Download the source code of the repository (You can either download it from the last release or from the repository itself)
2. Open a terminal
3. Using `cd` go to `Local-Video-Player/source/` 
4. Write and execute the following command: 
```
pyinstaller --noconfirm --onedir --add-data "C:/Users/user/AppData/Local/Programs/Python/Python312/Lib/site-packages/customtkinter;customtkinter/" --add-data "./lvp_templates/;./lvp_templates/" "App.py"
```
where you have to install `pyinstaller` with `pip install pyinstaller` if you don't already have it, and `user` has to be replaced with your own username.

5. Now check the `dist` folder: you will find the .exe in it.

Note that _internal and the executable must be in the same directory.

**External Libraries Required.**
You can find the all the libraries required to compile the tool, with which version I used, in `requirements.txt`