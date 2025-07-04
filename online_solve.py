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
from utilities.solver_logic import update_word_list
import os
import shutil

starting_guess = "salet"


region_coordinates = (300, 192, 646, 254) # (left, top, right, bottom)

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
    
    

def get_pixel_color(image_path, x, y):
    try:
        img = Image.open(image_path)
        r, g, b = img.getpixel((x, y))
        return (r, g, b)
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        exit(1)
    except IndexError:
        print(f"Error: Pixel coordinates ({x}, {y}) are out of bounds for the image.")
        exit(1)
    
def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')



if __name__ == "__main__":    

    clear_folder("screenshots")
    clear_folder("word_list_history")


    # read word list from file
    with open("shuffled_word_list.txt", "r") as f:
        word_list = f.read().splitlines()
    

    non_allowed_letters = set()          # letters certainly not in the word
    allowed_letters = defaultdict(list)  # letters in the word and the positions they cannot be in
    correct_letters = {}                 # letters in the word and the positions they are certainly in


    # wait for button press
    input("Press Enter to start solving the wordle and then switch to wordle screen...")
    time.sleep(3)

    print("Starting solver...")

    for i in range(6):
        print("Guess #", i + 1)
        if i == 0:
            guess = starting_guess
        else:
            word_list = update_word_list(word_list, non_allowed_letters, allowed_letters, correct_letters)
            # save word list to history directory
            with open(f"word_list_history/word_list_{i}.txt", "w") as f:
                f.write("\n".join(word_list))
            
            if len(word_list) == 0:
                print("No more words left to guess. Exiting.")
                exit(0)

            # look for a word with no repeating letters if possible (to maximize information gain)
            guess = next((word for word in word_list if len(set(word)) == len(word)), random.choice(word_list))

        print("Current word list length:", len(word_list))
        print("Guess:", guess)




        for letter in guess:
            pyautogui.press(letter)
            time.sleep(0.5)

        pyautogui.press("enter")
    

        # wait for wordle to update
        print("Waiting for Wordle to update...", end="", flush=True)
        time.sleep(3)
        print("Moving on.")

        

        screenshot_region = capture_screen_region(region_coordinates)

        # Convert to base64
        buffered = BytesIO()
        screenshot_region.save(buffered, format="PNG") 
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print(f"Captured screenshot.", flush=True)

        # save the image
        os.makedirs("screenshots", exist_ok=True)
        screenshot_region.save(f"screenshots/screenshot{i}.png", format="PNG")
        time.sleep(0.5)
      
                
        if screenshot_region:
            # get color of each letter
            colors_pixels = []
            colors = []
            colors_pixels.append(get_pixel_color(f"screenshots/screenshot{i}.png", 50, 10))
            colors_pixels.append(get_pixel_color(f"screenshots/screenshot{i}.png", 130, 10))
            colors_pixels.append(get_pixel_color(f"screenshots/screenshot{i}.png", 190, 10))
            colors_pixels.append(get_pixel_color(f"screenshots/screenshot{i}.png", 250, 10))
            colors_pixels.append(get_pixel_color(f"screenshots/screenshot{i}.png", 310, 10))

            for color in colors_pixels:
                if color == (181, 159, 59):
                    colors.append("yellow")
                elif color == (58, 58, 60):
                    colors.append("gray")
                else:
                    colors.append("green")

            correct_letter_count = 0
            # update word list
            for letter, color in zip(guess, colors):
                #print(f"Letter: {letter}, Color: {color}")
                if color == "green":
                    correct_letters[letter] = guess.index(letter)
                    print(f"Correct letter: {letter} at position {correct_letters[letter]}")
                    correct_letter_count += 1
                elif color == "yellow":
                    allowed_letters[letter].append(guess.index(letter))
                    print(f"Allowed letter: {letter} but not at position {allowed_letters[letter]}")
                elif color == "gray":
                    non_allowed_letters.add(letter)
                    print(f"Non-allowed letter: {letter}")
                
            if correct_letter_count == 5:
                print("Wordle solved! The word was: ", guess)
                exit(0)

        region_coordinates = (region_coordinates[0], region_coordinates[1] + 70, region_coordinates[2], region_coordinates[3] + 70)

        time.sleep(1)