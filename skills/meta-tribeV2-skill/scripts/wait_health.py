import requests
import time

url = "http://13.221.72.26:8000/health"
print("Waiting for model to load...")
for _ in range(60):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and r.json().get("model_loaded"):
            print("Model is loaded!")
            break
    except:
        pass
    time.sleep(10)
