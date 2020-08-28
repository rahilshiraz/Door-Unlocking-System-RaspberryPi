import cv2
import numpy as np
import time
import os

def detectface(img,model):
    (h,w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img,(300,300)),scalefactor=1.0,size=(300,300),
                                mean=(104.0,177.0,123.0))
    model.setInput(blob)
    detections = model.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0][0][i][2]
        if confidence > 0.5:
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX, startY, endX, endY) = box.astype("int")
            face = img[startY:endY,startX:endX]
            coordinates = [startX, startY, endX, endY]
    return coordinates,face

if __name__ == '__main__':
    cam = cv2.VideoCapture(1)
    count = 0
    id = input('Enter the id:')
    dirpath = os.path.dirname(__file__)
    modelFile = f"{dirpath}/model/res10_300x300_ssd_iter_140000.caffemodel"
    configFile = f"{dirpath}/model/deploy.prototxt.txt"
    model = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    while True:
        _,frame = cam.read()
        try:
            coordinates, face = detectface(frame,model)
        except:
            print('No face detected')
            continue
        writepath = os.path.join('DATA','user')
        cv2.imwrite(f"{dirpath}/{writepath}{id}.{str(count)}.jpg", face)
        cv2.rectangle(frame,(startX, startY),(endX,endY),(0,255,0),2)
        count += 1
        print(count)
        cv2.imshow("FACE",frame)
        if cv2.waitKey(1) & count==150:
            break
        time.sleep(0.1)
    cam.release()
    cv2.destroyAllWindows()