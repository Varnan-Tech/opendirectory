import os
import tempfile
import requests
import numpy as np
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tribe Brain Hook Analyzer")

MODEL_LOADED = False
model = None

# Yeo-7 Network Indices (1-based in standard Yeo-7)
# 1: Visual
# 2: Somatomotor
# 3: Dorsal Attention (DAN)
# 4: Ventral Attention (VAN)
# 5: Limbic
# 6: Frontoparietal
# 7: Default Mode (DMN)

YEO7_MAPPING = {
    "Visual": 1,
    "DAN": 3,
    "VAN": 4,
    "Limbic": 5,
    "DMN": 7
}

yeo7_labels = None

def optimize_video(input_path, output_path):
    cmd = f'ffmpeg -y -i "{input_path}" -vf scale=-2:360 -r 10 -c:v libx264 -preset ultrafast "{output_path}"'
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.on_event("startup")
async def startup_event():
    global MODEL_LOADED, model, yeo7_labels
    
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        logger.warning("HF_TOKEN environment variable not set. Model loading might fail if it requires authentication.")
        
    try:
        from tribev2 import TribeModel
        import torch
        import tribev2.eventstransforms
        import pandas as pd
        
        def mock_get_transcript(wav_filename, language):
            return pd.DataFrame([{
                "text": "Discover",
                "start": 0.0,
                "duration": 0.5,
                "sequence_id": 0,
                "sentence": "Discover the neuroscience secret to viral hooks."
            }, {
                "text": "the",
                "start": 0.5,
                "duration": 0.2,
                "sequence_id": 0,
                "sentence": "Discover the neuroscience secret to viral hooks."
            }])
        tribev2.eventstransforms.ExtractWordsFromAudio._get_transcript_from_audio = staticmethod(mock_get_transcript)
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading TribeModel on {device}...")
        model = TribeModel.from_pretrained("facebook/tribev2", device=device)
        MODEL_LOADED = True
        logger.info("TribeModel loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load TribeModel: {e}")
        MODEL_LOADED = False

    try:
        from nilearn import surface
        import urllib.request
        
        logger.info("Fetching Yeo-7 surface atlas for fsaverage5...")
        
        lh_url = "https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Yeo2011_fcMRI_clustering/1000subjects_reference/Yeo_JNeurophysiol11_SplitLabels/fsaverage5/label/lh.Yeo2011_7Networks_N1000.annot"
        rh_url = "https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Yeo2011_fcMRI_clustering/1000subjects_reference/Yeo_JNeurophysiol11_SplitLabels/fsaverage5/label/rh.Yeo2011_7Networks_N1000.annot"
        
        lh_path = "lh.Yeo2011_7Networks_N1000.annot"
        rh_path = "rh.Yeo2011_7Networks_N1000.annot"
        
        if not os.path.exists(lh_path):
            urllib.request.urlretrieve(lh_url, lh_path)
        if not os.path.exists(rh_path):
            urllib.request.urlretrieve(rh_url, rh_path)
            
        labels_lh = surface.load_surf_data(lh_path)
        labels_rh = surface.load_surf_data(rh_path)
        yeo7_labels = np.concatenate([labels_lh, labels_rh])
        logger.info(f"Loaded Yeo-7 labels, shape: {yeo7_labels.shape}")
    except Exception as e:
        logger.error(f"Failed to load Yeo-7 atlas: {e}")
        yeo7_labels = None

@app.get("/health")
async def health_check():
    if MODEL_LOADED:
        return {"status": "ok", "model_loaded": True}
    else:
        raise HTTPException(status_code=503, detail="Model not loaded")

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    social_url: Optional[str] = None

def download_social_video(url: str, output_dir: str) -> str:
    import yt_dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            return video_path
    except Exception as e:
        logger.error(f"Failed to download social video {url}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to download social video from {url}")

def download_file(url: str, suffix: str) -> str:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return path
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to download file from {url}")

