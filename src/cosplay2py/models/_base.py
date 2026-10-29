from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

_FRONTEND_NOISE = ("wid", "$$hashKey")


class Cosplay2Model(BaseModel):
    """Base for all response models.

    The Cosplay2 API is undocumented and evolves without notice, so unknown fields
    are kept (reachable via ``model_extra``) instead of failing validation.
    """

    model_config = ConfigDict(extra="allow", frozen=True, populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _strip_frontend_noise(cls, data: Any) -> Any:
        # Strip per-tab pool IDs (`wid`) and AngularJS `ng-repeat` keys (`$$hashKey`)
        # that the site's frontend accidentally saves into JSON blobs.
        if isinstance(data, dict) and any(k in data for k in _FRONTEND_NOISE):
            return {k: v for k, v in data.items() if k not in _FRONTEND_NOISE}
        return data
