import csv
import os
"""
@cecily (+ chatgpt)

this program will regenerate new csv files with a manually-input offset
"""
def main():
    input_path = input('Enter the input file path: ')
    if not os.path.isfile(input_path):
        print("Error: Invalid path!")
        exit(1)
    output_path = input("Enter the output file path: ")

    offset_x = 0.006086182271 #ENTER YOUR OWN X AND Y OFFSETS HERE
    offset_y = -0.04381214459

    data = []

    with open(input_path, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            data.append(row)

    with open(output_path, 'w') as output_file:
        writer = csv.writer(output_file)

        writer.writerow(data[0])

        for row in data[1:]:
            # if row[0] == '':
            #     continue

            row[2] = str(float(row[2]) + offset_x)
            row[3] = str(float(row[3]) + offset_y)

            writer.writerow(row)

main()