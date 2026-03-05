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

def test_token_count_value(root):
    # Wait for tokenizer to load
    # We use a loose match as the status might contain extra info
    expect(root.locator("#status")).to_have_text(re.compile("Tokenizer loaded"), timeout=60000)
    
    textarea = root.locator("#input")
    # "Hello" is 2 tokens in Gemma 3 (usually BOS + "Hello")
    textarea.fill("Hello")
    
    # Wait for debounce and check
    expect(root.locator("#tokens")).to_have_text("2", timeout=10000)
