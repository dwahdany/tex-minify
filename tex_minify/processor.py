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
    current_dir = file_path.parent
    
    # If no base_dir is provided, use the directory of the current file
    if base_dir is None:
        base_dir = current_dir

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def expand_input(match: re.Match) -> str:
        input_path = match.group(1).strip('{}')
        # Handle both .tex extension present or not
        if not input_path.endswith('.tex'):
            input_path += '.tex'
        
        # Try paths in order:
        # 1. Relative to current file's directory
        # 2. Relative to base directory
        # 3. As a nested path from base directory
        paths_to_try = [
            current_dir / input_path,
            base_dir / input_path,
            base_dir / Path(*Path(input_path).parts)
        ]
        
        for full_path in paths_to_try:
            if full_path.exists():
                # Recursively process the input file, using its directory as the new base_dir
                return process_tex_file(full_path, base_dir=base_dir)
                
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            f"Tried:\n" +
            "\n".join(f"  - {p}" for p in paths_to_try)
        )

    # Replace all \input commands with their expanded content
    pattern = r'\\input\{([^}]+)\}'
    return re.sub(pattern, expand_input, content)