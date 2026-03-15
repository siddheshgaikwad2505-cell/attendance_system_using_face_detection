import cv2
import numpy as np
from .models import Student, Attendance
from django.utils import timezone


def train_model():

    students = Student.objects.all()

    faces = []
    labels = []
    label_map = {}

    for idx, student in enumerate(students):

        img_path = student.image.path

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces.append(gray)
        labels.append(idx)

        label_map[idx] = student

    labels = np.array(labels)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, labels)

    return recognizer, label_map


def start_camera(subject):

    recognizer, label_map = train_model()

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            label, confidence = recognizer.predict(face)

            if confidence < 50:

                student = label_map[label]

                name = student.name

                cv2.putText(frame, f"{name} Y/N",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,255,0),
                            2)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('y'):

                    Attendance.objects.create(
                        student=student,
                        subject=subject,
                        date=timezone.now()
                    )

                    print("Attendance Marked")

                elif key == ord('n'):
                    print("Skipped")

            else:

                cv2.putText(frame, "Unknown",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,0,255),
                            2)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow("Attendance Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()