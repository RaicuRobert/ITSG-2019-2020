# import the necessary packages
from facealigner import FaceAligner
from imutils import paths
import face_recognition
import pickle
import os
# import the necessary packages
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2



# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images("datasetkids"))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

print("Nr. of images trained:{0}".format(len(imagePaths)))
# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    if imagePath.split(os.path.sep)[-2] == "test":
        continue
    # extract the person name from the image path
    print("[INFO] processing image {}/{}".format(i + 1,
                                                 len(imagePaths)))
    name = imagePath.split(os.path.sep)[-3]

    try:
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=800)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        continue

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb,model="cnn")

    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    # loop over the encodings
    for encoding in encodings:
        # add each encoding + name to our set of known names and
        # encodings
        knownEncodings.append(encoding)
        knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("unalignedKids.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
