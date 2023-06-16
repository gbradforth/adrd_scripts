import cv2

def main():
  vidcap = cv2.VideoCapture('cat.mp4')
  success,image = vidcap.read()
  count = 0
  while success:
    cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
    success,image = vidcap.read()
    count += 1

if __name__=="__main__":
    main()    