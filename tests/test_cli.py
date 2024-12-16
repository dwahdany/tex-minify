"""Test cases for CLI functionality."""

import pytest
from click.testing import CliRunner
from pathlib import Path
from tex_minify.cli import cli


def test_minify_command(tmp_path):
    runner = CliRunner()
    
    # Create a test input file
    input_file = tmp_path / "test.tex"
    input_file.write_text(r"\input{chapter1}")
    
    # Create the input file that will be referenced
    chapter_file = tmp_path / "chapter1.tex"
    chapter_file.write_text("Chapter 1 content")
    
    # Test with output to file
    output_file = tmp_path / "output.tex"
    result = runner.invoke(cli, ["minify", str(input_file), "-o", str(output_file)])
    assert result.exit_code == 0
    assert output_file.read_text() == "Chapter 1 content"
    
    # Test with output to stdout
    result = runner.invoke(cli, ["minify", str(input_file)])
    assert result.exit_code == 0
    assert result.output == "Chapter 1 content\n"


def test_filter_bib_command(tmp_path):
    runner = CliRunner()
    
    # Create test input files
    tex_file = tmp_path / "test.tex"
    tex_file.write_text(r"""
    This is a test document.
    \cite{key1,key2}
    \citep{key3}
    """)
    
    bib_file = tmp_path / "test.bib"
    bib_file.write_text("""
@article{key1,
    title = {Title 1},
    author = {Author 1},
}

@book{key2,
    title = {Title 2},
    author = {Author 2},
}

@inproceedings{key3,
    title = {Title 3},
    author = {Author 3},
}

@misc{key4,
    title = {Title 4},
    author = {Author 4},
}
""")
    
    # Test with output to file
    output_file = tmp_path / "filtered.bib"
    result = runner.invoke(cli, ["filter-bib", str(tex_file), str(bib_file), "-o", str(output_file)])
    assert result.exit_code == 0
    
    filtered_content = output_file.read_text()
    assert "@article{key1," in filtered_content
    assert "@book{key2," in filtered_content
    assert "@inproceedings{key3," in filtered_content
    assert "@misc{key4," not in filtered_content
    
    # Test with output to stdout
    result = runner.invoke(cli, ["filter-bib", str(tex_file), str(bib_file)])
    assert result.exit_code == 0
    assert "@article{key1," in result.output
    assert "@book{key2," in result.output
    assert "@inproceedings{key3," in result.output
    assert "@misc{key4," not in result.output


def test_filter_bib_command_no_citations(tmp_path):
    runner = CliRunner()
    
    # Create test input files with no citations
    tex_file = tmp_path / "test.tex"
    tex_file.write_text("This is a test document with no citations.")
    
    bib_file = tmp_path / "test.bib"
    bib_file.write_text("""
@article{key1,
    title = {Title 1},
    author = {Author 1},
}
""")
    
    # Test with output to file
    output_file = tmp_path / "filtered.bib"
    result = runner.invoke(cli, ["filter-bib", str(tex_file), str(bib_file), "-o", str(output_file)])
    assert result.exit_code == 0
    assert output_file.read_text().strip() == ""


def test_filter_bib_command_missing_files(tmp_path):
    runner = CliRunner()
    
    # Test with non-existent TeX file
    result = runner.invoke(cli, ["filter-bib", "nonexistent.tex", "test.bib"])
    assert result.exit_code != 0
    
    # Test with non-existent BibTeX file
    tex_file = tmp_path / "test.tex"
    tex_file.write_text(r"\cite{key1}")
    result = runner.invoke(cli, ["filter-bib", str(tex_file), "nonexistent.bib"])
    assert result.exit_code != 0 