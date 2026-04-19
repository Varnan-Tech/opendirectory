#!/bin/bash
# Universal Domain Availability Checker (Supports .com, .ai, .in, .tech, .dev, etc.)
# Uses a DNS NXDOMAIN primary check (works for ALL TLDs) with RDAP fallback.
# This script is part of the Brand Alchemy skill toolkit.

check_domain() {
    local domain=$1
    echo "Checking $domain..."
    
    # Primary Check: DNS Lookup (Fastest and universally supports .ai, .in, .io, etc.)
    # If the domain has no SOA record, it is almost certainly available.
    if ! dig +short SOA "$domain" | grep -q "."; then
        # Double check with NXDOMAIN status
        if dig "$domain" | grep -q "status: NXDOMAIN"; then
            echo "✅ $domain : LIKELY AVAILABLE (DNS NXDOMAIN)"
            return
        fi
    fi

    # Fallback Check: RDAP protocol
    local status_code=$(curl -Ls -o /dev/null -w "%{http_code}" "https://rdap.org/domain/$domain")
    
    if [ "$status_code" == "404" ]; then
        echo "✅ $domain : AVAILABLE (404 Not Found)"
    elif [ "$status_code" == "200" ]; then
        echo "❌ $domain : TAKEN (200 OK or Active DNS)"
    else
        echo "⚠️ $domain : TAKEN or UNKNOWN (Code: $status_code, Active DNS)"
    fi
}

# Ensure at least one argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./domain-checker.sh <domain1> [domain2] ..."
    echo "Example: ./domain-checker.sh mybrand.com mybrand.ai mybrand.in"
    exit 1
fi

# Loop through all arguments and check each domain
for domain in "$@"; do
    check_domain "$domain"
done
