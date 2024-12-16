"""Command-line interface for tex-minify."""

import sys
from pathlib import Path
import click
from .processor import process_tex_file


@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('-o', '--output', type=click.Path(dir_okay=False, path_type=Path),
              help='Output file path. If not specified, prints to stdout.')
@click.option('--base-dir', type=click.Path(exists=True, file_okay=False, path_type=Path),
              help='Base directory for resolving \\input paths. Defaults to input file directory.')
def main(input_file: Path, output: Path | None, base_dir: Path | None) -> None:
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


if __name__ == '__main__':
    main() 