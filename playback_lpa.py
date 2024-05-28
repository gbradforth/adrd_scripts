"""
playback.py
Plays back the eye tracker's data
@leticia, gwen
"""
import csv
import cv2
import os
import time
import numpy as np

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

    # Get screen dimensions
    screen_width, screen_height = 3072, 1920 #1280, 800  # Set your screen dimensions

    # Display image
    img = cv2.imread('cookie.png')
    img = cv2.resize(img, (screen_width, screen_height))

    # Create a black image to clear the screen
    black_img = np.zeros((screen_height, screen_width, 3), dtype = np.uint8)

    # Main loop
    for i in range(1, len(rows) - 1):
        # Exit if 'Esc' is pressed
        if cv2.waitKey(1) == 27:  # 27 is the ASCII code for 'Esc'
            break

        # Draw a circle where the gaze was
        screen_x = round(float(rows[i][2]) * screen_width)
        screen_y = round(float(rows[i][3]) * screen_height)
        cv2.circle(img, (screen_x, screen_y), 30, (255, 0, 0), 2)

        # Show the resulting image
        cv2.imshow('image', img)
        wait_time = int((float(rows[i][1]) - float(rows[i - 1][1])) * 1000)

        # Wait for a time (if time is 0, change to 1ms to prevent freezing)
        if wait_time:
            cv2.waitKey(1)
        else:
            cv2.waitKey(1)
        
        # Clear the screen
        img = cv2.imread('cookie.png')
        img = cv2.resize(img, (screen_width, screen_height))
        cv2.waitKey(1)

    cv2.destroyAllWindows()

main()
