"""The application classes."""

import dataclasses
import pathlib

# Copyright (C) 2024-present Michaël Hooreman <mhooreman@icloud.com>
import click
import pypdf


@dataclasses.dataclass(frozen=True)
class PdfCleaner:
    """The application main entry point."""

    top_input_path: pathlib.Path
    top_output_path: pathlib.Path

    @property
    def input_files(self) -> tuple[pathlib.Path, ...]:
        """Return all the input files (sorted)."""
        return tuple(sorted(self.top_input_path.glob("**/*.pdf")))

    def _input_path_to_output(self, input_path: pathlib.Path) -> pathlib.Path:
        return self.top_output_path.joinpath(
            input_path.relative_to(self.top_input_path)
        )

    @classmethod
    def _convert_file(cls, in_: pathlib.Path, out_: pathlib.Path) -> None:
        """Convert input path to output path.

        It reads the pages from the input path and copies them to the output
        path.

        Since only the pages are read, no additional artificial widget hiding
        the content is shown on the pages, and JavaScript code is dropped.
        """
        if not out_.parent.exists():
            out_.parent.mkdir(parents=True, exist_ok=True)
        with pypdf.PdfReader(in_) as rd, pypdf.PdfWriter(out_) as wr:
            for p in rd.pages:
                wr.add_page(p)

    def __call__(self) -> None:
        """Run the converter.

        This is the entry point for instances.
        """

        def _item_label(f: pathlib.Path) -> str:
            if f is None:
                return None
            return str(f.relative_to(self.top_input_path))

        with click.progressbar(
            self.input_files,
            item_show_func=_item_label,  # type: ignore
            width=0,
        ) as pbar:
            for f in pbar:
                g = self._input_path_to_output(f)
                self._convert_file(f, g)
