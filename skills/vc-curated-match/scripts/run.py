import argparse
import sys
import os

# Import the core pipeline components
from fetch_product_context import get_product_context
from match_vcs import match_vcs
from generate_report import generate_report

def main():
    parser = argparse.ArgumentParser(description="vc-curated-match: Algorithmically identify relevant VCs based on product context.")
    
    parser.add_argument("--description", required=True, help="Product description string.")
    parser.add_argument("--url", required=True, help="Product homepage or GitHub URL.")
    parser.add_argument("--stage", default=None, help="Optional startup stage hint.")
    parser.add_argument("--geography", default="Global", help="Optional target geography (Defaults to Global).")
    parser.add_argument("--output", default="vc-matches.md", help="Output file path (Defaults to vc-matches.md).")

    args = parser.parse_args()

    # Validation
    if not args.description or not args.description.strip():
        print("Error: --description must not be empty or whitespace only.", file=sys.stderr)
        sys.exit(1)
        
    if not args.url or not args.url.strip():
        print("Error: --url must not be empty.", file=sys.stderr)
        sys.exit(1)

    # Validate dataset existence per requirements
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "vc_funds.json")
    if not os.path.exists(data_path):
        print("Error: data/vc_funds.json not found. Make sure you are running from the skill root directory.", file=sys.stderr)
        sys.exit(1)

    try:
        # 1. Fetch Product Context
        product_context = get_product_context(
            description=args.description.strip(),
            url=args.url.strip(),
            stage=args.stage.strip() if args.stage else None,
            geography=args.geography.strip() if args.geography else "Global"
        )
        
        # 2. Match VCs
        matches = match_vcs(product_context, data_path=data_path)
        
        # 3. Generate Report
        report_str = generate_report(matches, product_context)
        
        # Ensure output directory exists and write
        output_dir = os.path.dirname(os.path.abspath(args.output))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report_str)
        except IOError:
            print(f"Error: Could not write to {args.output}.", file=sys.stderr)
            sys.exit(1)
            
        # 4. Generate Summary Console Print
        high = sum(1 for m in matches if m.get("confidence") == "High")
        medium = sum(1 for m in matches if m.get("confidence") == "Medium")
        low = sum(1 for m in matches if m.get("confidence") == "Low")
        
        print(f"Done. Report saved to {args.output}")
        print(f"Found {len(matches)} matches: {high} High, {medium} Medium, {low} Low confidence")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
