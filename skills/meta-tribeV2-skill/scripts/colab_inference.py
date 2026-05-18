import os
import torch
import numpy as np
import json
from tribev2 import TribeModel

os.environ["HF_TOKEN"] = "your_huggingface_token"

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading TribeModel on {device}...")
    model = TribeModel.from_pretrained("facebook/tribev2", device=device)
    print("Model loaded successfully.")

    video_url = "https://your-video-url.mp4"
    print(f"Analyzing {video_url}...")
    
    import urllib.request
    video_path = "/tmp/video.mp4"
    urllib.request.urlretrieve(video_url, video_path)
    
    df_events = model.get_events_dataframe(video_path=video_path)
    
    print("Predicting fMRI response...")
    preds, segments = model.predict(df_events)
    
    if not isinstance(preds, np.ndarray):
        preds = preds.cpu().numpy() if hasattr(preds, 'cpu') else np.array(preds)
    
    np.save("preds.npy", preds)
    with open("segments.json", "w") as f:
        json.dump([seg.to_dict() for seg in segments] if hasattr(segments[0], 'to_dict') else segments, f)
        
    print("Inference complete! Download preds.npy and segments.json to your local machine.")

if __name__ == "__main__":
    main()