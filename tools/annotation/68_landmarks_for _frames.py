import cv2
import dlib
import numpy


PREDICTOR_PATH = "/Users/xinghuihe/dlibmaster/examples/build/shape_predictor_68_face_landmarks.dat"

# 1.use dlib's frontal_face_detector to detect face
detector = dlib.get_frontal_face_detector()

# 2. use dlib's shape_predictor model to extract features
predictor = dlib.shape_predictor(PREDICTOR_PATH)


class NoFaces(Exception):
    pass

# 3. use opencv to read frames
im = cv2.imread("/Users/xinghuihe/Desktop/1.jpg")

face = detector(im, 1)

if len(face) >= 1:
    print("{} faces detected".format(len(face)))

if len(face) == 0:
    raise NoFaces

for i in range(len(face)):

# 4. use dlib's predictor() to recognize the 68 landmarks of face
    landmarks = numpy.matrix([[p.x, p.y] for p in predictor(im, face[i]).parts()])
    im = im.copy()

# 5.use enumerate function to mark the landmarks with idx and point
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])

        # opencv's putText to mark with red number
        cv2.putText(im,str(idx),pos,
        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        fontScale=0.4,color=(0,0,255))

        # opencv's circle to mark with green circle
        cv2.circle(im, pos, 3, color=(0, 255, 0))

cv2.namedWindow("im", 2)
cv2.imshow("im", im)
cv2.waitKey(0)