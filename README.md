# Local-Video-Player
**About the tool.** This tool aims to let the user share videos over his local network such that every browser of any device, after the webserver has started, can watch the videos shared. 
It is written in Python 3.12, and is Open Source under the GPL-3.0 license.

**About new releases.** The releases don't have a deadline so it can take months for a new version, but every new one will bring new features and improvements.

**About the templates.** Templates, chosen by the user in the settings of Local Video Player, customize the style and the code of the webserver.

**How to compile the tool.**
1. Download the source code of the repository (You can either download it from the last release or from the repository itself)
2. Open a terminal
3. Using `cd` go to `Local-Video-Player/` 
4. Install the libraries, required by the tool, using: `pip install -r requirements.txt`
5. If you don't already have pyinstaller install it with `pip install pyinstaller`
6. Compile the tool by executing the following command: 
```
pyinstaller --noconfirm --onedir --add-data "C:/Users/user/AppData/Local/Programs/Python/Python312/Lib/site-packages/customtkinter;customtkinter/" --add-data "./templates/;./LocalVideoPlayer/templates/" "./source/App.py"
```
where `user` has to be replaced with your own username.

7. Run the following command to rename the executable and to get the Windows Firewall settings:
```
Rename-Item "./dist/App/App.exe" "Local Video Player.exe"
```
8. Now check the `dist` folder: you will find the executable in it.

Note that the \_internal folder and the executable must be in the same directory.

**Webserver troubleshooting.** If you have started the tool but using other devices you can't access the address it means you have to modify your Windows Firewall settings and enable private network.

**External Libraries Required.**
You can find all the libraries required to compile the tool, with which version I used, in `requirements.txt`