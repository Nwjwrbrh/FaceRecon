import cv2
import sqlite3
import numpy as np

def Register(name: str, department: str):
    cap = cv2.VideoCapture(0)


    _, frame = cap.read()

    img1 = frame


# Create detector and recognizer
    detector = cv2.FaceDetectorYN.create(
        "/home/abhijit71/Desktop/FaceRecon/src/recog/face_detection_yunet_2026may.onnx",
        "",
        (320, 320),
    )

    recognizer = cv2.FaceRecognizerSF.create(
        "/home/abhijit71/Desktop/FaceRecon/src/recog/face_recognition_sface_2021dec.onnx",
        "",
    )

# Detect faces in both images
    detector.setInputSize((img1.shape[1], img1.shape[0]))
    _, faces1 = detector.detect(img1)


    if faces1 is not None:
    # Get first face from each image
        face1_box = faces1[0]

    # Align and extract features
        aligned1 = recognizer.alignCrop(img1, face1_box)

        feature1 = recognizer.feature(aligned1)
        print(feature1)
        byt = feature1.tobytes()
        print(byt)
        print(np.frombuffer(byt, dtype=np.float32))
        print(feature1 == np.frombuffer(byt, dtype=np.float32))

    else:
        print("Not captured , please try again")
    
    
    

def dbWrite():
    conn = sqlite3.connect("college_club.db")
    cursor = conn.cursor()
    student_data={}
    try:
        cursor.execute("""
        INSERT INTO club (rollno, name, department, bin)
        VALUES (?, ?, ?, ?)
        """, student_data)
        conn.commit()
        print("Successfully inserted student data and embedding.")
    except sqlite3.IntegrityError:
        print("Student with this roll number already exists.")

if __name__ == "__main__":
    Register("abhi","kabhi")