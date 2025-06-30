import face_recognition
import os
import pickle

known_faces = {}

for person_name in os.listdir("known_faces"):
    person_dir = os.path.join("known_faces", person_name)
    if not os.path.isdir(person_dir):
        continue

    encodings = []
    for filename in os.listdir(person_dir):
        path = os.path.join(person_dir, filename)
        image = face_recognition.load_image_file(path)
        face_encs = face_recognition.face_encodings(image)
        if face_encs:
            encodings.append(face_encs[0])

    if encodings:
        known_faces[person_name] = encodings
        print(f"Encoded {len(encodings)} images for {person_name}")

with open("known_faces.pkl", "wb") as f:
    pickle.dump(known_faces, f)
