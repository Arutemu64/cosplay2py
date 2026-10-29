from pydantic import BaseModel, ConfigDict


class Cosplay2Model(BaseModel):
    """Base for all response models.

    The Cosplay2 API is undocumented and evolves without notice, so unknown fields
    are kept (reachable via ``model_extra``) instead of failing validation.
    """

    model_config = ConfigDict(extra="allow", frozen=True, populate_by_name=True)
