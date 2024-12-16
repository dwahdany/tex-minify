"""BibTeX processor module for filtering references."""

import re
from pathlib import Path
from typing import Set, Union

def extract_citations(content: str) -> Set[str]:
    """
    Extract all citation keys from a TeX content.
    
    Args:
        content: The TeX content to process
        
    Returns:
        Set of citation keys
    """
    # Match all citation variants:
    # \cite{key}, \citep{key}, \citet{key}, \citep*{key}, \citet*{key},
    # \citeauthor{key}, \citeyear{key}
    # Also handles multiple keys in one citation: \cite{key1,key2,key3}
    # Also handles citations preceded by a tilde: text~\cite{key}
    pattern = r'\\cite(?:t\*?|p\*?|author|year)?\s*{([^}]*)}'
    citations = set()
    
    for match in re.finditer(pattern, content):
        # Split by comma and strip whitespace for multiple keys
        keys = [key.strip() for key in match.group(1).split(',')]
        citations.update(keys)
    
    return citations

def filter_bib_file(bib_path: Union[str, Path], used_citations: Set[str]) -> str:
    """
    Filter a BibTeX file to only include used references.
    
    Args:
        bib_path: Path to the BibTeX file
        used_citations: Set of citation keys to keep
        
    Returns:
        Filtered BibTeX content
    """
    bib_path = Path(bib_path)
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match complete BibTeX entries
    entry_pattern = r'(@[^@]*)'
    filtered_entries = []
    
    for entry in re.finditer(entry_pattern, content, re.DOTALL):
        entry_text = entry.group(1)
        # Extract the citation key
        key_match = re.match(r'@\w+\s*{\s*([^,\s]*)', entry_text)
        if key_match and key_match.group(1) in used_citations:
            filtered_entries.append(entry_text)
    
    return '\n'.join(filtered_entries) 