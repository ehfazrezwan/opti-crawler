import asyncio
import csv
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from pathlib import Path


def get_filename_from_url(url: str) -> str:
    """Extract the endpoint from URL and create a filename."""
    path = urlparse(url).path
    # Get the last non-empty part of the path
    endpoint = [p for p in path.split("/") if p][-1]
    return f"{endpoint}.md"


async def process_url(
    crawler: AsyncWebCrawler, url: str, run_conf: CrawlerRunConfig, category: str
):
    """Process a single URL and save its markdown."""
    try:
        result = await crawler.arun(url=url, config=run_conf)

        # Create output directory if it doesn't exist
        output_dir = Path(f"output/{category}")
        output_dir.mkdir(exist_ok=True)

        # Generate dynamic filename based on URL endpoint
        output_file = output_dir / get_filename_from_url(url)

        # Write both the main markdown and references
        markdown_content = result.markdown_v2.markdown_with_citations
        if result.markdown_v2.references_markdown:
            markdown_content += (
                "\n\n## References\n" + result.markdown_v2.references_markdown
            )

        output_file.write_text(markdown_content)
        print(f"✓ Processed {url} -> {output_file}")

        # Print stats about content
        print(
            f"  Main content length: {len(result.markdown_v2.markdown_with_citations)}"
        )
        if result.markdown_v2.references_markdown:
            print(f"  References length: {len(result.markdown_v2.references_markdown)}")

    except Exception as e:
        print(f"✗ Error processing {url}: {str(e)}")


async def main():
    # Configure browser and crawler settings
    browser_conf = BrowserConfig(
        headless=True,  # Run in headless mode
        java_script_enabled=True,  # Enable JavaScript for dynamic content
    )

    # Configure markdown generator with specific options
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_images": True,  # Skip image references
            "body_width": 80,  # Wrap text at 80 characters
            "skip_internal_links": True,  # Skip same-page anchor links
            "include_sup_sub": True,  # Handle superscript/subscript better
            "ignore_links": True,
        }
    )

    # Configure crawler
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,  # Ensure fresh content
        page_timeout=30000,  # 30 second timeout
        markdown_generator=md_generator,
    )

    # Read URLs from CSV
    urls = []
    # with open("insight_links.csv", "r") as f:
    with open("product_links.csv", "r") as f:
        reader = csv.DictReader(f)
        urls = [row["URL"] for row in reader]

    print(f"Found {len(urls)} URLs to process")

    # Process URLs in batches of 5 for efficiency
    batch_size = 5
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        for i in range(0, len(urls), batch_size):
            batch = urls[i : i + batch_size]
            tasks = [process_url(crawler, url, run_conf, "products") for url in batch]
            await asyncio.gather(*tasks)
            print(
                f"Completed batch {i//batch_size + 1}/{(len(urls) + batch_size - 1)//batch_size}"
            )


if __name__ == "__main__":
    asyncio.run(main())
