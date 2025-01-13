# Optimizely Case Study Crawler

A Python-based web crawler that extracts and converts Optimizely case studies into markdown format for easy reference and documentation.

## Overview

This project consists of two main components:

1. `urlExtract.py`: Extracts case study URLs from an HTML file
2. `app.py`: Converts the extracted URLs into markdown files using async web crawling

## Prerequisites

- Python 3.9+
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd crawler-v2
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows, use: env\Scripts\activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Extract Case Study URLs

Run the URL extractor on your HTML file:

```bash
python urlExtract.py case_studies.html
```

This will:

- Parse the HTML file for case study links
- Save the extracted URLs to `insight_links.csv`

### Step 2: Convert URLs to Markdown

Run the crawler to convert the URLs to markdown:

```bash
python app.py
```

This will:

- Read URLs from the CSV file
- Process them in batches of 5 for efficiency
- Generate markdown files in the `output/products/` directory
- Include both content and references in the markdown files

## Output Structure

```
output/
└── products/
    ├── case-study-1.md
    ├── case-study-2.md
    └── ...
```

Each markdown file contains:

- Main content from the case study
- References section (if available)

## Features

- Asynchronous web crawling for improved performance
- Batch processing to handle multiple URLs efficiently
- Automatic directory creation for output
- Error handling for failed URL processing
- Progress tracking with detailed console output
- Configurable markdown generation options

## Configuration

The crawler can be configured through `app.py`:

- Browser settings (headless mode, JavaScript support)
- Markdown generation options (text width, link handling)
- Cache settings
- Page timeout values
- Batch size for processing

## Error Handling

The system handles various error cases:

- Invalid HTML files
- Missing files
- Network errors during crawling
- Invalid URLs
- Failed markdown conversions

## Testing

Run the test suite to verify functionality:

```bash
python -m pytest test_app.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]
