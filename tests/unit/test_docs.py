import inspect
import re
from pathlib import Path

from cosplay2py import Cosplay2

API_NOTES = Path(__file__).parents[2] / "docs" / "api-notes.md"


def test_api_notes_list_every_method() -> None:
    documented = set(re.findall(r"`(\w+\.\w+)\(\)`", API_NOTES.read_text("utf-8")))
    methods = {
        f"{attr}.{name}"
        for attr, cls in inspect.get_annotations(Cosplay2).items()
        for name in vars(cls)
        if not name.startswith("_")
    }
    assert methods - documented == set(), "add these to docs/api-notes.md"
