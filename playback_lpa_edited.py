"""
playback.py
Plays back the eye tracker's data
THIS IS THE VERSION THAT WORKS
@leticia, Cecily
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
    screen_width, screen_height = 2560, 1600  # Set your screen dimensions
    window = 'Cookie Theft EyeTracking'

    # Display image
    img = cv2.imread('cookie.png')
    img = cv2.resize(img, (screen_width, screen_height))

    # Create a black image to clear the screen
    black_img = np.zeros((screen_height, screen_width, 3), dtype = np.uint8)

    # Prompt the user if the participant was shown a red dot
    dot_q = input('Red Dot? y/n: ')
    has_dot = True
    if dot_q == 'n':
        has_dot = False

    # If they have a dot, draw the dot
    if has_dot:
        dot_color = (0, 0, 255)  # Red
      
        # Draw a red dot in the center
        dot_position = (screen_width // 2, screen_height // 2)
        cv2.circle(black_img, dot_position, 40, dot_color, -1)


    # Gets ten seconds ahead, used if the csv file does not have a blank row
    start_time = rows[0][1]
    ten_secs = float(start_time) + 10

    dot_showing = has_dot

    # Used for manually calculating offsets
    diffX = 0
    diffY = 0

    # Main loop
    for i in range(1, len(rows) - 1):
        # Exit if 'Esc' is pressed
        if cv2.waitKey(1) == 27:  # 27 is the ASCII code for 'Esc'
            break

        # Draw a circle where the gaze was
        if 'nan' == rows[i][2]:
           rows[i][2] = 0.0
        if 'nan' == rows[i][3]:
           rows[i][3] = 0.0

        # If there was a dot, then verify the dot should still be showing
        # i.e. The iterator hasn't hit the blank row or been more than 10 seconds
        if dot_showing:

            # If you hit a blank row in the file, the dot has disappeared
            # Some files did not have blank rows, so the image will switch after 10 seconds max
            if rows[i][0] == '' or float(rows[i][1]) > ten_secs:
                dot_showing = False
                
                # Print statement to find the blank row automatically
                if rows[i][0] == '':
                    print ("blank row @ row " + str(i))
                continue

        screen_x = round((float(rows[i][2]) - diffX) * screen_width)
        screen_y = round((float(rows[i][3]) - diffY) * screen_height)

        # If the dot is still showing, then load the blue circle onto the dot
        if dot_showing:
            cv2.circle(black_img, (screen_x, screen_y), 40, (255, 0, 0), 6)
            cv2.imshow(window, black_img)
        # Otherwise draw it on the cartoon image
        else:
            cv2.circle(img, (screen_x, screen_y), 40, (255, 0, 0), 6)
            cv2.imshow(window, img)

        # If the row before is blank, skip ahead (otherwise other parts of the code fail)
        if '' == rows[i-1][0]:
            continue

        wait_time = int((float(rows[i][1]) - float(rows[i - 1][1])) * 1000)

        # If time is 0, change to 1ms to prevent freezing
        if not wait_time:
            wait_time = 1
       
        cv2.waitKey(wait_time)

        # Clear the screen, replacing it with the correct image (either the dot or the cartoon)
        if dot_showing:
            black_img = np.zeros((screen_height, screen_width, 3), dtype = np.uint8)
            cv2.circle(black_img, dot_position, 40, dot_color, -1)
        else:
            img = cv2.imread('cookie.png')
            img = cv2.resize(img, (screen_width, screen_height))

    cv2.destroyAllWindows()

main()