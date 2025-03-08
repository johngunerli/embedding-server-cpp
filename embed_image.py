import sys
import json
import torch
import numpy as np
from PIL import Image
from transformers import ViTImageProcessor, ViTModel


model_name = "facebook/dino-vits16"
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTModel.from_pretrained(model_name)

def array_to_image(image_array):
    image_array = np.array(image_array, dtype=np.uint8)
    image = Image.fromarray(image_array)
    return image

def image_to_embedding(image):
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)


    embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
    return embedding

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No JSON file provided"}))
        sys.exit(1)

    json_path = sys.argv[1]

    try:
 
        with open(json_path, "r") as f:
            data = json.load(f)
        
        if "image" not in data:
            raise ValueError("Missing 'image' key in JSON.")

 
        image_array = data["image"]
        image = array_to_image(image_array)

 
        embedding = image_to_embedding(image)

 
        print(json.dumps({"embedding": embedding}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
