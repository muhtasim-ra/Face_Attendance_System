import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import sqlite3
from datetime import datetime

# Capture Video
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Import Mode Images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load Encodings
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

# OPTIMIZATION VARIABLES
frame_count = 0
faceCurFrame = []
encodeCurFrame = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # OPTIMIZATION: Process only every 8th frame
    if frame_count % 8 == 0:
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    frame_count += 1

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute("SELECT * FROM students WHERE id=?", (id,))
                student_data = c.fetchone()

                if student_data:
                    studentInfo = {
                        "id": student_data[0],
                        "name": student_data[1],
                        "major": student_data[2],
                        "starting_year": student_data[3],
                        "total_attendance": student_data[4],
                        "standing": student_data[5],
                        "year": student_data[6],
                        "last_attendance_time": student_data[7]
                    }

                    img_path_png = f'Images/{id}.png'
                    img_path_jpg = f'Images/{id}.jpg'
                    img_path_jpeg = f'Images/{id}.jpeg'

                    if os.path.exists(img_path_png):
                        imgStudent = cv2.imread(img_path_png)
                    elif os.path.exists(img_path_jpg):
                        imgStudent = cv2.imread(img_path_jpg)
                    elif os.path.exists(img_path_jpeg):
                        imgStudent = cv2.imread(img_path_jpeg)
                    else:
                        print(f"ERROR: Image not found for ID {id}")
                        imgStudent = None

                    if imgStudent is not None:
                        imgStudent = cv2.resize(imgStudent, (216, 216))
                    else:
                        imgStudent = np.zeros((216, 216, 3), dtype=np.uint8)

                    # ATTENDANCE UPDATE
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                    if secondsElapsed > 30:
                        new_attendance = studentInfo['total_attendance'] + 1
                        new_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        c.execute("UPDATE students SET total_attendance = ?, last_attendance_time = ? WHERE id = ?",
                                  (new_attendance, new_time, id))
                        conn.commit()

                        studentInfo['total_attendance'] = new_attendance
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                else:
                    print(f"ID {id} detected but not found in Database!")
                    modeType = 0
                    counter = 0

                conn.close()

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    if imgStudent is not None:
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    (cv2.waitKey
     (10))