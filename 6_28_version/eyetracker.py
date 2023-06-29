import pygame
import time
import tobii_research as tr
import numpy as np
import csv
import sys
import keyboard

# Track time
t_start = time.time()
t_end = t_start + 120  # change to length in seconds you want

# Write to data
fileName = r"./" + time.strftime("%m-%d_%H.%M.%S") + ".csv"
file = open(fileName, 'w', newline='')
writer = csv.writer(file)
writer.writerow(["Time", "Timestamp", "X", "Y"])


def gaze_data_callback(gaze_data):
    # Get gaze coordinates
    gaze_left_eye = np.array(gaze_data['left_gaze_point_on_display_area'])
    gaze_right_eye = np.array(gaze_data['right_gaze_point_on_display_area'])

    # Center gaze
    if np.isnan(gaze_left_eye).any() and np.isnan(gaze_right_eye).any():
        center = np.array(center)
    elif np.isnan(gaze_left_eye).any():
        center = gaze_right_eye
    elif np.isnan(gaze_right_eye).any():
        center = gaze_left_eye
    else:
        center = (gaze_left_eye+gaze_right_eye) / 2

    # save to file
    timestamp = time.time() - t_start
    current_time = time.strftime("%H:%M:%S")
    # current time, time elapsed, x, y
    writer.writerow([current_time, timestamp, center[0], center[1]])


def main():
    # Initialize Pygame
    pygame.init()

    # Find eye tracker
    found_eyetrackers = tr.find_all_eyetrackers()
    if len(found_eyetrackers) == 0:
        print("No eye trackers found")
        sys.exit(1)
    my_eyetracker = found_eyetrackers[0]

    # Set the display mode to full screen
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode(
        (screen_width, screen_height), pygame.FULLSCREEN)

    # RGB color of the dot
    dot_color = (255, 0, 0)  # Red

    # Radius of the dot
    dot_radius = 10

    # Draw a red dot in the center
    dot_position = (screen_width // 2, screen_height // 2)
    with open('screen_dimensions.txt', 'w') as f:
        f.write(
            f"Screen Width: {screen_width}, Screen Height: {screen_height}, Dot Position X: {dot_position[0]}, Dot Position Y: {dot_position[1]}")
    pygame.draw.circle(screen, dot_color, dot_position, dot_radius)

    # Update the display
    pygame.display.flip()

    # Subscribe to gaze data
    my_eyetracker.subscribe_to(
        tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    # Keep the red dot for 5 seconds
    time.sleep(10)
    writer.writerow(["", "", "", ""])

     # Load the image
    image_path = "./cookie.png"
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screen_width, screen_height))

    # Draw the image on the screen
    screen.blit(image, (0, 0))
    pygame.display.update()


    

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


if __name__ == "__main__":
    main()
