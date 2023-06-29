"""
playback.py
Plays back the eye tracker's data
@author Gwen Bradforth, Terry Tao, Leslie Moreno
@version 2023-6-28
"""
import csv
import numpy as np
import cv2
import keyboard
import ctypes
import os
import pygame

def main():
  # Read filename from user
  filename = input('Enter your file name/path: ')
  if not os.path.isfile(filename):
     print("Error: Invalid path!")
     exit(1)

  # Open the CSV file for reading
  with open(filename, 'r') as file:

      # Load the CSV data into a Python object
      reader = csv.reader(file)

      # Access the data as a Python list
      rows = [row for row in reader]
      del rows[0]

  # Initialize Pygame
  pygame.init()

  # Create a black image of size of the screen
  user = ctypes.windll.user32
  screen_width = user.GetSystemMetrics(0)
  screen_height = user.GetSystemMetrics(1)
  screen = pygame.display.set_mode(
      (screen_width, screen_height), pygame.FULLSCREEN)

  cv2.namedWindow("image",cv2.WINDOW_NORMAL)
  cv2.setWindowProperty("image",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)



  # RGB color of the dot
  dot_color = (255, 0, 0)  # Red

  # Radius of the dot
  dot_radius = 10

  # Draw a red dot in the center
  dot_position = (screen_width // 2, screen_height // 2)
  with open('screen_dimensions_playback.txt', 'w') as f:
      f.write(
          f"Screen Width: {screen_width}, Screen Height: {screen_height}, Dot Position X: {dot_position[0]}, Dot Position Y: {dot_position[1]}")
  pygame.draw.circle(screen, dot_color, dot_position, dot_radius)
  pygame.image.save(screen, "red_dot.png")

  img = cv2.imread('./red_dot.png')
  
  flag = 0
  print("pog")
  # Main loop
  for i in range(1, len(rows)-1):
    # Exit if esc pressed
    if (keyboard.is_pressed('Esc')):
        break

    #If empty row, then switch to Cookie
 
        
    if (rows[i][2] and rows[i][3] != ''):
        # Draw a circle where the gaze was
        screen_x = round(float(rows[i][2])*screen_width)
        screen_y = round(float(rows[i][3])*screen_height)
        cv2.circle(img, (screen_x, screen_y), 20, (255, 0, 0), 2)
    else:
        flag = 1
        print("blank row ")
        # Display image
        img = cv2.imread('./cookie.png')
        image_width = 1302
        image_height = 939
        img = cv2.resize(img, (screen_width, screen_height))

    # Show the resulting image
    cv2.imshow('image',img)
    if(rows[i][1] != '' and rows[i-1][1] != ''):
        wait_time = int( (float(rows[i][1]) - float(rows[i-1][1]) ) * 1000)
    else:
        continue

    #Wait for a time (if time is 0, change to 1ms to prevent freezing)
    if wait_time == 0:
        cv2.waitKey(1)
    else:
        cv2.waitKey(wait_time)

    if flag == 1:
        img = cv2.imread('./cookie.png')
    else:
        img = cv2.imread('./red_dot.png')

  cv2.destroyAllWindows()

if __name__=="__main__":
    main()    