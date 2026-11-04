"""Run with a clean interpreter after installing a built wheel or sdist."""

import importlib.metadata
import importlib.resources
import tomllib
from pathlib import Path

import cosplay2py
from cosplay2py import AsyncCosplay2, Cosplay2

expected = tomllib.loads(
    (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text("utf-8")
)["project"]["version"]
assert importlib.metadata.version("cosplay2py") == expected
assert cosplay2py.__version__ == expected
assert importlib.resources.files("cosplay2py").joinpath("py.typed").is_file()
assert Cosplay2
assert AsyncCosplay2
print("Installed package imports, version and typing marker verified.")
