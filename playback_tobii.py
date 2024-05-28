
"""
playback_tobii.py
Plays back the eye tracker's data from old tobii data (tsv)
@author Gwen Bradforth
@version 2023-6-19
"""
import csv
import cv2
import keyboard
import ctypes
import os

def main():
  # Read filename from user
  filename = input('Enter your file name/path: ')
  if not os.path.isfile(filename):
     print("Error: Invalid path!")
     exit(1)

  # Read participant number from user
  participant = input("Enter the participant's number (1,2,3...): ")
  # Check format
  if not participant.isdigit():
      print("Error: Invalid participant number.")
      exit(1)
  participant = "Participant" + participant

  # Open the file for reading
  with open(filename, 'r') as file:

      # Load the TSV data into a Python object
      reader = csv.reader(file, delimiter="\t")

      print("accessing data...")
      # Access the data as a Python list, filtering by participant, and when they're looking at the cookie
      rows = [row for row in reader if row[5] == participant and row[72] == "cookie"]
      del rows[0]
    
  # Check if the list is empty (participant does not exist)
  if not rows:
      print("Error: Participant does not exist.")
      exit(1)

  # Create a black image of size of the screen
  user = ctypes.windll.user32
  screen_width = user.GetSystemMetrics(0)
  screen_height = user.GetSystemMetrics(1)
  cv2.namedWindow("image",cv2.WINDOW_NORMAL)
  cv2.setWindowProperty("image",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

  # Display image
  img = cv2.imread('./cookie.png')
  image_width = 1302
  image_height = 939
  img = cv2.resize(img, (screen_width, screen_height))

  # Main loop
  for i in range(1, len(rows)-1):
    # Exit if esc pressed
    if (keyboard.is_pressed('Esc')):
        break
    
    # Draw a circle where the gaze was
    if rows[i][39] == "" or rows[i][40] == "":
        screen_x, screen_y = 0,0
    else:
        screen_x = int(rows[i][39])
        screen_y = int(rows[i][40])
        cv2.circle(img, (screen_x, screen_y), 20, (255, 0, 0), 2)

    # Show the resulting image
    cv2.imshow('image',img)
    wait_time = int( (float(rows[i][0]) - float(rows[i-1][0]) ) / 100)
    cv2.waitKey(wait_time)
    img = cv2.imread('./cookie.png')

  cv2.destroyAllWindows()

if __name__=="__main__":
    main()    
