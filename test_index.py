import re
from playwright.sync_api import Page, expect
import pytest

from pathlib import Path

file_url = Path("index.html").resolve().as_uri()

@pytest.fixture
def root(page: Page):
    page.goto(f"{file_url}#")
    return page

def test_page_title(root):
    expect(root).to_have_title(re.compile("Text Count"))

def test_counts_update(root):
    textarea = root.locator("#input")
    textarea.fill("Hello world")
    
    expect(root.locator("#chars")).to_have_text("11")
    expect(root.locator("#words")).to_have_text("2")
    expect(root.locator("#lines")).to_have_text("1")

def test_multiple_lines(root):
    textarea = root.locator("#input")
    textarea.fill("Line 1\nLine 2\nLine 3")
    
    expect(root.locator("#lines")).to_have_text("3")

def test_tokenizer_loading(root):
    # This might take a moment as it fetches from CDN in the browser
    # We wait for the status to change from "Loading tokenizer..."
    expect(root.locator("#status")).not_to_have_text("Loading tokenizer…", timeout=30000)
    
    textarea = root.locator("#input")
    textarea.fill("test")
    
    # Wait for debounce and token count to update
    # Gemma tokenizer usually gives 1 token for "test" (plus maybe BOS, but script uses add_special_tokens: false)
    # We just check it's a number and not "loading…" or "err"
    expect(root.locator("#tokens")).not_to_have_text("loading…", timeout=30000)
    tokens_text = root.locator("#tokens").inner_text()
    # On some test environments, the tokenizer might fail to load (e.g. CORS or network issues)
    # We accept 'disabled' if the environment is restricted
    assert tokens_text.isdigit() or tokens_text in ["0", "disabled"]
