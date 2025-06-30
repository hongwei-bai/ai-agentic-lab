import base64
import requests
import os
import json

# Step 1: Define image path
img1 = "test_images/1hpojmqb7yw8ex9w3h1muh9ep.jpg"
img2 = "test_images/4.jpg"
image_path = os.path.join(os.getcwd(), img2)  # or absolute path

# Step 2: Encode image to base64
with open(image_path, "rb") as f:

    image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

# Step 3: Define the prompt and call Ollama
payload = {
    "model": "llava",
    "prompt": "provide a short description of the photo",
    "images": [image_base64],
    "stream": False
}

response = requests.post("http://localhost:11434/api/generate", json=payload)

# Step 4: Print result
full_response = ""
for line in response.iter_lines(decode_unicode=True):
    if line.strip():  # ignore empty lines
        data = json.loads(line)
        full_response += data.get("response", "")

print("AI says:")
print(full_response)
