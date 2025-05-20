from PIL import ImageGrab, Image
import mss

bbox_coordinates = (100, 200, 500, 400) # (left, top, right, bottom)

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
    

def get_characters(image):
    pass

if __name__ == "__main__":

    # wait for button press
    input("Press Enter to capture the screen region...")
    
    print(f"Capturing region: {bbox_coordinates}")

    screenshot_region = capture_screen_region(bbox_coordinates)
    
    if screenshot_region:
        screenshot_region.show()  # Display the captured image for verification

    if screenshot_region:
        extracted_text = get_characters(screenshot_region)

        if extracted_text:
            print("\n--- Extracted Text ---")
            print(extracted_text)
            print("----------------------")
        else:
            print("\nNo text could be extracted from the region, or an error occurred.")
    else:
        print("Failed to capture the screen region.")