import numpy as np
import json
import argparse
from nilearn import surface
import urllib.request
import os

def init_atlas():
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
    return np.concatenate([labels_lh, labels_rh])

def analyze(preds_path):
    preds = np.load(preds_path)
    yeo7_labels = init_atlas()
    
    YEO7_MAPPING = {"Visual": 1, "DAN": 3, "VAN": 4, "Limbic": 5, "DMN": 7}
    engagement_timeseries = []
    
    hrf_offset = 5
    valid_preds = preds[hrf_offset:] if len(preds) > hrf_offset else preds

    for t in range(len(valid_preds)):
        mean_preds = valid_preds[t]
        network_means = {net: float(np.mean(mean_preds[yeo7_labels == idx])) for net, idx in YEO7_MAPPING.items()}
        all_net_means = [np.mean(mean_preds[yeo7_labels == i]) for i in range(1, 8)]
        
        pop_mean = np.mean(all_net_means) if len(all_net_means) > 1 else 0.0
        pop_std = np.std(all_net_means) + 1e-8 if len(all_net_means) > 1 else 1.0
        
        z_scores = {k: float((v - pop_mean) / pop_std) for k, v in network_means.items()}
        e_score = z_scores["DAN"] + z_scores["VAN"] + z_scores["Limbic"] + z_scores["Visual"] - z_scores["DMN"]
        engagement_timeseries.append(e_score)

    engagement_timeseries = np.array(engagement_timeseries)
    if len(engagement_timeseries) > 1:
        e_mean = np.mean(engagement_timeseries)
        e_std = np.std(engagement_timeseries) + 1e-8
        engagement_z = (engagement_timeseries - e_mean) / e_std
    else:
        engagement_z = np.zeros_like(engagement_timeseries)
        
    overall_mean_preds = np.mean(valid_preds, axis=0) if valid_preds.ndim > 1 else valid_preds
    overall_network_means = {net: float(np.mean(overall_mean_preds[yeo7_labels == idx])) for net, idx in YEO7_MAPPING.items()}
    all_overall_net_means = [np.mean(overall_mean_preds[yeo7_labels == i]) for i in range(1, 8)]
    o_pop_mean = np.mean(all_overall_net_means) if len(all_overall_net_means) > 1 else 0.0
    o_pop_std = np.std(all_overall_net_means) + 1e-8 if len(all_overall_net_means) > 1 else 1.0
    overall_z_scores = {k: float((v - o_pop_mean) / o_pop_std) for k, v in overall_network_means.items()}

    peaks = []
    valleys = []
    current_valley_start = -1
    current_peak_start = -1
    
    for t in range(len(engagement_z)):
        if engagement_z[t] < -1.0:
            if current_valley_start == -1:
                current_valley_start = t
            current_peak_start = -1
        elif engagement_z[t] > 1.0:
            if current_peak_start == -1:
                current_peak_start = t
            current_valley_start = -1
        else:
            if current_valley_start != -1 and (t - current_valley_start) >= 4:
                valleys.append((current_valley_start, t-1))
            if current_peak_start != -1 and (t - current_peak_start) >= 4:
                peaks.append((current_peak_start, t-1))
            current_valley_start = -1
            current_peak_start = -1

    if current_valley_start != -1 and (len(engagement_z) - current_valley_start) >= 4:
        valleys.append((current_valley_start, len(engagement_z)-1))
    if current_peak_start != -1 and (len(engagement_z) - current_peak_start) >= 4:
        peaks.append((current_peak_start, len(engagement_z)-1))

    print("Engagement Report")
    print("-" * 30)
    print(f"Is this surprising enough to stop a scroll? (VAN: {overall_z_scores['VAN']:.2f})")
    print(f"Will people get bored and tune out? (DMN: {overall_z_scores['DMN']:.2f})")
    print(f"Are people actively following along? (DAN: {overall_z_scores['DAN']:.2f})")
    print(f"Does this make people feel something? (Limbic: {overall_z_scores['Limbic']:.2f})")
    print("-" * 30)
    print("Time-Series Recommendations:")
    for start, end in valleys:
        print(f"Cut Candidate: {start}s - {end}s (Low engagement)")
    for start, end in peaks:
        print(f"Protect Region: {start}s - {end}s (High engagement)")

    print("\n" + "="*50)
    print(" ENGAGEMENT CURVE (Terminal View)")
    print("="*50)
    print(" Time(s) |  Z-Score Graph (-2.0  <-->  +2.0)")
    print("---------|-----------------------------------------")
    
    for t, z in enumerate(engagement_z):
        pos = int((z + 2.0) * 10)
        pos = max(0, min(40, pos))
        
        bar_list = [" "] * 41
        bar_list[20] = "|"
        bar_list[pos] = "█"
        bar = "".join(bar_list)
        
        marker = ""
        if z > 1.0: marker = " <PEAK>"
        elif z < -1.0: marker = " <VALLEY>"
            
        print(f" {t:5d}s  | {bar} {marker}")
        
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preds", required=True, help="Path to preds.npy")
    args = parser.parse_args()
    analyze(args.preds)