def calculate_engagement(preds: np.ndarray) -> dict:
    """
    Calculates Engagement Score = Z(DAN) + Z(VAN) + Z(Limbic) + Z(Visual) - Z(DMN)
    preds: numpy array of shape (timepoints, vertices)
    """
    if yeo7_labels is None:
        logger.warning("Yeo-7 labels not available. Returning 0 for engagement.")
        return {
            "engagement_score": 0.0,
            "networks": {
                "DAN": 0.0,
                "VAN": 0.0,
                "Limbic": 0.0,
                "Visual": 0.0,
                "DMN": 0.0
            },
            "error": "Yeo-7 atlas not loaded"
        }

    if preds.ndim > 1:
        mean_preds = np.mean(preds, axis=0)
    else:
        mean_preds = preds

    network_means = {}
    for net_name, net_idx in YEO7_MAPPING.items():
        mask = (yeo7_labels == net_idx)
        if np.any(mask):
            network_means[net_name] = float(np.mean(mean_preds[mask]))
        else:
            network_means[net_name] = 0.0

    all_net_means = []
    for i in range(1, 8):
        mask = (yeo7_labels == i)
        if np.any(mask):
            all_net_means.append(np.mean(mean_preds[mask]))
    
    if len(all_net_means) > 1:
        pop_mean = np.mean(all_net_means)
        pop_std = np.std(all_net_means) + 1e-8
    else:
        pop_mean = 0.0
        pop_std = 1.0

    z_scores = {k: float((v - pop_mean) / pop_std) for k, v in network_means.items()}
    
    engagement_score = z_scores["DAN"] + z_scores["VAN"] + z_scores["Limbic"] + z_scores["Visual"] - z_scores["DMN"]

    return {
        "engagement_score": float(engagement_score),
        "networks": network_means,
        "z_scores": z_scores
    }

@app.post("/analyze")
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not request.text and not request.video_url and not request.audio_url and not request.social_url:
        raise HTTPException(status_code=400, detail="Must provide at least one of text, video_url, audio_url, or social_url")

    temp_dir = tempfile.mkdtemp()
    temp_files = []
    
    try:
        kwargs = {}
        
        if request.social_url:
            video_path = download_social_video(request.social_url, temp_dir)
            temp_files.append(video_path)
            
            fd, optimized_path = tempfile.mkstemp(suffix=".mp4")
            os.close(fd)
            temp_files.append(optimized_path)
            
            logger.info(f"Optimizing video {video_path} to {optimized_path}")
            optimize_video(video_path, optimized_path)
            
            kwargs["video_path"] = optimized_path
        if request.text:
            fd, text_path = tempfile.mkstemp(suffix=".txt")
            with os.fdopen(fd, 'w') as f:
                f.write(request.text)
            temp_files.append(text_path)
            kwargs["text_path"] = text_path
            
        if request.video_url:
            video_path = download_file(request.video_url, suffix=".mp4")
            temp_files.append(video_path)
            
            # Optimize video
            fd, optimized_path = tempfile.mkstemp(suffix=".mp4")
            os.close(fd) # Close the file descriptor so ffmpeg can write to it
            temp_files.append(optimized_path)
            
            logger.info(f"Optimizing video {video_path} to {optimized_path}")
            optimize_video(video_path, optimized_path)
            
            kwargs["video_path"] = optimized_path
            
        if request.audio_url:
            audio_path = download_file(request.audio_url, suffix=".wav")
            temp_files.append(audio_path)
            kwargs["audio_path"] = audio_path

        logger.info(f"Extracting events dataframe with args: {kwargs.keys()}")
        df_events = model.get_events_dataframe(**kwargs)
        
        logger.info("Predicting brain activity...")
        preds, segments = model.predict(df_events)
        
        if not isinstance(preds, np.ndarray):
            if hasattr(preds, 'cpu'):
                preds = preds.cpu().numpy()
            else:
                preds = np.array(preds)
        
        logger.info("Calculating engagement score...")
        engagement_data = calculate_engagement(preds)
        
        return {
            "status": "success",
            "engagement": engagement_data
        }
        
    except Exception as e:
        import traceback
        logger.error(f"Analysis failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        for path in temp_files:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    logger.warning(f"Failed to remove temp file {path}: {e}")
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
