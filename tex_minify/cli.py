"""Command-line interface for tex-minify."""

import sys
from pathlib import Path
import click
from .processor import process_tex_file
from .bib_processor import extract_citations, filter_bib_file


@click.group()
def cli():
    """TeX Minify - A tool for processing TeX files."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('-o', '--output', type=click.Path(dir_okay=False, path_type=Path),
              help='Output file path. If not specified, prints to stdout.')
@click.option('--base-dir', type=click.Path(exists=True, file_okay=False, path_type=Path),
              help='Base directory for resolving \\input paths. Defaults to input file directory.')
def minify(input_file: Path, output: Path | None, base_dir: Path | None) -> None:
    """
    Process a TeX file and expand all \\input commands.
    
    INPUT_FILE: Path to the input TeX file
    """
    try:
        processed_content = process_tex_file(input_file, base_dir=base_dir)
        
        if output:
            output.write_text(processed_content, encoding='utf-8')
            click.echo(f"Processed TeX file written to: {output}", err=True)
        else:
            click.echo(processed_content)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('tex_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument('bib_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('-o', '--output', type=click.Path(dir_okay=False, path_type=Path),
              help='Output file path. If not specified, prints to stdout.')
def filter_bib(tex_file: Path, bib_file: Path, output: Path | None) -> None:
    """
    Filter a BibTeX file to only include references used in the TeX file.
    
    TEX_FILE: Path to the input TeX file
    BIB_FILE: Path to the input BibTeX file
    """
    try:
        # First minify the TeX file to get all citations
        processed_content = process_tex_file(tex_file)
        
        # Extract citations from the processed content
        used_citations = extract_citations(processed_content)
        
        # Filter the BibTeX file
        filtered_content = filter_bib_file(bib_file, used_citations)
        
        if output:
            output.write_text(filtered_content, encoding='utf-8')
            click.echo(f"Filtered BibTeX file written to: {output}", err=True)
            click.echo(f"Kept {len(used_citations)} citations", err=True)
        else:
            click.echo(filtered_content)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli() 