import requests
import json
import time

URL = "http://localhost:11434/api/pull"


# downloads the requested model from Ollama or attempts to update it if it already exists
# returns attribute "status" as "success" if successful
def pull_model(model):
    data = {
        "model": model,
        "stream": False
    }
    response = requests.post(URL, json=data)
    response_json = json.loads(response.text)
    return response_json["status"]


def load_model(MODEL):
    # pull the model
    if pull_model(MODEL) == "success":
        print("Model successfully loaded.")        
    else:
        print("Model pull failed. Exiting...")
    

if __name__ == "__main__":
    print("This script is not meant to be run directly.")