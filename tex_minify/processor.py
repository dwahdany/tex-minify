"""TeX processor module for expanding \\input commands."""

import os
import re
from pathlib import Path
from typing import Union, Optional


def process_tex_file(file_path: Union[str, Path], base_dir: Optional[Path] = None) -> str:
    """
    Process a TeX file and expand all \\input commands.
    
    Args:
        file_path: Path to the TeX file
        base_dir: Base directory for relative paths in \\input commands
        
    Returns:
        Processed TeX content with expanded \\input commands
    """
    file_path = Path(file_path)
    if base_dir is None:
        base_dir = file_path.parent

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def expand_input(match: re.Match) -> str:
        input_path = match.group(1).strip('{}')
        # Handle both .tex extension present or not
        if not input_path.endswith('.tex'):
            input_path += '.tex'
        
        full_path = base_dir / input_path
        if not full_path.exists():
            raise FileNotFoundError(f"Input file not found: {full_path}")
            
        # Recursively process the input file
        return process_tex_file(full_path, base_dir=base_dir)

    # Replace all \input commands
    # This regex matches \input{filename} or \input {filename} patterns
    pattern = r'\\input\s*{([^}]*)}'
    processed_content = re.sub(pattern, expand_input, content)
    
    return processed_content 