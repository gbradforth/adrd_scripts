"""
eyetracker.py
Tracks eye movement to an image and saves the data
@author Gwen Bradforth, Leticia Pinto-Alva
@version 2023-6-16
"""
import pygame
import time
import tobii_research as tr
import numpy as np
import csv
import sys
import keyboard

# Track time
t_start = time.time()
t_end = t_start + 120 # change to length in seconds you want

# Write to data
fileName = r"./" + time.strftime("%m-%d_%H.%M.%S") +".csv"
file = open(fileName,'w',newline='')
writer = csv.writer(file)
writer.writerow(["Time","Timestamp","X","Y"])

# Callback function for gaze data
def gaze_data_callback(gaze_data):
    # Get gaze coordinates
    gaze_left_eye = np.array(gaze_data['left_gaze_point_on_display_area'])
    gaze_right_eye = np.array(gaze_data['right_gaze_point_on_display_area'])

    # Center gaze
    if np.isnan(gaze_left_eye).any() and np.isnan(gaze_right_eye).any():
        center = [float("NaN"),float("NaN")]
    elif np.isnan(gaze_left_eye).any():
        center=gaze_right_eye 
    elif np.isnan(gaze_right_eye).any():
        center = gaze_left_eye
    else:
        center = (gaze_left_eye+gaze_right_eye) / 2 

    #save to file
    timestamp = time.time() - t_start
    #timestamp = f"{(time_passed / 3600):02d}:{((time_passed % 3600)/60):02d}:{time_passed % 60:02d}" #this line breaks everything for some reason
    current_time = time.strftime("%H:%M:%S")
    writer.writerow([current_time,timestamp,center[0],center[1]]) #current time, time elapsed, x, y
    
   
    # Draw the image on the screen
    #screen.blit(image, (0, 0))
    #pygame.draw.circle(screen, (255, 0, 0), (screen_x*screen_width, screen_y*screen_height), 20,width=2)  # Display gaze point as a red circle
    #pygame.display.update()


def main():
    # Initialize Pygame
    pygame.init()

    # Find eye tracker
    found_eyetrackers = tr.find_all_eyetrackers()
    if len(found_eyetrackers) == 0:
        print("No eye trackers found")
        exit(1)
    my_eyetracker = found_eyetrackers[0]

    # Set the display mode to full screen
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    # Load the image
    image_path = "./cookie.png"
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screen_width, screen_height))

    # Draw the image on the screen
    screen.blit(image, (0, 0))
    pygame.display.update()

    # Subscribe to gaze data
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    # Main loop
    while time.time() < t_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        if keyboard.is_pressed('Esc'):
            break

    # Unsubscribe from gaze data
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

    # Clean up
    file.close()
    pygame.quit()

if __name__=="__main__":
    main()