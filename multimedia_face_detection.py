import cv2
import sys

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def live_detection():
    video_capture = cv2.VideoCapture(0)

    while (video_capture.isOpened()):
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2 )

        cv2.imshow("Live Video" ,frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows


def video_detection():

    v = input("Please enter video file (present in current directory:\n")

    video_capture = cv2.VideoCapture(v)

    ret, frame = video_capture.read()

    if (video_capture.isOpened() == False):  
        print("Error reading video file") 

    frame_width = int(video_capture.get(3)) 
    frame_height = int(video_capture.get(4))

    size = (frame_width, frame_height)

    writer = cv2.VideoWriter(v + "_face_detected.avi", cv2.VideoWriter_fourcc(*'MJPG'),  20, size)

    while(video_capture.isOpened()):

        ret, frame = video_capture.read()

        if not(ret): break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        writer.write(frame)


    writer.release()
    video_capture.release()
    cv2.destroyAllWindows()
    print('Successfully saved')


def photo_detection():

    v = input("Please enter the image name(present in same directory:\n")

    img = cv2.imread(v)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imwrite(v + "_faces_detected.png",img)

    cv2.destroyAllWindows()

    print("Saved Successfully")




if __name__ == '__main__':

    print("Please enter media type:",
          "'live' for live video input",
          "'video' for video input",
          "'photo' for photo input", sep= '\n')

    s = input()

    if(s=='live'):
        live_detection()

    if (s=='video'):
        video_detection()

    if (s=="photo"):
        photo_detection()

