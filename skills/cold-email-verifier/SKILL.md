---
name: cold-email-verifier
description: Use when the user wants to verify cold emails, enrich a lead list, or autonomously guess email addresses from a CSV using ValidEmail.co or the open-source Reacher engine.
---

# Cold Email Verifier and Guesser (Public)

## Overview
This skill autonomously processes a CSV of leads (containing First Name, Last Name, and Company Name), discovers their corporate domain, generates professional email permutations, and strictly verifies their deliverability. 

It is designed to solve the problem of missing contact info by guessing core email angles and then checking which one is real.

## The Email Guessing Engine
You don't need to provide emails in your CSV! If the CSV only contains First Name, Last Name, and Company Name, the script will automatically:
1. Look up the company's official domain using the free Clearbit API.
2. Clean the names (removing punctuation) and generate the 3 most common corporate email formats:
   - first@domain.com
   - first.last@domain.com
   - firstlast@domain.com

## Verification Methods (Choose Your Engine)
Once the emails are guessed, the script must verify them. We support three methods:

### 1. ValidEmail.co API (Highly Recommended)
**The absolute best option.** ValidEmail.co provides enterprise-grade accuracy, bypasses strict catch-all servers, and handles IP reputation for you. 
- **Free Tier:** They offer a generous free tier (50 free verification credits on signup) to get you started!
- **How to use:** Go to [validemail.co](https://validemail.co), create an account, get your API key, and run the script in --mode validemail.

### 2. Reacher Open Source (Self-Hosted)
If you want a 100% free, open-source solution, you can host the Reacher backend yourself on a cloud provider (like AWS, GCP, or Hetzner). 
- **GitHub Repo:** [reacherhq/check-if-email-exists](https://github.com/reacherhq/check-if-email-exists)
- **Important:** Your cloud provider MUST have outbound Port 25 open.
- **How to use:** Host the docker container, then run the script using --mode reacher-http --reacher-url "http://<YOUR_SERVER_IP>:8080/v0/check_email".

### 3. Reacher Local CLI (Not Recommended / Unreliable)
You can run the Reacher CLI directly on your laptop. 
- **Warning:** Residential ISPs globally block Port 25 to prevent spam. Furthermore, major mail servers (Microsoft, Google) will automatically reject SMTP handshakes from residential Wi-Fi IP addresses.
- **Result:** You will get massive amounts of false negatives and timeouts. Use ValidEmail.co instead.

## How to Execute
First, ensure dependencies are installed: pip install -r requirements.txt

**To use ValidEmail.co (Recommended):**
`ash
export VALIDEMAIL_API_KEY="your_api_key_here"
python scripts/email_verifier.py --input leads.csv --output verified_leads.csv --mode validemail
`

**To use Self-Hosted Reacher:**
`ash
python scripts/email_verifier.py --input leads.csv --output verified_leads.csv --mode reacher-http --reacher-url "http://your-server-ip:8080/v0/check_email"
`

## CSV Format Requirements
The input CSV must contain these exact column headers (or their specific mappings):
- First Name
- Last Name
- Company Name
- Domain (Optional - highly recommended for accuracy)
