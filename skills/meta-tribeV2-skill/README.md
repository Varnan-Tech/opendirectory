# Meta Tribe Skill

AI Skill that uses Meta's TRIBE v2 fMRI Model to analyze the neuroscience of video hooks, reels, and scripts. 

Instead of guessing what makes a hook engaging using prompt engineering, this skill predicts actual human brain activity across the scientifically validated Yeo-7 Functional Networks, giving you an evidence-based Engagement Report for your content.

<img width="2752" height="1536" alt="meta-tribeV2-skill-cover-image" src="https://github.com/user-attachments/assets/7fc9b683-2c9a-416e-92c8-79a0f4f0228e" />

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install meta-tribeV2-skill --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fmeta-tribeV2-skill&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What This Skill Does

This skill provides the infrastructure to host the massive 80GB TRIBE v2 model pipeline and gives your AI Agent the ability to:
1. Process video, audio, or text scripts.
2. Intercept and optimize the media (downscaling video to 360p at 10fps to avoid hour-long bottleneck processing times).
3. Process the content through V-JEPA (Vision), W2V-BERT (Acoustics), and LLaMA 3.2 3B (Linguistics).
4. Predict human brain fMRI activity across the Yeo-7 networks.
5. Generate an actionable, human-readable neuroscience report without the jargon.

---

## Deployment Options

Because TRIBE v2 requires a massive amount of VRAM (24GB for text, up to 80GB for video), we offer 3 different deployment options so anyone can use it, regardless of budget or technical expertise.

### 1. Google Colab (Zero Cost, Decoupled)
Best for users without a cloud budget. Colab provides free T4 GPUs.
* How it works: We use a decoupled architecture. You run the heavy AI inference in a Colab Notebook, which outputs a preds.npy prediction file. You then run a local script on your laptop to generate the report.
* Setup:
  1. Open Google Colab and upload the script from scripts/colab_inference.py into a new Notebook.
  2. Run the notebook. It will output preds.npy and segments.json.
  3. Download those files to your machine and run: `python scripts/local_analyze.py --preds preds.npy`. This will output a text report and an ASCII terminal graph showing the engagement peaks and valleys.

### 2. RunPod (Serverless, Pay-per-second)
Best for production agents and developers. You only pay for the seconds the model is running.
* How it works: We provide a RunPod Handler and a custom Dockerfile that caches the 80GB model inside the image.
* Setup:
  1. Build the Docker image using server/Dockerfile.runpod: docker build -f Dockerfile.runpod -t tribe-runpod .
  2. Push the image to Docker Hub or GHCR.
  3. Create a new RunPod Serverless Endpoint using your image URL.
  4. Point your AI Agent to your RunPod Endpoint URL.

### 3. AWS EC2 Persistent (Enterprise, BYO-Compute)
Best for heavy, continuous usage. 
* How it works: Automatically provisions an AWS g5.12xlarge instance (4x A10G GPUs) and runs a FastAPI server.
* Setup:
  1. Ensure your AWS account has a vCPU quota limit of at least 48 for "Running On-Demand G and VT instances".
  2. Run bash scripts/launch_persistent.sh to provision the instance.
  3. Run export HF_TOKEN="your_token" followed by bash scripts/deploy_to_persistent.sh to build and launch the Docker API.

#### AWS GPU Lifecycle & Estimated Costs
Running the `g5.12xlarge` instance (4x A10G GPUs) provides incredible speed but costs **$7.09 per hour** on On-Demand pricing. It is crucial to manage this lifecycle.
1. **Launch:** Run `bash scripts/launch_persistent.sh` (Takes ~3 minutes).
2. **Analyze:** Run your videos through the API.
3. **Terminate:** When you are completely finished for the day, you MUST terminate the instance to stop billing.
   - Run `aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"` to find your Instance ID.
   - Run `aws ec2 terminate-instances --instance-ids <YOUR_INSTANCE_ID>`.
   - *Do not just "stop" the instance if you don't want to pay for EBS Volume storage costs overnight. Terminate it.*

---

## HuggingFace Authentication (Required for all methods)

TRIBE v2 relies on meta-llama/Llama-3.2-3B, which is a Gated Model.
1. Create a HuggingFace account.
2. Go to the Llama 3.2 3B page and TRIBE v2 page and agree to Meta's license terms.
3. Generate a HuggingFace Access Token (Read permissions) at huggingface.co/settings/tokens.
4. Supply this token via the HF_TOKEN environment variable.

---

## The Neuroscience of the Engagement Report

The AI agent will read the raw API output and translate the neuroscience into plain English for you:

* VAN (Ventral Attention Network): Translated to "Is this surprising enough to stop a scroll?". High VAN means the content is novel and creates a pattern interrupt.
* DMN (Default Mode Network): Translated to "Will people get bored and tune out?". High DMN is bad. It means the brain is wandering. The AI uses this to identify "Cut Candidates" in your video.
* DAN (Dorsal Attention Network): Translated to "Are people actively following along?". High DAN means strong logical focus.
* Limbic Network: Translated to "Does this make people feel something?". High Limbic means strong emotional response.

Check out the [Results Showcase](results_showcase.md) for actual examples of Neuro-Marketing reports generated by this skill.
