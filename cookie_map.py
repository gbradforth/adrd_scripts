"""
cookie_map.py
Takes in color coded map of cookie theft and outputs a pixel map of the categories.
No one should need this other than me. The output pixel map is stored in output_array_but_better.csv
@author Gwen Bradforth
@version 2023-11-18
"""
from PIL import Image
import numpy as np
import csv

color_mapping = {
    (255, 255, 255, 255): 0,  # White (bg)
    (255,255,190, 255): 1,  # Yellow (mother)
    (220,250,255, 255): 2,  # Light Blue (daughter)
    (255,200,255, 255): 3,  # Pink (son)
    (240,229,220, 255): 4, # Brown (cupboard)
    (235,235,255, 255): 5, # Purple (Cookie Jar)
    (254,239,198, 255): 6, # Tan (Cookie) 
    (157,66,67, 255): 7, # Maroon (Stool)
    (235,254,220, 255): 8, # Green (Dish and rag)
    (250,105,130, 255): 9, # Red (Sink)
    (110,200,250, 255): 10, # Blue (Water)
    (255,224,185, 255): 11, # Orange (Curtain)
    (255,185,204, 255): 12, # Light Red (Outdoors)
    (255,210,210, 255): 13, # Salmon (dishes)
    (215,215,215, 255): 14 # Grey (countertops)
}
count = 0
count2 = 0

def convert_image_to_array(image_path, color_mapping):
    image = Image.open(image_path)
    width, height = image.size

    pixel_array = []
    global count
    global count2

    # for y in range(height):
    #     row = []
    #     for x in range(width):
    #         pixel_color = image.getpixel((x, y))
    #         if pixel_color in color_mapping:
    #             row.append(color_mapping[pixel_color])
    #             count += 1
    #         else:
    #             row.append(-1)  # Default value for unmapped colors
    #             count2 += 1
    #     pixel_array.append(row)

    tolerance = 50
    for y in range(height):
        row = []
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            closest_color = min(color_mapping.keys(), key=lambda c: sum(abs(b - p) for b, p in zip(c, pixel_color)))
            if sum(abs(b - p) for b, p in zip(closest_color, pixel_color)) <= tolerance:
                row.append(color_mapping[closest_color])
                count += 1
            else:
                row.append(-1)  # Default value for unmapped colors
                count2 += 1
        pixel_array.append(row)

    return pixel_array

def main():
    input_image_path = "cookie_theft_outline.png"
    output_array = convert_image_to_array(input_image_path, color_mapping)
    output_file_path = "output_array.csv"

    with open(output_file_path,'w', newline='') as output_file:
        csv_writer= csv.writer(output_file)
        for row in output_array:
            csv_writer.writerow(row)

    print("Output array written to", output_file_path)
    print("Miss rate: " + str((count2)/(count + count2) * 100) + "%")   
    print("Note: a miss is classified as a color in the image that is not one of the categorized colors \n (notated as -1 in the resultant csv file)")

if __name__=="__main__":
    main()