import face_recognition
import os
import pickle
from PIL import Image, ImageDraw

# Load known face encodings
with open("known_faces.pkl", "rb") as f:
    known_faces = pickle.load(f)

known_names = list(known_faces.keys())
known_encodings = list(known_faces.values())

for filename in os.listdir("photos"):
    path = os.path.join("photos", filename)
    image = face_recognition.load_image_file(path)
    locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, locations)

    # Convert to PIL for drawing
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    print(f"\n📷 {filename}: Found {len(encodings)} face(s)")

    for (top, right, bottom, left), face_encoding in zip(locations, encodings):
        name = "Unknown"
        min_distance = 0.45  # You can tune this threshold

        for person_name, encodings in known_faces.items():
            results = face_recognition.compare_faces(encodings, face_encoding)
            distances = face_recognition.face_distance(encodings, face_encoding)

            if True in results:
                best_match_idx = distances.argmin()
                if distances[best_match_idx] < min_distance:
                    name = person_name
                    min_distance = distances[best_match_idx]

        draw.rectangle([left, top, right, bottom], outline="green", width=2)
        draw.text((left, top - 10), name, fill="green")

        print(f" → Detected: {name}")

    # Optional: Save or show the result
    output_path = os.path.join("output", filename)
    os.makedirs("output", exist_ok=True)
    pil_image.save(output_path)
