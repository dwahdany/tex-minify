"""Test cases for BibTeX processing functionality."""

import pytest
from pathlib import Path
from tex_minify.bib_processor import extract_citations, filter_bib_file


def test_extract_single_citation():
    content = r"""
    This is a test document with a single citation \cite{key1}.
    """
    citations = extract_citations(content)
    assert citations == {"key1"}


def test_extract_multiple_citations_single_cite():
    content = r"""
    This is a test document with multiple citations \cite{key1,key2, key3}.
    """
    citations = extract_citations(content)
    assert citations == {"key1", "key2", "key3"}


def test_extract_multiple_cite_commands():
    content = r"""
    Different types of citations:
    \cite{key1}
    \citep{key2}
    \citet{key3}
    """
    citations = extract_citations(content)
    assert citations == {"key1", "key2", "key3"}


def test_extract_natbib_citations():
    content = r"""
    Testing natbib citation variants:
    \citet{key1}
    \citep{key2}
    \citet*{key3}
    \citep*{key4}
    \citeauthor{key5}
    \citeyear{key6}
    """
    citations = extract_citations(content)
    assert citations == {"key1", "key2", "key3", "key4", "key5", "key6"}


def test_extract_citations_with_tilde():
    content = r"""
    Testing citations with tilde:
    CIFAR10~\cite{key1}, CIFAR100~\cite{key2}
    Dataset1~\citep{key3}
    Method2~\citet{key4}
    """
    citations = extract_citations(content)
    assert citations == {"key1", "key2", "key3", "key4"}


def test_extract_duplicate_citations():
    content = r"""
    Duplicate citations:
    \cite{key1}
    \cite{key2,key1}
    \citep{key1,key3}
    """
    citations = extract_citations(content)
    assert citations == {"key1", "key2", "key3"}


def test_extract_no_citations():
    content = "This is a test document with no citations."
    citations = extract_citations(content)
    assert citations == set()


def test_filter_bib_file(tmp_path):
    # Create a temporary BibTeX file
    bib_content = """
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
"""
    bib_file = tmp_path / "test.bib"
    bib_file.write_text(bib_content)

    # Test filtering with different citation sets
    used_citations = {"key1", "key3"}
    filtered = filter_bib_file(bib_file, used_citations)
    
    # Check that only key1 and key3 entries are present
    assert "@article{key1," in filtered
    assert "@inproceedings{key3," in filtered
    assert "@book{key2," not in filtered


def test_filter_bib_file_no_matches(tmp_path):
    bib_content = """
@article{key1,
    title = {Title 1},
    author = {Author 1},
}
"""
    bib_file = tmp_path / "test.bib"
    bib_file.write_text(bib_content)

    used_citations = {"key2"}
    filtered = filter_bib_file(bib_file, used_citations)
    assert filtered.strip() == ""


def test_filter_bib_file_empty_citations(tmp_path):
    bib_content = """
@article{key1,
    title = {Title 1},
    author = {Author 1},
}
"""
    bib_file = tmp_path / "test.bib"
    bib_file.write_text(bib_content)

    used_citations = set()
    filtered = filter_bib_file(bib_file, used_citations)
    assert filtered.strip() == ""


def test_filter_bib_file_with_comments(tmp_path):
    bib_content = """
% This is a comment
@article{key1,
    title = {Title 1},
    author = {Author 1},
}

% Another comment
@book{key2,
    title = {Title 2},
    author = {Author 2},
}
"""
    bib_file = tmp_path / "test.bib"
    bib_file.write_text(bib_content)

    used_citations = {"key1"}
    filtered = filter_bib_file(bib_file, used_citations)
    assert "@article{key1," in filtered
    assert "@book{key2," not in filtered
 