"""
playback_frames.py
Saves the eye tracker's data as frames
@author Gwen Bradforth
@version 2023-6-16
"""
import csv
import cv2
import os

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

  # Display image
  img = cv2.imread('./cookie.png')
  image_width = 1302
  image_height = 939

  # Create the output directory if it doesn't exist
  if not os.path.exists("frames"):
      os.makedirs("frames")

  # Main loop
  for i in range(1, len(rows)-1):
    # Draw a circle where the gaze was
    screen_x = round(float(rows[i][2])*image_width)
    screen_y = round(float(rows[i][3])*image_height)
    cv2.circle(img, (screen_x, screen_y), 20, (255, 0, 0), 2)

    # Show the resulting image
    cv2.imwrite("./frames/frame%d.jpg" % i, img)
    img = cv2.imread('./cookie.png')

  cv2.destroyAllWindows()

if __name__=="__main__":
    main()    