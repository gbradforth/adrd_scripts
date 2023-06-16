import csv
import numpy as np
import cv2
import keyboard
import sys
import ctypes

def main():
  # Open the CSV file for reading
  with open('./data.csv', 'r') as file:

      # Load the CSV data into a Python object
      reader = csv.reader(file)

      # Access the data as a Python list
      rows = [row for row in reader]
      del rows[0]

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
    if (keyboard.is_pressed('Esc')):
        break
    
    # Draw a circle where the gaze was
    cv2.circle(img, (int(float(rows[i][2])*image_width), int(float(rows[i][3]) * image_height) )
              , 20, (255, 0, 0), 2)
    # Show the resulting image
    cv2.imshow('image',img)

    wait_time = int( (float(rows[i][1]) - float(rows[i-1][1]) ) * 1000)
    cv2.waitKey(wait_time)
    img = cv2.imread('./cookie.png')

  cv2.destroyAllWindows()

if __name__=="__main__":
    main()    