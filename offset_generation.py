import csv
import os
"""
@leslie + chatgpt, gwen

this program will easily find the averages of our coordinates to make it easy to find the offset
"""
def calculate_averages(csv_file_path):
    # Initialize variables to store the sum and count of x and y coordinates
    sum_x_coords = 0
    sum_y_coords = 0
    count = 0

    # Flag to track if an empty row is encountered
    emptyRow = False
    print("CSV Filepath: " + csv_file_path)
    # Open and read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader)

        # Iterate through the rows in the CSV
        for row in csv_reader:
            if row[2] == "":
                emptyRow = True
                break  # Exit the loop if an empty row is encountered

           
            x_coord = float(row[2])
            y_coord = float(row[3])

            sum_x_coords += x_coord
            sum_y_coords += y_coord
            count += 1

    # Calculate the averages
    if count > 0:
        avg_x = sum_x_coords / count
        avg_y = sum_y_coords / count
        return emptyRow, avg_x, avg_y
    
    else:
        return emptyRow, None, None
        
def alter_file(red_dot,csv_file_path, x_offset=0, y_offset=0):
    print("Altering file " + csv_file_path)
    # Open and read the CSV file
    os.makedirs("offset_eye_data", exist_ok=True)
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader)

        #create a new csv
        fileName = csv_file_path + "2"
        file = open(fileName,'w',newline='')
        writer = csv.writer(file)
        writer.writerow(["Time","Timestamp","X","Y"])

        # Iterate through the rows in the CSV
        for row in csv_reader:
            if red_dot:
                if(row[2] == ''):
                    continue
                x_coord = float(row[2]) + x_offset
                y_coord = float(row[3]) + y_offset
                writer.writerow([row[0],row[1], x_coord, y_coord]) 
            else:
                writer.writerow([row[0],row[1], row[2], row[3]]) 


# Ask the user for a directory path
directory_path = input("Enter the directory path: ")

sum_x = 0
sum_y = 0
count = 0

# Iterate through the directories starting with 'PC' or 'PD'
for file in os.walk(directory_path):
    for f in file[2]:
        if f.endswith('.csv'):
            csv_file_path = "./realigned/" + f
            emptyRow, avg_x, avg_y = calculate_averages(directory_path + "/" + f)
            print(f'CSV File: {f}')
            print(f'Average X Coordinate: {avg_x}')
            print(f'Average Y Coordinate: {avg_y}')
            x_offset = 0.5 - avg_x
            y_offset = 0.5 - avg_y
            print(f'X Offset: {x_offset}')
            print(f'Y Offset: {y_offset}')
            if emptyRow:
                print("Red dot calibration done for this file. Empty row was encountered.")
                sum_x += avg_x
                sum_y += avg_y
                count += 1
                
                alter_file(True,csv_file_path,x_offset,y_offset)
            else:
                print('No red dot calibration.')
                alter_file(False,csv_file_path)
            print("Moving onto next file. \n")

print(f'Average X Offset: {0.5 - sum_x/count}')
print(f'Average Y Offset: {0.5 - sum_y/count}')
            
            