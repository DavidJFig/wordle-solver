from PIL import ImageGrab, Image
import mss
import time
import requests
import json
import base64
from io import BytesIO
import pyautogui
import random
from collections import defaultdict
from solve import update_word_list

# Ollama Constants
MODEL = "gemma3:4b"
CHAT_API_URL = "http://localhost:11434/api/chat"


starting_guess = "salet"




region_coordinates = (280, 180, 650, 250) # (left, top, right, bottom)

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
    
    
    # print("VLM is processing the image...")
    start_time = time.time()
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Extract the 5 letters shown in the image. Return exactly those 5 letters as a mapping of letters to their color, which can be either green, yellow or gray. ",
                "images": [image]
            }
        ],
        "stream": False,
        "temperature": 0.1,
    }
    response = requests.post(CHAT_API_URL, json=data)
    # print(f"VLM Request Time: {time.time() - start_time:.2f} seconds")

    if response.status_code != 200:
        print(f"VLM Error: {response.status_code} - {response.text}")
        return None
    
    response = response.json()
    
    print(f"VLM response: {response}")

    return response["message"]["content"]

if __name__ == "__main__":


    # read word list from file
    with open("shuffled_word_list.txt", "r") as f:
        word_list = f.read().splitlines()
    

    non_allowed_letters = set()          # letters certainly not in the word
    allowed_letters = defaultdict(list)  # letters in the word and the positions they cannot be in
    correct_letters = {}                 # letters in the word and the positions they are certainly in


    # wait for button press
    input("Press Enter to start solving the wordle and then switch to wordle screen...")
    time.sleep(5)

    print("Starting solver...")

    for i in range(6):
        print("Guess #", i + 1)
        if i == 0:
            guess = starting_guess
        else:
            word_list = update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters)
            guess = random.choice(word_list)
        print("Guess:", guess)




        for letter in guess:
            pyautogui.press(letter)
            time.sleep(0.5)

        pyautogui.press("enter")
    

        # wait for wordle to update
        print("Waiting for Wordle to update...", end="", flush=True)
        time.sleep(5)
        print("Moving on.")

        

        screenshot_region = capture_screen_region(region_coordinates)

        # Convert to base64
        buffered = BytesIO()
        screenshot_region.save(buffered, format="PNG") 
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print(f"Captured region with coordinates {region_coordinates}", flush=True)

        # save the image
        screenshot_region.save(f"screenshot{i}.png", format="PNG")  # Save the image as PNG
        
        
        if screenshot_region:
            screenshot_region.show()  

            # Extract text from the captured image using the VLM
            extracted_text = get_characters(img_base64)

            if extracted_text is None:
                print("VLM Error: No text extracted from the image.")
                exit(1) # TODO: handle VLM error

        # update word list
        for letter, color in extracted_text.items():
            if color == "green":
                correct_letters[letter] = guess.index(letter)
            elif color == "yellow":
                allowed_letters[letter].append(guess.index(letter))
            elif color == "gray":
                non_allowed_letters.add(letter)
            else:
                print(f"Unknown color '{color}' for letter '{letter}'")
        else:
            print("Failed to capture the screen region.")

        region_coordinates = (region_coordinates[0], region_coordinates[1] + 70, region_coordinates[2], region_coordinates[3] + 70)