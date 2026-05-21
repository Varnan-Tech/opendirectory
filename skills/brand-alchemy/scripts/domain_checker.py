import sys
import socket
import urllib.request
import json
import ssl

# Set UTF-8 encoding for standard output to support emojis
sys.stdout.reconfigure(encoding='utf-8')

def check_domain(domain):
    print(f"Checking {domain}...")
    
    # Primary Check: DNS Lookup (Fastest and universally supports .ai, .in, .io, etc.)
    # We attempt to resolve the domain. If it fails with a specific error (NXDOMAIN), it's likely available.
    try:
        # gethostbyname_ex will raise socket.gaierror if domain doesn't exist
        socket.gethostbyname_ex(domain)
        print(f"❌ {domain} : TAKEN (Active DNS record found)")
        return
    except socket.gaierror as e:
        # Check if the error is specifically because the host is not known (errno 11001 on Windows, or other NXDOMAIN equivalents)
        # We will still fallback to RDAP just in case it's a transient DNS issue or registered without A records,
        # but a socket.gaierror often means NXDOMAIN.
        pass

    # Fallback Check: RDAP protocol via HTTP
    # Create an unverified context just in case there are local SSL certificate issues
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        f"https://rdap.org/domain/{domain}",
        headers={'Accept': 'application/rdap+json'}
    )

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            if response.status == 200:
                print(f"❌ {domain} : TAKEN (RDAP 200 OK)")
            else:
                print(f"⚠️ {domain} : UNKNOWN (RDAP returned {response.status})")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"✅ {domain} : AVAILABLE (RDAP 404 Not Found)")
        elif e.code == 403:
            print(f"⚠️ {domain} : BLOCKED/RESERVED (RDAP 403 Forbidden - likely a premium or blocked query)")
        else:
            print(f"⚠️ {domain} : UNKNOWN (RDAP HTTP Error {e.code})")
    except Exception as e:
        print(f"⚠️ {domain} : ERROR checking RDAP ({str(e)})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python domain_checker.py <domain1> [domain2] ...")
        print("Example: python domain_checker.py mybrand.com mybrand.ai mybrand.in")
        sys.exit(1)

    for d in sys.argv[1:]:
        check_domain(d)
