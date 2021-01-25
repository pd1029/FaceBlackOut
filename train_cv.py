import os
import cv2
import numpy as np
from sklearn import preprocessing

from PIL import Image

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def process(img):

    originalImg = img.copy()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Get the coordinates of the location of the face in the picture
    faces = faceCascade.detectMultiScale(gray_img,
                                         scaleFactor=1.2,
                                         minNeighbors=5,
                                         minSize=(50, 50))
    
    for (x, y, w, h) in faces:
        coords = [x, y, w, h]
        originalImg = originalImg[coords[1] : coords[1] + coords[3], coords[0] : coords[0] + coords[2]]

    return originalImg

    


#Initialize names and path to empty list 
names = []
path = []

# Get the names of all the users
for users in os.listdir("dataset"):
    names.append(users)


# Get the path to all the images
for name in names:
    for image in os.listdir("dataset/{}".format(name)):
        path_string = os.path.join("dataset/{}".format(name), image)
        path.append(path_string)


faces = []
ids = []

# For each image create a numpy array and add it to faces list
for img_path in path:
    image = Image.open(img_path).convert("L")

    image = process(image)

    imgNp = np.array(image, "uint8")

    id = img_path.split("/")[2].split("_")[0] + "_" + img_path.split("/")[2].split("_")[1]

    faces.append(imgNp)
    ids.append(id)
    print(id)

le = preprocessing.LabelEncoder()
ids = le.fit_transform(ids)

print(ids)

# Convert the ids to numpy array and add it to ids list
ids = np.array(ids)

print("[INFO] Created faces and names Numpy Arrays")
print("[INFO] Initializing the Classifier")


# Call the recognizer
trainer = cv2.face.LBPHFaceRecognizer_create()
# Give the faces and ids numpy arrays
trainer.train(faces, ids)
# Write the generated model to a yml file
trainer.write("training.yml")

print("[INFO] Training Done")
