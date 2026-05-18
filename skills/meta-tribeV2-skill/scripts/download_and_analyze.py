import os
import time
import json
import requests
import argparse

def analyze_social_url(social_url, api_url="http://13.221.72.26:8000/analyze"):
    print(f"Sending {social_url} to TRIBE API...")
    print("This will take 1-5 minutes depending on video length. The AWS instance is downloading and analyzing it...")
    
    start_time = time.time()
    try:
        api_resp = requests.post(api_url, json={"social_url": social_url}, timeout=600)
        elapsed = time.time() - start_time
        
        if api_resp.status_code == 200:
            result = api_resp.json()
            print(f"\nSUCCESS! Analysis completed in {elapsed:.1f} seconds.")
            return result
        else:
            print(f"\nAPI Error ({api_resp.status_code}): {api_resp.text}")
            return None
    except Exception as e:
        print(f"\nRequest Error: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze an Instagram Reel, YouTube Shorts, or TikTok URL with TRIBE v2.")
    parser.add_argument("url", help="Social media URL")
    args = parser.parse_args()
    
    results = analyze_social_url(args.url)
    if results:
        print("\n--- RAW TRIBE SCORES ---")
        print(json.dumps(results, indent=2))
        print("\nCopy these z_scores to the AI agent for the Neuro-Marketing Report.")