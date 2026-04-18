"""
Email Verifier Script
This script will handle the logic for verifying cold emails.
"""

import argparse
import os
import re
import requests
import subprocess
import json
import pandas as pd
from urllib.parse import urlparse


def get_domain(company_name):
    """
    Extracts the domain for a given company name.
    Uses Clearbit Autocomplete API, otherwise falls back to a simple heuristic.
    """
    try:
        response = requests.get(
            f"https://autocomplete.clearbit.com/v1/companies/suggest?query={company_name}",
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                domain = data[0].get("domain")
                if domain:
                    return domain
    except Exception as e:
        print(f"Clearbit autocomplete failed for {company_name}: {e}")

    # Fallback heuristic
    clean_name = re.sub(r"[^\w\s]", "", company_name)
    clean_name = re.sub(r"\s+", "", clean_name)
    return f"{clean_name.lower()}.com"


def parse_args():
    parser = argparse.ArgumentParser(description="Cold Email Verifier")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument(
        "--output",
        default="output.csv",
        help="Path to output CSV (default: output.csv)",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["validemail", "reacher-http", "reacher-cli"],
        help="Verification mode",
    )
    parser.add_argument(
        "--reacher-url",
        default="http://localhost:8080/v0/check_email",
        help="Reacher HTTP URL (default: http://localhost:8080/v0/check_email)",
    )
    parser.add_argument(
        "--test",
        "--dry-run",
        action="store_true",
        dest="test",
        help="Run in test/dry-run mode",
    )
    return parser.parse_args()


_reacher_cli_warning_printed = False


def verify_validemail(email):
    api_key = os.environ.get("VALIDEMAIL_API_KEY")
    if not api_key:
        print("Error: VALIDEMAIL_API_KEY environment variable not set.")
        return False

    try:
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        response = requests.get(
            f"https://validemail.co/api/v1/validate?email={email}",
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("isDeliverable") is True
    except Exception as e:
        print(f"ValidEmail API error for {email}: {e}")
        return False


def verify_reacher_http(email, url):
    try:
        response = requests.post(url, json={"to_email": email})
        response.raise_for_status()
        data = response.json()
        return data.get("is_reachable") == "safe"
    except Exception as e:
        print(f"Reacher HTTP error for {email}: {e}")
        return False


def verify_reacher_cli(email):
    global _reacher_cli_warning_printed
    if not _reacher_cli_warning_printed:
        print(
            "WARNING: Residential ISPs often block Port 25. Reacher CLI may fail or timeout if run from a residential network."
        )
        _reacher_cli_warning_printed = True

    try:
        result = subprocess.run(
            ["check_if_email_exists", email],
            capture_output=True,
            text=True,
            check=False,
        )

        try:
            data = json.loads(result.stdout)
            return data.get("is_reachable") == "safe"
        except json.JSONDecodeError:
            return "safe" in result.stdout.lower()

    except FileNotFoundError:
        print(
            "Error: check_if_email_exists command not found. Please install reacher CLI."
        )
        return False
    except Exception as e:
        print(f"Reacher CLI error for {email}: {e}")
        return False


def generate_permutations(first: str, last: str, domain: str) -> list[str]:
    first = re.sub(r"[^\w\s]", "", first.strip().lower())
    last = re.sub(r"[^\w\s]", "", last.strip().lower())
    domain = domain.strip().lower()

    perms = []
    if first: 
        perms.append(f"{first}@{domain}")
    
    if first and last:
        perms.extend([
            f"{first}.{last}@{domain}",
            f"{first}{last}@{domain}"
        ])

    return list(dict.fromkeys([p for p in perms if p]))


def main():
    args = parse_args()
    print(f"Arguments parsed: {args}")

    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Error reading input CSV: {e}")
        return

    required_cols = ["First Name", "Last Name", "Company Name"]

    col_mapping = {
        "Founder 1 First Name": "First Name",
        "Founder 1 Last Name": "Last Name",
        "Startup Name": "Company Name",
        "Website": "Domain",
    }
    df.rename(columns=col_mapping, inplace=True)

    for col in required_cols:
        if col not in df.columns:
            print(
                f"Error: Input CSV must contain '{col}' column. Found: {list(df.columns)}"
            )
            return

    valid_emails = []

    for index, row in df.iterrows():
        first = str(row["First Name"])
        last = str(row["Last Name"])
        company = str(row["Company Name"])

        domain = ""
        if (
            "Domain" in df.columns
            and pd.notna(row["Domain"])
            and str(row["Domain"]).strip()
        ):
            domain_raw = str(row["Domain"]).strip()
            parsed = urlparse(domain_raw)
            if parsed.netloc:
                domain = parsed.netloc
            else:
                domain = parsed.path

            if domain.startswith("www."):
                domain = domain[4:]
        else:
            domain = get_domain(company)

        perms = generate_permutations(first, last, domain)

        found_valid = ""
        for email in perms:
            if args.test:
                print(f"[TEST] Generated permutation: {email}")
                if not found_valid:
                    found_valid = email  # Assume first is valid in test mode
            else:
                is_valid = False
                if args.mode == "validemail":
                    is_valid = verify_validemail(email)
                elif args.mode == "reacher-http":
                    is_valid = verify_reacher_http(email, args.reacher_url)
                elif args.mode == "reacher-cli":
                    is_valid = verify_reacher_cli(email)

                if is_valid:
                    found_valid = email
                    break

        valid_emails.append(found_valid)

    df["Valid Email"] = valid_emails

    try:
        df.to_csv(args.output, index=False)
        print(f"Output saved to {args.output}")
    except Exception as e:
        print(f"Error saving output CSV: {e}")


if __name__ == "__main__":
    main()
