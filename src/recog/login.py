import cv2

cap = cv2.VideoCapture(0)

_,frame = cap.read()
print("took 1")
time.sleep(5)
_,frame2 = cap.read()
print("took 2")

print(frame)
cv2.imwrite('saved_frame.jpg', frame)
cv2.imwrite('saved_frame2.jpg', frame2)
print(frame2)
print( str(frame) == str(frame2))

import cv2

# Load images
img1 = frame
img2 = frame2

# Create detector and recognizer
detector = cv2.FaceDetectorYN.create(
    '/home/abhijit71/Desktop/FaceRecon/src/recog/face_detection_yunet_2026may.onnx',
    '',
    (320, 320)
)

recognizer = cv2.FaceRecognizerSF.create(
    '/home/abhijit71/Desktop/FaceRecon/src/recog/face_recognition_sface_2021dec.onnx',
    ''
)

# Detect faces in both images
detector.setInputSize((img1.shape[1], img1.shape[0]))
_, faces1 = detector.detect(img1)

detector.setInputSize((img2.shape[1], img2.shape[0]))
_, faces2 = detector.detect(img2)

if faces1 is not None and faces2 is not None:
    # Get first face from each image
    face1_box = faces1[0]
    face2_box = faces2[0]
    
    # Align and extract features
    aligned1 = recognizer.alignCrop(img1, face1_box)
    aligned2 = recognizer.alignCrop(img2, face2_box)
    
    feature1 = recognizer.feature(aligned1)
    feature2 = recognizer.feature(aligned2)
    
    # Compare faces
    score = recognizer.match(feature1, feature2)
    print(f"Match score: {score}")