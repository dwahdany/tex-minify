"""Tests for the TeX processor."""

from pathlib import Path
import pytest
from tex_minify.processor import process_tex_file

# Get the path to the test files
TEST_DIR = Path(__file__).parent


def normalize_text(text: str) -> str:
    """Normalize text by removing trailing whitespace from each line and ensuring single newlines."""
    return '\n'.join(line.rstrip() for line in text.strip().splitlines())


def read_file(path: Path) -> str:
    """Read a file and return its contents with normalized whitespace."""
    with open(path, 'r', encoding='utf-8') as f:
        return normalize_text(f.read())


def assert_output_matches(processed: str, expected: str, message: str):
    """Assert that processed content matches expected, with helpful diff on failure."""
    processed = normalize_text(processed)
    expected = normalize_text(expected)
    
    if processed != expected:
        raise AssertionError(
            f"{message}\n\n"
            f"Expected output:\n{'-' * 40}\n{expected}\n{'-' * 40}\n\n"
            f"Actual output:\n{'-' * 40}\n{processed}\n{'-' * 40}"
        )


def test_simple_file():
    r"""Test processing a file without any \input commands."""
    test_dir = TEST_DIR / "simple"
    input_file = test_dir / "input.tex"
    expected_output = read_file(test_dir / "expected_output.txt")
    
    processed_content = process_tex_file(input_file)
    assert_output_matches(
        processed_content, 
        expected_output,
        "Content should remain unchanged"
    )


def test_single_input():
    r"""Test processing a file with a single \input command."""
    test_dir = TEST_DIR / "single_input"
    input_file = test_dir / "main.tex"
    expected_output = read_file(test_dir / "expected_output.txt")
    
    processed_content = process_tex_file(input_file)
    assert_output_matches(
        processed_content,
        expected_output,
        "Content should match expected output"
    )


def test_nested_input():
    r"""Test processing a file with nested \input commands."""
    test_dir = TEST_DIR / "nested_input"
    input_file = test_dir / "main.tex"
    expected_output = read_file(test_dir / "expected_output.txt")
    
    processed_content = process_tex_file(input_file)
    assert_output_matches(
        processed_content,
        expected_output,
        "Content should match expected output"
    )


def test_subfolder_input():
    r"""Test processing a file that inputs content from a subfolder."""
    test_dir = TEST_DIR / "subfolder_input"
    input_file = test_dir / "main.tex"
    expected_output = read_file(test_dir / "expected_output.txt")
    
    processed_content = process_tex_file(input_file)
    assert_output_matches(
        processed_content,
        expected_output,
        "Content from subfolder should be correctly included"
    )


def test_nested_subfolder_input():
    r"""Test processing a file with nested subfolder includes."""
    test_dir = TEST_DIR / "nested_subfolder"
    input_file = test_dir / "main.tex"
    expected_output = read_file(test_dir / "expected_output.txt")
    
    processed_content = process_tex_file(input_file)
    assert_output_matches(
        processed_content,
        expected_output,
        "Content from nested subfolders should be correctly included"
    ) 