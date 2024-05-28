"""
tsv_to_csv.py
Cuts a portion of a tsv file and saves it to a csv file.
@author Gwen Bradforth
@version 2023-6-21
"""

import os
import csv

def main():
    # Read filename from user
    filename = "eyetrack_pd0002.tsv"
    if not os.path.isfile(filename):
        print("Error: Invalid path!")
        exit(1)

    # Read participant number from user
    participantNum = input("Enter the participant's number (1,2,3...): ")
    participant = "Participant" + str(participantNum)

    offset = input("Enter the offset (where the eyetracking starts): ")

    # Open the file for reading
    with open(filename, 'r') as file:
        # Load the TSV data into a Python object
        reader = csv.reader(file, delimiter="\t")

        print("accessing data...")
        # Access the data as a Python list
        rows = [row for row in reader if row[5] == participant and row[72] == "cookie"]
        
    # Check if the list is empty (participant does not exist)
    if not rows:
        print("Error: Participant does not exist.")
        exit(1)

    # Write to new file
    fileName = "pc000" + str(participantNum) +".csv"
    file = open(fileName,'w')
    writer = csv.writer(file)
    writer.writerow(["Time","Timestamp","X","Y"])

    # Write the data with participant to the file
    for row in rows:
        # time = row[9] + 
        timeStamp = float(row[0])/float(1000000) - float(offset) #convert from microseconds to seconds
        if (row[39] != ''):
            x = float(row[39])/float(1920)
            y = float(row[40])/float(1080)
        else:
            x = float('nan')
            y = float('nan')
        newRow = ["",timeStamp,x,y]
        writer.writerow(newRow)
    
    file.close()


if __name__=="__main__":
    main()    
