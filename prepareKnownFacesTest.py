import dlib
import numpy as np
from PIL import Image

# Load with PIL (avoids OpenCV weirdness)
img = Image.open("known_faces/Mike.jpg").convert("RGB")
rgb_image = np.array(img, dtype=np.uint8)

# Ensure contiguous array
rgb_image = np.ascontiguousarray(rgb_image)

# Confirm shape/dtype again
print("dtype:", rgb_image.dtype)
print("shape:", rgb_image.shape)
print("contiguous:", rgb_image.flags['C_CONTIGUOUS'])

# Run detector
detector = dlib.get_frontal_face_detector()
faces = detector(rgb_image)
print(f"Faces found: {len(faces)}")