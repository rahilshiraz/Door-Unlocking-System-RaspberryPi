import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = r"F:\College Project\DATA"
def getImageswithid(path):
    imagepaths = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagepath in imagepaths:
        faceimg = Image.open(imagepath).convert('L')  #convert to gray
        facenp = np.array(faceimg,'uint8')
        ID = int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(facenp)
        print(ID)
        IDs.append(ID)
        cv2.imshow("training",facenp)
        cv2.waitKey(1)
    return np.array(IDs),faces

IDs, faces = getImageswithid(path)
recognizer.train(faces, IDs)
recognizer.save(r"recognizer\trainingdata.yml")
print('Saved')
