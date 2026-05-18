import os
import tempfile
import numpy as np
import json
from fastapi import FastAPI, HTTPException
import runpod

# Initialize Tribe model globally to avoid reloading on every serverless invocation
MODEL_LOADED = False
model = None
yeo7_labels = None

def init_model():
    global MODEL_LOADED, model, yeo7_labels
    if MODEL_LOADED:
        return

    import torch
    from tribev2 import TribeModel
    from nilearn import surface
    import urllib.request

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading TribeModel on {device}...")
    
    try:
        model = TribeModel.from_pretrained("facebook/tribev2", device=device)
        print("Fetching Yeo-7 surface atlas for fsaverage5...")
        
        lh_url = "https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Yeo2011_fcMRI_clustering/1000subjects_reference/Yeo_JNeurophysiol11_SplitLabels/fsaverage5/label/lh.Yeo2011_7Networks_N1000.annot"
        rh_url = "https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Yeo2011_fcMRI_clustering/1000subjects_reference/Yeo_JNeurophysiol11_SplitLabels/fsaverage5/label/rh.Yeo2011_7Networks_N1000.annot"
        
        lh_path = "/tmp/lh.Yeo2011_7Networks_N1000.annot"
        rh_path = "/tmp/rh.Yeo2011_7Networks_N1000.annot"
        
        if not os.path.exists(lh_path):
            urllib.request.urlretrieve(lh_url, lh_path)
        if not os.path.exists(rh_path):
            urllib.request.urlretrieve(rh_url, rh_path)
            
        labels_lh = surface.load_surf_data(lh_path)
        labels_rh = surface.load_surf_data(rh_path)
        yeo7_labels = np.concatenate([labels_lh, labels_rh])
        
        MODEL_LOADED = True
        print("Model and Atlas initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize model: {e}")
        raise e

def calculate_engagement(preds: np.ndarray) -> dict:
    if yeo7_labels is None:
        return {"engagement_score": 0.0, "z_scores": {}, "error": "Yeo-7 atlas not loaded"}

    # Define Yeo-7 Mapping
    YEO7_MAPPING = {"Visual": 1, "Somatomotor": 2, "DAN": 3, "VAN": 4, "Limbic": 5, "Frontoparietal": 6, "DMN": 7}
    
    mean_preds = np.mean(preds, axis=0) if preds.ndim > 1 else preds
    network_means = {}
    
    for net_name, net_idx in YEO7_MAPPING.items():
        mask = (yeo7_labels == net_idx)
        network_means[net_name] = float(np.mean(mean_preds[mask])) if np.any(mask) else 0.0

    all_net_means = [np.mean(mean_preds[yeo7_labels == i]) for i in range(1, 8) if np.any(yeo7_labels == i)]
    pop_mean = np.mean(all_net_means) if len(all_net_means) > 1 else 0.0
    pop_std = np.std(all_net_means) + 1e-8 if len(all_net_means) > 1 else 1.0

    z_scores = {k: float((v - pop_mean) / pop_std) for k, v in network_means.items()}
    engagement_score = z_scores.get("DAN", 0) + z_scores.get("VAN", 0) + z_scores.get("Limbic", 0) + z_scores.get("Visual", 0) - z_scores.get("DMN", 0)

    return {
        "engagement_score": float(engagement_score),
        "z_scores": z_scores
    }

def handler(event):
    """
    RunPod Serverless Handler.
    Expects event["input"]["video_url"] or event["input"]["text"]
    """
    init_model()
    
    job_input = event.get("input", {})
    video_url = job_input.get("video_url")
    text = job_input.get("text")
    
    if not video_url and not text:
        return {"error": "Missing video_url or text in input."}
        
    try:
        kwargs = {}
        if text:
            fd, text_path = tempfile.mkstemp(suffix=".txt")
            with os.fdopen(fd, 'w') as f:
                f.write(text)
            kwargs["text_path"] = text_path
            
        if video_url:
            import requests
            import subprocess
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            
            fd, video_path = tempfile.mkstemp(suffix=".mp4")
            with os.fdopen(fd, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            fd, optimized_path = tempfile.mkstemp(suffix=".mp4")
            os.close(fd)
            subprocess.run(f"ffmpeg -y -i {video_path} -vf scale=-2:360 -r 10 -c:v libx264 -preset ultrafast {optimized_path}", shell=True, check=True)
            kwargs["video_path"] = optimized_path
            
        df_events = model.get_events_dataframe(**kwargs)
        preds, segments = model.predict(df_events)
        
        if not isinstance(preds, np.ndarray):
            preds = preds.cpu().numpy() if hasattr(preds, 'cpu') else np.array(preds)
            
        engagement_data = calculate_engagement(preds)
        
        return {"status": "success", "engagement": engagement_data}
        
    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})