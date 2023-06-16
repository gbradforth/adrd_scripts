"""
camera.py
Records video
@author Gwen Bradforth
@version 2023-6-16
"""
import cv2

def main():
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_file = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()

        if ret:
            output_file

if __name__=="__main__":
    main()