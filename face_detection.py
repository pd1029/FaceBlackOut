import cv2
import sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture("Will_Smith_test.avi")
if (video_capture.isOpened() == False):  
    print("Error reading video file") 

frame_width = int(video_capture.get(3)) 
frame_height = int(video_capture.get(4)) 

size = (frame_width, frame_height) 

writer = cv2.VideoWriter("Will_Smith_test_face_detected.avi",cv2.VideoWriter_fourcc(*'MJPG'),  20, size)

while (video_capture.isOpened()):
    # Capture frame-by-frame 

    ret, frame = video_capture.read()
    
    if not(ret):
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    writer.write(frame) 
    #cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'): 
        break

writer.release()
video_capture.release()
cv2.destroyAllWindows()
print('Successfully saved')
