"""
pause_analysis.py
Gets the longest, shortest, and average pause length from all provided transcript files
"""
from collections import Counter
import csv
import os
import yaml

def calculate_time_between_words(yaml_data):
    times_between_words = []

    for segment in yaml_data:
        words_list = segment.get('result', [])
        word_count = len(words_list)

        for i in range(1, word_count):
            end_current_word = words_list[i - 1]['end']
            start_next_word = words_list[i]['start']
            pause_time = start_next_word - end_current_word
            times_between_words.append(pause_time)
            if pause_time < 0:
                print(words_list[i])

    # Calculate statistics
    longest_pause = max(times_between_words, default=0)
    shortest_pause = min(times_between_words, default=0)
    average_pause = sum(times_between_words) / len(times_between_words) if times_between_words else 0

    # Calculate significant pauses
    # average_pause_length = sum(times_between_words) / len(times_between_words) if times_between_words else 0
    significant_pauses = [pause for pause in times_between_words if pause > average_pause]
    total_significant_pauses = len(significant_pauses)

    return longest_pause, shortest_pause, average_pause, total_significant_pauses


def main():
    directory_path = "../cookietheftdata/" #CHANGE TO YOUR DIRECTORY

    for directory in os.listdir(directory_path):
        if directory.startswith("PC"):  # Filter directories
            pc_directory = os.path.join(directory_path, directory)
        
            # Iterate over files in the directory
            for filename in os.listdir(pc_directory):
                if filename.endswith("_transcript_par.yaml"):  # Filter YAML files
                    yaml_file_path = os.path.join(pc_directory, filename)
        
                    # Extract the first 6 characters of the YAML file name as the row header
                    participant_id = filename[:6]

                    # Read YAML content
                    with open(yaml_file_path, 'r') as file:
                        yaml_content = yaml.safe_load(file)

                    # Calculate time between words
                    longest_pause, shortest_pause, average_pause, total_significant_pauses = calculate_time_between_words(yaml_content)

                    print("Participant:",participant_id)
                    print("Longest Pause (s):",longest_pause)
                    print("Shortest Pause (s):",shortest_pause)
                    print("Average Pause Length (s):",average_pause)
                    print("Total Significant Pauses: ",total_significant_pauses)

if __name__ == "__main__":
    main()
