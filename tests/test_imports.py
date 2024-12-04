# Copyright (C) 2024-present Michaël Hooreman <mhooreman@icloud.com>
"""Testing of modules import."""

import importlib
import pathlib
import typing

import pytest

import pdfcleaner


def _gen_modules() -> typing.Iterator[str]:
    pkgdir = pathlib.Path(pdfcleaner.__file__).parent
    for f_ in pkgdir.glob("**/*.py"):
        f = f_.relative_to(pkgdir.parent)
        y = list(f.parts[:-1])
        if f.stem != "__init__":
            y.append(f.stem)
        yield ".".join(y)


@pytest.mark.parametrize("module", _gen_modules())
def test_import(module: str) -> None:
    """Test the import of a module.

    It simply loads it.
    """
    importlib.import_module(module)
