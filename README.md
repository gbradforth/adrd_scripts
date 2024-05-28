# Eyetracker and Playback

Eyetracker and Playback are Python files for recording eye tracker data and playing it back. 

## Installation
Eyetracker has several dependencies. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.
```bash
pip install -r requirements.txt
```
Make sure to run this code with python 3.10. `tobii-research` doesn't have compatibility with 3.11. You can do this using a `conda` environment if needed.    
 In order to run this program, you will need a Tobii Pro device connected to your computer.
## Usage
In the same folder as the python files, place the image you wish to display. Currently, the image is called `cookie.png` in the code.  Either change the file name or alter the code.
Run the eye tracker in your terminal environment.
```
python eyetracker.py
```
This will display the chosen image for 2 minutes and collect data from the eye tracker. The program can be exited at any time with the `esc` key. The time and coordinate data from the eye tracker will be recorded in `data.csv`, in the same folder as the python files.  
  
Run the playback in your terminal environment.
```
python playback.py
```
This will display the same photo, with circles overlayed playing in real time to replicate the eye tracker's data. This can be exited at any time with `esc`. 
## Troubleshooting
This portion will discuss common issues.  
```
no module named [package]
```
Make sure to install all dependencies.

```
No eye tracker found!
```
This happens sometimes, run the program again. If this occurs repetitively, make sure you have your eye tracker plugged in appropriately.


version: June 2023