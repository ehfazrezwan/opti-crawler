import unittest
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from pathlib import Path
from app import get_filename_from_url, process_url, main
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


class TestAppFunctions(unittest.TestCase):
    def test_get_filename_from_url_normal_path(self):
        """Test get_filename_from_url with a normal URL path"""
        url = "https://example.com/products/item-name"
        expected = "item-name.md"
        self.assertEqual(get_filename_from_url(url), expected)

    def test_get_filename_from_url_trailing_slash(self):
        """Test get_filename_from_url with trailing slash"""
        url = "https://example.com/products/item-name/"
        expected = "item-name.md"
        self.assertEqual(get_filename_from_url(url), expected)

    def test_get_filename_from_url_query_params(self):
        """Test get_filename_from_url with query parameters"""
        url = "https://example.com/products/item-name?param=value"
        expected = "item-name.md"
        self.assertEqual(get_filename_from_url(url), expected)

    def test_get_filename_from_url_complex_path(self):
        """Test get_filename_from_url with complex path"""
        url = "https://example.com/category/subcategory/products/item-name"
        expected = "item-name.md"
        self.assertEqual(get_filename_from_url(url), expected)


@pytest.mark.asyncio
class TestAsyncFunctions:
    async def test_process_url_success(self):
        """Test successful URL processing"""
        # Mock crawler and result
        mock_crawler = AsyncMock()
        mock_result = MagicMock()
        mock_result.markdown_v2.markdown_with_citations = "Test content"
        mock_result.markdown_v2.references_markdown = "Test references"
        mock_crawler.arun.return_value = mock_result

        # Test parameters
        url = "https://example.com/test-page"
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            page_timeout=30000,
            markdown_generator=DefaultMarkdownGenerator(),
        )
        category = "test"

        with patch("pathlib.Path.mkdir") as mock_mkdir, patch(
            "pathlib.Path.write_text"
        ) as mock_write_text:
            # Run the function
            await process_url(mock_crawler, url, run_conf, category)

            # Verify calls
            mock_mkdir.assert_called_once_with(exist_ok=True)
            mock_write_text.assert_called_once()
            assert "Test content" in mock_write_text.call_args[0][0]
            assert "Test references" in mock_write_text.call_args[0][0]

    async def test_process_url_no_references(self):
        """Test URL processing without references"""
        mock_crawler = AsyncMock()
        mock_result = MagicMock()
        mock_result.markdown_v2.markdown_with_citations = "Test content"
        mock_result.markdown_v2.references_markdown = ""
        mock_crawler.arun.return_value = mock_result

        url = "https://example.com/test-page"
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            page_timeout=30000,
            markdown_generator=DefaultMarkdownGenerator(),
        )
        category = "test"

        with patch("pathlib.Path.mkdir") as mock_mkdir, patch(
            "pathlib.Path.write_text"
        ) as mock_write_text:
            await process_url(mock_crawler, url, run_conf, category)

            mock_mkdir.assert_called_once_with(exist_ok=True)
            mock_write_text.assert_called_once()
            assert mock_write_text.call_args[0][0] == "Test content"

    async def test_process_url_error(self):
        """Test URL processing with error"""
        mock_crawler = AsyncMock()
        mock_crawler.arun.side_effect = Exception("Test error")

        url = "https://example.com/test-page"
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            page_timeout=30000,
            markdown_generator=DefaultMarkdownGenerator(),
        )
        category = "test"

        with patch("pathlib.Path.mkdir") as mock_mkdir, patch(
            "pathlib.Path.write_text"
        ) as mock_write_text:
            await process_url(mock_crawler, url, run_conf, category)

            mock_mkdir.assert_not_called()
            mock_write_text.assert_not_called()

    async def test_main_function(self):
        """Test main function execution"""
        # Mock CSV reader
        mock_csv_data = [
            {"URL": "https://example.com/page1"},
            {"URL": "https://example.com/page2"},
        ]

        # Mock AsyncWebCrawler context manager
        mock_crawler = AsyncMock()
        mock_crawler.__aenter__.return_value = mock_crawler
        mock_crawler.__aexit__.return_value = None

        with patch("csv.DictReader", return_value=mock_csv_data), patch(
            "builtins.open"
        ), patch("app.AsyncWebCrawler", return_value=mock_crawler):
            await main()

            # Verify that the crawler was called for each URL
            assert mock_crawler.arun.call_count == 2


if __name__ == "__main__":
    pytest.main(["-v", "test_app.py"])
