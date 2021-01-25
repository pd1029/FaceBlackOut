import os
import tkinter as tk
import cv2
import face_recognition
import numpy as np

subdirs = [x[0] for x in os.walk('.')]

subdirs.remove('.')

n = len(subdirs)

for i in range(n):
    subdirs[i] = subdirs[i][2:]


def on_keyrelease(event):
    
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()
    
    # get data from test_list
    if value == '':
        data = test_list
    else:
        data = []
        for item in test_list:
            if value in item.lower():
                data.append(item)                

    # update data in listbox
    listbox_update(data)
    
    
def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')
    
    # sorting data 
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    # display element selected on list
    #print('(event) previous:', event.widget.get('active'))
    print('Selected Person:', event.widget.get(event.widget.curselection()))
    print('---')
    global person_input
    person_input = str(event.widget.get(event.widget.curselection()))
    return str(event.widget.get(event.widget.curselection()))


# --- main ---

test_list = subdirs

root = tk.Tk()

root.geometry("300x600")

entry = tk.Entry(root)
entry.pack()
entry.bind('<KeyRelease>', on_keyrelease)

listbox = tk.Listbox(root, width = 20,height = 30, font=('times', 15))
listbox.pack()
#listbox.bind('<Double-Button-1>', on_select)

person_input = ""

listbox.bind('<<ListboxSelect>>', on_select)

listbox_update(test_list)

root.mainloop()

######################################################################################

path = os.getcwd()

path1 = path + "/" + person_input

os.chdir(path1)

person = face_recognition.load_image_file(person_input+"_0001.jpg")

person_encoding = face_recognition.face_encodings(person)[0]

os.chdir(path)

v = input('Enter the image name:\n') #image_souorce

known_face_encodings = [
    person_encoding
]

known_face_names = [
    person_input
]

video_capture = cv2.VideoCapture(v)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

#writer = writer = cv2.VideoWriter( person_input+ "_face_detected.avi", cv2.VideoWriter_fourcc(*'MJPG'),  20, size)

while True:
    # Grab a single frame of video
    frame = cv2.imread(v)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    
    rgb_small_frame = small_frame[:, :, ::-1]

    
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = ""

            face_distances = face_recognition. face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left) in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/2 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)


    
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        if name!= "":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), -1)
            
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 1)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    
    cv2.imshow('Photo', frame)

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()