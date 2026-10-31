import inspect
import re
from pathlib import Path

from cosplay2py import Cosplay2

API_REFERENCE = Path(__file__).parents[2] / "docs" / "api"


def test_api_reference_lists_every_method() -> None:
    reference = "\n".join(
        page.read_text("utf-8")
        for page in API_REFERENCE.glob("*.md")
        if page.stem not in {"workflows", "sdk-normalization", "index"}
    )
    documented = set(re.findall(r"`(\w+\.\w+)\(\)`", reference))
    methods = {
        f"{attr}.{name}"
        for attr, cls in inspect.get_annotations(Cosplay2).items()
        for name in vars(cls)
        if not name.startswith("_")
    }
    assert methods - documented == set(), "add these to the matching docs/api/ page"
