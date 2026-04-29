# tests/test_scraper/test_playwright_engine.py

import pytest
from unittest.mock import patch, MagicMock

from scraper.playwright_scraper import PlaywrightEngine


@pytest.fixture
def engine():
    return PlaywrightEngine(headless=True)


# ====================== تست‌های ساده ======================

def test_engine_initialization(engine):
    assert engine.headless is True
    assert engine.proxies == []
    assert engine.user_agents == []
    assert engine.playwright is None
    assert engine.browser is None


# ====================== تست با Mock ======================

@patch("scraper.playwright_scraper.sync_playwright")
def test_start_method(mock_sync_playwright, engine):
    mock_playwright_instance = MagicMock()
    mock_browser = MagicMock()

    mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
    mock_playwright_instance.chromium.launch.return_value = mock_browser

    engine.start()

    mock_sync_playwright.return_value.start.assert_called_once()
    mock_playwright_instance.chromium.launch.assert_called_once_with(
        headless=True,
        proxy=None
    )

    assert engine.playwright == mock_playwright_instance
    assert engine.browser == mock_browser


def test_stop_method(engine):
    engine.browser = MagicMock()
    engine.playwright = MagicMock()

    engine.stop()

    engine.browser.close.assert_called_once()
    engine.playwright.stop.assert_called_once()


@patch.object(PlaywrightEngine, '_get_proxy')
@patch.object(PlaywrightEngine, '_get_user_agent')
@patch("scraper.playwright_scraper.sync_playwright")
def test_get_page_success(mock_sync, mock_get_ua, mock_get_proxy, engine):
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page = MagicMock()

    engine.browser = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page

    mock_get_ua.return_value = "Mozilla Test Agent"
    mock_get_proxy.return_value = None

    result = engine.get_page("https://example.com")

    assert result is not None
    page, context = result
    assert page == mock_page
    assert context == mock_context

    mock_browser.new_context.assert_called_once_with(user_agent="Mozilla Test Agent")
    mock_context.new_page.assert_called_once()
    mock_page.goto.assert_called_once_with("https://example.com")
    mock_page.wait_for_load_state.assert_called_once_with("networkidle")


def test_get_page_with_retries_on_failure(engine):
    engine.browser = MagicMock()
    engine.browser.new_context.side_effect = Exception("Connection error")

    result = engine.get_page("https://example.com", retries=2, delay=0)

    assert result is None
    assert engine.browser.new_context.call_count == 2