from bs4 import BeautifulSoup
import csv
import sys
import os


def extract_insight_links(html_content):
    """
    Extract all href values from <a> tags that start with /insights/

    Args:
        html_content (str): HTML content as a string

    Returns:
        list: List of href values that match the pattern
    """
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <a> tags
    links = soup.find_all("a")

    # Extract href values that start with /insights/
    insight_links = []
    for link in links:
        href = link.get("href")
        if href and href.startswith("/insights/"):
            insight_links.append(href)

    return insight_links


def save_to_csv(links, output_file="insight_links.csv"):
    """
    Save the extracted links to a CSV file

    Args:
        links (list): List of links to save
        output_file (str): Name of the output CSV file
    """
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL"])  # Header
        for link in links:
            writer.writerow([link])


def main():
    # Check if HTML file is provided as argument
    if len(sys.argv) != 2:
        print("Usage: python urlExtract.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]

    # Check if file exists
    if not os.path.exists(html_file):
        print(f"Error: File '{html_file}' not found")
        sys.exit(1)

    # Read HTML file
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Extract links
    links = extract_insight_links(html_content)

    # Save to CSV
    output_file = "insight_links.csv"
    save_to_csv(links, output_file)

    print(f"Found {len(links)} insight links")
    print(f"Links have been saved to {output_file}")


if __name__ == "__main__":
    main()
