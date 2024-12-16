# tex-minify

A command-line tool to expand `\input` commands in TeX files.

## Installation

Using pixi:

```bash
pixi install
pixi run install
```

## Usage

```bash
# Basic usage (prints to stdout)
tex-minify input.tex

# Save to output file
tex-minify input.tex -o output.tex

# Specify base directory for \input resolution
tex-minify input.tex --base-dir /path/to/tex/files -o output.tex
```

## Features

- Recursively expands all `\input` commands in TeX files
- Handles relative paths correctly
- Supports both `.tex` extension present or not in `\input` commands
- UTF-8 encoding support
- Configurable base directory for input resolution

## Error Handling

The tool will exit with a non-zero status code and display an error message if:
- Input file is not found
- Referenced `\input` files are not found
- Output file cannot be written
- Any other processing errors occur 