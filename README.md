# tex-minify

A command-line tool to expand `\input` commands in TeX files.

## Usage

### Using uvx (no installation required)

```bash
# Basic usage (prints to stdout)
uvx tex-minify input.tex

# Save to output file
uvx tex-minify input.tex -o output.tex

# Specify base directory for \input resolution
uvx tex-minify input.tex --base-dir /path/to/tex/files -o output.tex
```

### Using pip installation

First install:
```bash
pip install tex-minify
```

Then use:
```bash
tex-minify input.tex -o output.tex
```

### Using pixi (for development)

```bash
# Setup development environment
pixi install
pixi run install

# Run the tool
pixi run tex-minify input.tex
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