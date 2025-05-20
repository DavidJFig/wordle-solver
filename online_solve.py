from PIL import ImageGrab, Image
import mss
import time
import requests
import json
import base64
from io import BytesIO


# Ollama Constants
MODEL = "gemma3:4b"
CHAT_API_URL = "http://localhost:11434/api/chat"




initial_region = (280, 180, 650, 250) # (left, top, right, bottom)

def capture_screen_region(bbox):
    try:
        with mss.mss() as sct:
            monitor = {"top": bbox[1], "left": bbox[0], "width": bbox[2] - bbox[0], "height": bbox[3] - bbox[1]}
            sct_img = sct.grab(monitor)

            img = Image.frombytes("RGB", (sct_img.width, sct_img.height), sct_img.rgb)
        return img
    except Exception as e:
        print(f"Error capturing screen region: {e}")
        return None
    
    
# Uses a VLM to read characters from the image
def get_characters(image):
    if image is None:
        print("VLM Error: No image provided to VLM.")
        return None
    
    
    print("VLM is processing the image...")
    start_time = time.time()
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Extract the 5 letters shown in the image. Return exactly those 5 letters in order with no spaces, punctuation, or additional text.",
                "images": [image]
            }
        ],
        "stream": False,
        "temperature": 0.1,
    }
    response = requests.post(CHAT_API_URL, json=data)
    print(f"VLM Request Time: {time.time() - start_time:.2f} seconds")

    if response.status_code != 200:
        print(f"VLM Error: {response.status_code} - {response.text}")
        return None
    
    response = response.json()
    print(f"Raw VLM Response: {response} with type {type(response)}")


    content = json.loads(response["message"]["content"])
    print(f"VLM Response content: {content} with type {type(content)}")
    

    return content

if __name__ == "__main__":

    # wait for button press
    input("Press Enter to capture the screen region...")
    
    print(f"Capturing region: {initial_region}", flush=True)

    screenshot_region = capture_screen_region(initial_region)


    # Convert to base64
    buffered = BytesIO()
    screenshot_region.save(buffered, format="PNG")  # You can change to "JPEG" if needed
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    print(f"Captured region", flush=True)

    
    
    if screenshot_region:
        screenshot_region.show()  

        # Extract text from the captured image using the VLM
        extracted_text = get_characters(img_base64)

        if extracted_text:
            print("\n--- Extracted Text ---")
            print(extracted_text)
            print("----------------------")
        else:
            print("\nNo text could be extracted from the region, or an error occurred.")
    else:
        print("Failed to capture the screen region.")