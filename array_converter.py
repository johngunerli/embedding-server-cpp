import numpy as np
import json
from PIL import Image
import requests
from io import BytesIO

# download the image from URL
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))


img = img.convert('RGB')


img_array = np.array(img).tolist()  

output = {"image": img_array}


with open('image_array.json', 'w') as f:
    json.dump(output, f)

# Call the API
url = "http://localhost:8080/embed"
response = requests.post(url, json=output)
print(response.json())  # Print API response
