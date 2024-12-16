# tex-minify

A command-line tool to expand `\input` commands in TeX files and filter BibTeX files based on citations.

## Features

- Recursively expands all `\input` commands in TeX files
- Handles relative paths correctly
- Supports both `.tex` extension present or not in `\input` commands
- UTF-8 encoding support
- Configurable base directory for input resolution
- Filter BibTeX files to only keep cited references

## Usage

### Using uvx (no installation required)

```bash
# Minify a TeX file (prints to stdout)
uvx tex-minify minify input.tex

# Save minified output to file
uvx tex-minify minify input.tex -o output.tex

# Specify base directory for \input resolution
uvx tex-minify minify input.tex --base-dir /path/to/tex/files -o output.tex

# Filter BibTeX file to only keep cited references
uvx tex-minify filter-bib paper.tex references.bib -o filtered.bib
```

### Using pip installation

First install:
```bash
pip install tex-minify
```

Then use:
```bash
# Minify a TeX file
tex-minify minify input.tex -o output.tex

# Filter BibTeX file
tex-minify filter-bib paper.tex references.bib -o filtered.bib
```

### Using pixi (for development)

```bash
# Setup development environment
pixi install
pixi run install

# Run the tool
pixi run -- tex-minify minify input.tex
pixi run -- tex-minify filter-bib paper.tex references.bib
```

## Commands

### minify

Process a TeX file and expand all `\input` commands.

```bash
tex-minify minify INPUT_FILE [-o OUTPUT] [--base-dir BASE_DIR]
```

Arguments:
- `INPUT_FILE`: Path to the input TeX file
- `-o, --output`: Output file path (optional, defaults to stdout)
- `--base-dir`: Base directory for resolving `\input` paths (optional, defaults to input file directory)

### filter-bib

Filter a BibTeX file to only include references that are cited in the TeX file.

```bash
tex-minify filter-bib TEX_FILE BIB_FILE [-o OUTPUT]
```

Arguments:
- `TEX_FILE`: Path to the TeX file containing citations
- `BIB_FILE`: Path to the BibTeX file to filter
- `-o, --output`: Output file path (optional, defaults to stdout)

## Error Handling

The tool will exit with a non-zero status code and display an error message if:
- Input files are not found
- Referenced `\input` files are not found
- Output file cannot be written
- Any other processing errors occur