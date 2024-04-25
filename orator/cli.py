import click

from . import tts


@click.group()
def cli():
    pass


@cli.command(name='orate')
@click.option('--book-path', help='Path to `epub` file.')
@click.option('--out-path', help='Path to directory for generated audio.')
def _orate(book_path, out_path):
    """CLI wrapper for orate function.

    See Also
    --------
    `orate`
    """
    return tts.orate(book_path, out_path)