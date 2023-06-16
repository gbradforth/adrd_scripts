"""
frames.py
Converts a video to frames
@author Gwen Bradforth
@version 2023-6-16
"""
import cv2
import os

def main():
  # Read filename from user
  filename = input('Enter your file name/path: ')
  if not os.path.isfile(filename):
     print("Error: Invalid path!")
     exit(1)
  
  vidcap = cv2.VideoCapture(filename)
  success,image = vidcap.read()

  # Create the output directory if it doesn't exist
  if not os.path.exists("frames"):
      os.makedirs("frames")

  count = 0
  while success:
    cv2.imwrite("./frames/frame%d.jpg" % count, image)  # save frame as JPEG file      
    success,image = vidcap.read()
    count += 1

if __name__=="__main__":
    main()    