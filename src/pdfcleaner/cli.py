# Copyright (C) 2024-present Michaël Hooreman <mhooreman@icloud.com>

"""Command line interface."""

import pathlib

import click
from loguru import logger

from pdfcleaner.__about__ import __version__
from pdfcleaner.app import PdfCleaner


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(
    version=__version__,
)
@click.option(
    "--input_dir",
    "-i",
    help="The top input directory.",
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--output_dir",
    "-o",
    help="The top output directory.",
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=pathlib.Path,
    ),
)
@logger.catch
def pdfcleaner(input_dir: pathlib.Path, output_dir: pathlib.Path) -> None:
    """Convert PDF to PDF by keeping only the pages contents.

    That way, any additional content, for example to hide pages contents, is
    dropped.
    """
    logger.info("Starting")
    PdfCleaner(input_dir, output_dir)()
    logger.info("Completed")
