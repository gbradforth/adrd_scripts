import argparse
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

parser = argparse.ArgumentParser(
    description="Transcribe audio from a video file")
parser.add_argument('file_name', type=str, help='The path to the video file')
parser.add_argument('start_time_minutes', type=int,
                    help='Start time (minutes)')
parser.add_argument('start_time_seconds', type=int,
                    help='Start time (seconds)')

args = parser.parse_args()

clip = VideoFileClip(args.file_name)
clip.audio.write_audiofile('temp_audio.wav')

# Load audio file
audio = AudioSegment.from_file('temp_audio.wav')

louder_audio = audio + 10

# Define start and end times in milliseconds
start_time = (args.start_time_minutes * 60 + args.start_time_seconds) * 1000
end_time_1 = start_time + 60 * 1000
end_time_2 = end_time_1 + 60 * 1000

# Trim and save the two audio segments
trimmed_audio_1 = louder_audio[start_time:end_time_1]
trimmed_audio_2 = louder_audio[end_time_1:end_time_2]
trimmed_audio_1.export("audio_1.wav", format="wav")
trimmed_audio_2.export("audio_2.wav", format="wav")

# Create a Recognizer instance
r = sr.Recognizer()

# Function to transcribe audio


def transcribe_audio(file_path):
    with sr.AudioFile(file_path) as source:
        # Read the entire audio file
        audio = r.record(source)
    try:
        # Using google speech recognition
        transcription = r.recognize_google(audio)
        print("Transcription: " + transcription)
        return transcription
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""


# Transcribe the two audio segments and combine the results
transcription_1 = transcribe_audio('audio_1.wav')
transcription_2 = transcribe_audio('audio_2.wav')
combined_transcription = transcription_1 + " " + transcription_2

# Write the results to a file
with open('transcript.txt', 'w', encoding='utf-8') as file:
    file.write(combined_transcription)
