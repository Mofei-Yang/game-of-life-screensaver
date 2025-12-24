# Game of life screensaver
Screensaver that runs in the terminal, works for unix, tested on macOS Tahoe 26

This displays the conway's game of life in the terminal, effectively acting as a screensaver.

# Requirements
Python 3.6 or above (probably, not tested), pip

# Usage
If you are using it for the first time, install all related packages in the source code. You can run this:
```
pip install time random shutil sys os collections pyinstaller
```
then, copy the life.py file over to a preferrably empty directory, and run 
```
pyinstaller --onefile life.py
cd dist
chmod +x life
sudo mv life /usr/local/bin
cd ..
rm -rf dist
```

You can run the command `life` after this to enjoy the screensaver.
